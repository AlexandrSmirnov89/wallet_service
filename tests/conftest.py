import pytest

pytest_plugins = "pytest_asyncio"

def pytest_configure():
    pytest.asyncio_mode = "auto"
