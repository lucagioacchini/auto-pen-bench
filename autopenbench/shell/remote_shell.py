import time
import socket
import chardet
import paramiko


def receive_data(shell: paramiko.Channel):
    """Receives data from the shell and decodes it using the appropriate
    character encoding.

    Args:
        shell (paramiko.Channel): The active shell session from which to
        receive data.

    Returns:
        str: Decoded output from the shell session, or an empty string if
        there's a timeout.
    """
    try:
        data = shell.recv(9999)  # Receive data from the shell
    except socket.timeout:
        return ''  # Return empty string on timeout

    try:
        text_data = data.decode('utf-8')  # Try to decode data using UTF-8
    except UnicodeDecodeError:
        # If UTF-8 decoding fails, use chardet to detect the correct encoding
        # and decode accordingly
        encoding = chardet.detect(data)['encoding']
        # Replace invalid characters
        text_data = data.decode(encoding, errors='replace')

    return text_data  # Return the decoded text data


class RemoteShell():
    """A class to manage an interactive remote shell session.

    Args:
        shell (paramiko.Channel): The shell channel for sending and receiving data.

    Attributes:
        sudo (bool): Indicates whether sudo is in use in the current session.
        shell (paramiko.Channel): The shell session channel.
        msfshell (bool): Indicates whether a Metasploit shell is active.

    Methods:
        check_metasploit_shell(out): Checks if the output is from a Metasploit shell.
        execute_cmd(cmd): Sends a command to the shell and retrieves the output.
    """

    def __init__(self, shell: paramiko.Channel):
        self.sudo = False  # Track if sudo is active
        self.shell = shell  # Store the shell session
        self.msfshell = False  # Track if using a Metasploit shell
        try:
            # Set a timeout for receiving data from the shell
            self.shell.settimeout(5.0)
        except:
            pass

    def check_metasploit_shell(self, out: str):
        """Checks whether the session output indicates a Metasploit shell.

        Args:
            out (str): The shell output to check.

        Returns:
            bool: True if a Metasploit shell is detected and open, False
            otherwise
        """
        # Parse the output line by line
        for l in out.split('\n'):
            if 'Command shell session' in l:
                if 'opened' in l:
                    return True  # If Metasploit shell session is open
                if 'closed' in l:
                    return False  # If Metasploit shell session is closed
        return self.msfshell  # Return the current state of msfshell

    def execute_cmd(self, cmd: str):
        """Sends a command to the remote shell and processes the response.

        Args:
            cmd (str): The command to be executed.

        Returns:
            str: The output from the shell after executing the command.
        """
        # Check if forbidden commands are being used (like netcat or socat)
        for x in cmd.split(' '):
            if x == 'nc' or x == 'socat':
                return "Don't use netcat or socat!"

        retries = 0  # Counter for retries if the shell doesn't respond as expected
        self.shell.send(cmd+'\n')  # Send the command to the shell
        out = receive_data(self.shell)  # Receive initial data from the shell

        # Special handling for sudo commands
        if cmd[:4] == 'sudo':
            self.sudo = True  # Set sudo mode

            # Wait for the shell to ask for the sudo password
            while 'password' not in out.lower():
                last_line = out.split('\n')[-1]  # Get the last line of output
                if '$' in last_line or '#' in last_line:
                    if self.sudo:
                        self.sudo = False  # Disable sudo mode if prompt is ready
                    break
                time.sleep(.5)  # Wait before attempting to receive more data
                out += str(self.shell.recv(9999).decode('utf-8',
                           errors='ignore'))  # Append new data
        else:
            # Handle non-sudo commands
            last_line = ' '
            while True:
                lines = out.split('\n')  # Split output into lines
                lines = [x.strip() for x in lines if x.strip()
                         != '']  # Clean up empty lines
                if len(lines) > 0:
                    # Get the last line of the cleaned output
                    last_line = lines[-1].strip()

                # Check if it's a Metasploit shell session
                self.msfshell = self.check_metasploit_shell(out)
                if self.msfshell and 'exit' in cmd:
                    # Exit the Metasploit shell if 'exit' command is issued
                    self.msfshell = False

                # If sudo is not active, check for a command prompt
                if not self.sudo:
                    # Check for common shell prompt formats (e.g., user@hostname:$ or #)
                    if ('@' in last_line and (
                            last_line[-1] == '$' or last_line[-1] == '#'
                        )) or ('bash' in last_line and (
                            last_line[-1] == '$' or last_line[-1] == '#')):
                        break
                    # Handle various prompt-like outputs, retries on common cases
                    elif last_line[-1] in ['?', '$', '#'] or \
                        'yes/no/[fingerprint]' in last_line.lower() or \
                        '[y/n]' in last_line.lower() or \
                        '--more--' in last_line.lower() or \
                            'msf6' in last_line.lower():
                        retries += 1

                    elif last_line[-1] == ':' and \
                        '::' not in last_line and \
                            '-->' not in last_line:
                        retries += 1

                    elif last_line[-1] == '>' and \
                        '<' not in last_line and \
                            '-->' not in last_line:
                        retries += 1

                    if 'What do you want to do about modified configuration '\
                            'file sshd_config?' in out:
                        break  # Special case handling for configuration prompts
                    if retries == 3:  # If retries hit 3, stop waiting for output
                        break
                else:
                    # If sudo is active, check for the appropriate prompt
                    if ':' in last_line[-1] and '::' not in last_line:
                        retries += 1
                    if '@' in last_line and ('$' in last_line[-1] or
                                             '#' in last_line[-1]):
                        self.sudo = False  # Disable sudo mode if prompt is detected
                        break
                    if retries == 3:  # Stop waiting after 3 retries
                        break

                # Continuously receive more data from the shell
                received_data = receive_data(self.shell)
                if received_data != '':
                    out = out + received_data

                # For Metasploit shells, simulate stopping the output with a prompt
                if self.msfshell:
                    out = f'{out}\nmeterpreter >'
                    break

        # Handle special output formatting for Metasploit shells
        if not self.msfshell:
            pass
        else:
            if '^J' in out:
                # Remove unnecessary ^J from output
                out = '\n'.join(out.split('^J')[1:])
            else:
                # Remove first line if not needed
                out = '\n'.join(out.split('\n')[1:])

        return out  # Return the complete output after command execution
