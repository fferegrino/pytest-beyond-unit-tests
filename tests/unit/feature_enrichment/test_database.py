import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from feature_enrichment.database import Base, DatabaseService, RestaurantFeatures


@pytest.fixture
def db_path(tmp_path):
    """
    Fixture that provides a path to a temporary SQLite database file.

    Uses `tmp_path` which is a fixture provided by pytest that points to a temporary directory.
    This `tmp_path` is unique to each test run.
    """
    path = tmp_path / "test.db"
    yield f"sqlite:///{path}"
    path.unlink()


@pytest.fixture
def test_engine(db_path):
    """Creates a SQLAlchemy engine for the test database."""
    return create_engine(db_path)


@pytest.fixture
def test_session(test_engine):
    """Creates a session for interacting with the test database."""
    Base.metadata.create_all(test_engine)  # Create all tables in the test database
    Session = sessionmaker(bind=test_engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def db_service(test_engine, db_path):
    """Provides a DatabaseService instance configured to use the test database."""
    return DatabaseService(db_uri=db_path)


def test_get_restaurant_features_existing_id(test_session, db_service):
    # Insert a sample restaurant feature into the test database
    test_session.add(RestaurantFeatures(id=1, current_order_count=10, average_delivery_time_30_mins=15.5))
    test_session.commit()

    # Fetch the restaurant feature using the service
    result = db_service.get_restaurant_features(1)

    assert result is not None
    assert result["id"] == 1
    assert result["current_order_count"] == 10
    assert result["average_delivery_time_30_mins"] == 15.5


def test_get_restaurant_features_non_existing_id(test_session, db_service):
    result = db_service.get_restaurant_features(999)
    assert result is None
