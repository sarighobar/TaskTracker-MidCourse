import pytest
from app.database import Base, engine

@pytest.fixture(autouse=True)
def run_around_tests():
    # Clear out DB tables
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield