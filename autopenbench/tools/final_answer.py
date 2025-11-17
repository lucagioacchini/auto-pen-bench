from pydantic import BaseModel
from pydantic import Field


class FinalAnswer(BaseModel):
    """Provide the final flag of the CTF game."""
    flag: str = Field(..., description="The captured flag")

    def run(self, correct_flag: str) -> str:
        if self.flag == correct_flag:
            return "Congratulations! You have captured the correct flag."
        else:
            return "Incorrect flag. Please try again."