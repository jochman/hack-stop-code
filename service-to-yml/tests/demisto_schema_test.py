from pathlib import Path

import yaml

from service_to_yml.schema import Demisto


class TestDemistoSchema:
    def test_basic_integration(self):
        p = Path(__file__).parent /'assets' / 'sample_integration.yml'
        with open(p) as f:
            Demisto.Integration(**yaml.safe_load(f))
