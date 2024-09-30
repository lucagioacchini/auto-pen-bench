from pydantic import BaseModel
from pydantic import Field
import os

from dotenv import load_dotenv
load_dotenv()

SCRIPTS = os.environ.get("KALISCRIPTS")


class WriteFile(BaseModel):
    """Write a script or a text into a file. The file will be located in the 
    /root/scripts foolder of Kali machine."""
    content: str = Field(...)
    file_name: str = Field(...)

    def run(self):
        """Write a script in the /root/scripts folder of the Kali container 

        Returns:
            str: observation for the agent
        """
        with open(f'{SCRIPTS}/{self.file_name}', 'w') as file:
            file.write(self.content)
        output = f'File /root/scripts/{self.file_name} correctly saved.'

        return output
