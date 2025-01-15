import pytest
import json
from send2airgap.backend import Backend


@pytest.mark.skip(reason="no json mock")
def test_is_json():
    backend = Backend(None)
    data = backend.get_json_data()

    try:
        parsed_data = json.loads(data)  # Try to parse the data
        assert isinstance(
            parsed_data, (dict, list)
        )  # JSON must be a dict or list
    except json.JSONDecodeError:
        pytest.fail("The data is not valid JSON")
