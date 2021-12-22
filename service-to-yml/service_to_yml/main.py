from parser import Parser

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from schema import Demisto, WebSchema

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)


@app.post('/', response_model=Demisto.Integration)
async def service_to_yml(integration: WebSchema.Integration):
    parser = Parser(integration)
    return parser.parse()
