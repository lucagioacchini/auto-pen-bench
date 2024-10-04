from pydantic import BaseModel
from pydantic import Field
from autopenbench.shell import RemoteShell


class ExecuteBash(BaseModel):
    """Execute a shell command on a machine."""
    machine_ipaddr: str = Field(...)
    cmd: str = Field(...)

    def run(self, shell: RemoteShell):
        """Execute the bash within the Docker container

        Args:
            shell (src.RemoteShell): the interactive console of the container

        Returns:
            str: system observation for the agent
        """
        try:
            output = shell.execute_cmd(self.cmd)
        except Exception as e:
            output = "Before sending a remote command you need to set-up" \
                "an SSH connection."
        return output
