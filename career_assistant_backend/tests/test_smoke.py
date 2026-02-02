import requests
import pytest

BASE = "http://127.0.0.1:8000"


def _try_get(path, timeout=2):
    try:
        return requests.get(BASE + path, timeout=timeout)
    except requests.exceptions.ConnectionError:
        pytest.skip("Server not running at 127.0.0.1:8000")


def _try_post(path, json, timeout=3):
    try:
        return requests.post(BASE + path, json=json, timeout=timeout)
    except requests.exceptions.ConnectionError:
        pytest.skip("Server not running at 127.0.0.1:8000")


def test_ping_live():
    r = _try_get("/ping")
    assert r.status_code == 200
    assert r.json() == {"status": "ok", "message": "pong"}


def test_root_live():
    r = _try_get("/")
    assert r.status_code == 200
    data = r.json()
    assert "message" in data and "status" in data


def test_docs_live():
    r = _try_get("/docs")
    assert r.status_code == 200


def test_query_live():
    # Send a simple non-sensitive query and assert we get a JSON answer (200)
    payload = {"question": "What is 2+2?", "session_id": "smoke-test-session"}
    r = _try_post("/query", json=payload)
    assert r.status_code == 200
    j = r.json()
    assert isinstance(j.get("answer"), str)

