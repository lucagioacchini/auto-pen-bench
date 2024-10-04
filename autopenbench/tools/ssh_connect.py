import paramiko
import paramiko.ssh_exception
from pydantic import BaseModel
from pydantic import Field
import time


def wait_for_message(shell: paramiko.Channel):
    """Waits for a specific prompt message indicating that the shell is ready 
    for user input.

    Args:
        shell (paramiko.Channel): The active shell session from which to 
        receive the output.

    Returns:
        str: The accumulated output from the shell session as a string until a 
        valid prompt is detected.
    """
    out = str(shell.recv(9999).decode())  # Initial output read from the shell.
    last_line = ''

    # Loop until a valid prompt (like bash prompt) is detected in the output.
    while True:
        last_line = out.split('\n')[-1]  # Extract the last line of output.

        # Check if the last line indicates a prompt, such as a
        # username@hostname:$ or root@hostname:#.
        if ('@' in last_line and ('$' in last_line or '#' in last_line)) or \
                ('bash' in last_line and ('$' in last_line or '#' in last_line)):
            break

        time.sleep(.5)  # Wait for a short period before reading more data.
        # Read more data and append to the output.
        out = out + str(shell.recv(9999).decode())

    return out


class SSHConnect(BaseModel):
    """Start an SSH session into the target machine"""
    ssh_ipaddr: str = Field(..., description="Remote server")
    ssh_port: int = Field(...)
    ssh_username: str = Field(...)
    ssh_password: str = Field(...)

    def _open_kali_tunnel(self, ssh_kali: paramiko.SSHClient):
        """Opens an SSH tunnel from the Kali machine to the remote machine.

        Args:
            ssh_kali (paramiko.SSHClient): SSHClient connected to the Kali 
            machine.

        Returns:
            paramiko.Channel or str: The channel created for the tunnel if 
            successful, or an error message if not.
        """
        ssh_kali_transport = ssh_kali.get_transport()
        local_listen_addr = ('127.0.0.1', 2222)  # Local address to listen on
        # Remote server address and port
        remote_addr = (self.ssh_ipaddr, self.ssh_port)

        try:
            # Open a direct TCP/IP channel for tunneling traffic between the
            # Kali machine and the remote server
            ssh_kali_channel = ssh_kali_transport.open_channel(
                "direct-tcpip",
                remote_addr,
                local_listen_addr,
                timeout=10
            )
            return ssh_kali_channel
        except paramiko.ssh_exception.SSHException as e:
            # Error if tunnel fails
            return f'No SSH service active at {self.ssh_ipaddr}:{self.ssh_port}'

    def _connect_to_remote(self, ssh_kali: paramiko.SSHClient):
        """Establishes a connection to the remote server through the Kali 
        machine.

        Args:
            ssh_kali (paramiko.SSHClient): SSHClient connected to the Kali 
            machine.

        Returns:
            tuple: A tuple containing the shell object or SSHClient and a 
            message (either output or error).
        """
        ssh = paramiko.SSHClient()
        # Automatically accept host keys
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Set up the tunnel through the Kali machine
        tunnel = self._open_kali_tunnel(ssh_kali)

        # If tunnel setup fails, return the error message
        if type(tunnel) == str:
            return ssh, tunnel

        try:
            # Attempt to connect to the remote server through the tunnel
            ssh.connect(
                self.ssh_ipaddr,
                username=self.ssh_username,
                password=self.ssh_password,
                port=int(self.ssh_port),
                sock=tunnel
            )
            ssh = ssh.invoke_shell()  # Open an interactive shell session
            msg = wait_for_message(ssh)  # Wait for the shell to be ready
        except Exception as error:
            msg = str(error)  # Capture any connection errors

        # Return the SSH object and the message (output or error)
        return ssh, msg

    def run(self, ssh_kali: paramiko.SSHClient):
        """Executes the SSH connection and returns the result.

        Args:
            ssh_kali (paramiko.SSHClient): SSHClient connected to the Kali 
            machine.

        Returns:
            tuple: A tuple containing the shell object or SSHClient and a 
            message (either output or error).
        """
        connection_result = self._connect_to_remote(ssh_kali)

        return connection_result
