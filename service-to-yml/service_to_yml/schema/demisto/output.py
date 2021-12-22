from pydantic import BaseModel, Field


class Output(BaseModel):
    contextPath: str = ''
    description: str = ''
    type: str = 'String'
