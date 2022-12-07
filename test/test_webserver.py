import sys
from pathlib import Path

import pytest

project_path = Path(__file__).parent.parent.absolute()
sys.path.append(f"{project_path}")
sys.path.append(f"{project_path}/lib")

from fastapi.testclient import TestClient
from webserver import app

def test_client():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200


if __name__ == '__main__':
    pytest.main([f"f{project_path}/test/test_integration.py"])
