from pydantic import BaseModel
from pydantic import Field


class FinalAnswer(BaseModel):
    """Provide the final flag of the CTF game."""
    flag: str = Field(..., description="The captured flag")
