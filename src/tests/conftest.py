from typing import Generator

import pytest

from app.database import Session


@pytest.fixture(scope="session")
def db() -> Generator:
    yield Session()
