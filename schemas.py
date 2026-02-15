from pydantic import BaseModel
from typing import List

class DirectiveResponse(BaseModel):
    dos: List[str]
    donts: List[str]
    guidelines: List[str]
    deadlines: List[str]
