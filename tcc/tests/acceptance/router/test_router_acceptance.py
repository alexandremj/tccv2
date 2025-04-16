from fastapi.testclient import TestClient
from http import HTTPStatus
import pytest

from main import app


client = TestClient(app)

@pytest.mark.asyncio()
async def test_working():
    assert True


@pytest.mark.asyncio()
async def test_create_and_read():
    get = client.get("/posts/2")
    assert get.status_code == HTTPStatus.OK
