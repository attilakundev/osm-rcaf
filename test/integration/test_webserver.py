from fastapi.testclient import TestClient
from src.webserver import app, project_path


def test_main_page():
    client = TestClient(app)
    response = client.get("/")
    assert client is not None
    assert response.status_code == 200


def test_compare_get():
    client = TestClient(app)
    response = client.get("/compare")
    assert client is not None
    assert response.status_code == 200

def test_about():
    client = TestClient(app)
    response = client.get("/about")
    assert client is not None
    assert response.status_code == 200

def test_debug_mode():
    client = TestClient(app)
    response = client.get("/debug_mode")
    assert response.status_code == 200


def test_analyze_url():
    client = TestClient(app)
    response = client.get("/analyze")
    assert response.status_code == 405
    relation = {
        "relation_id": "23099"
    }
    response = client.post("/analyze", data=relation)
    assert response.status_code == 200


def test_analyze_file():
    client = TestClient(app)
    response = client.get("/analyze_file")
    assert response.status_code == 405
    with open(f"{project_path}/test/files/simplest_way.xml", "rb") as file:
        files = {"relation_file": file}
        response = client.post("/analyze_file", files=files, data={"relation_id": "-99775"})
        assert response.status_code == 200


def test_fix_file():
    client = TestClient(app)
    with open(f"{project_path}/test/files/67157.xml", "rb") as file:
        files = {"relation_file": file}
        response = client.post("/fix", files=files, data={"first_way": "4293039"})
        assert response.status_code == 200
def test_compare_file():
    client = TestClient(app)
    with open(f"{project_path}/test/files/67157.xml", "rb") as file:
        files = {"old_rel": file, "new_rel": file}
        response = client.post("/compare", files=files, data={"relation_id": "67157"})
        assert response.status_code == 200