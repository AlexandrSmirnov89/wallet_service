import pytest
import uuid
from unittest.mock import patch
from fastapi.testclient import TestClient
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from src.main import app


client = TestClient(app)

@pytest.mark.asyncio
@patch("src.api.v1.tasks.wallet.process_wallet_operation.delay")
async def test_wallet_operation(mock_celery):
    wallet_id = str(uuid.uuid4())

    response = client.post(f"/api/v1/wallets/{wallet_id}/operation", json={"operationType": "DEPOSIT", "amount": 100})
    assert response.status_code == 202
    mock_celery.assert_called_once_with(wallet_id, "DEPOSIT", 100.0)

@pytest.mark.asyncio
@patch("src.api.v1.tasks.wallet.get_wallet_balance_task.delay")
async def test_get_wallet_balance(mock_celery):
    wallet_id = str(uuid.uuid4())

    response = client.get(f"/api/v1/wallets/{wallet_id}")
    assert response.status_code == 200
    mock_celery.assert_called_once_with(wallet_id)
