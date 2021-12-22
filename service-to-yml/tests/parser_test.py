from service_to_yml.schema import Demisto, WebSchema
from service_to_yml import Parser
from fastapi.testclient import TestClient
from service_to_yml import app

client = TestClient(app)

class TestParser:
    integration = WebSchema.Integration(
        configuration=WebSchema.Configuration(
            name='Sample',
            base_url='http://www.example.com',
            context_key='Integration',
            headers=[]
        ),
        commands=[]
    )

    integration_with_headers = integration.configuration.headers = [
        WebSchema.Param(
            key='Authorization',
            value='Bearer :token',
            required=True,
            hidden=False
        )]
    integration_with_params = integration.commands = [
        WebSchema.Command(
            name='cmd',
            method='GET',
            context_key='Event',
            suffix='event',
            params=[
                WebSchema.Param(
                    key='event',
                    value='',
                    required=False,
                    hidden=False
                )]
        )
    ]

    def test_basic_parse(self):
        global client
        r = client.post('/', json=self.integration.dict())
        js = r.json()
        assert js
