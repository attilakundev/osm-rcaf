import sys
from pathlib import Path
import pytest

project_path = Path(__file__).parents[2].absolute()
sys.path.append(f"{project_path}")
sys.path.append(f"{project_path}/lib")
sys.path.append(f"{project_path}/lib/model")
from fastapi.testclient import TestClient
from webserver import app


def test_client():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200


def test_analyze_url():
    client = TestClient(app)
    response = client.get("/analyze")
    assert response.status_code == 405  # NOT allowed method (since this is post)
    relation = {
        "relation_id": "23099"
    }
    response = client.post("/analyze", data=relation)
    assert response.status_code == 200  # because we redirect the user so it should be correct


def test_analyze_file():
    client = TestClient(app)
    response = client.get("/analyze_file")
    assert response.status_code == 405  # NOT allowed method (since this is post)
    with open(f"{project_path}/test/files/simplest_way.xml", "rb") as file:
        files = {"relation_file": file}
        response = client.post("/analyze_file", files=files)
        assert response.status_code == 200  # because we redirect the user so it should be correct