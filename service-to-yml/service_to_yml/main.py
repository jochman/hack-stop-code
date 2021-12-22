from typing import Optional

import yaml
from fastapi import FastAPI

from parser import Parser
from schema import Demisto, WebSchema
import logging


app = FastAPI()


@app.post('/', response_model=Demisto.Integration)
async def service_to_yml(integration: WebSchema.Integration):
    parser = Parser(integration)
    return parser.parse()
