from sqlalchemy import Column, Float, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class RestaurantFeatures(Base):
    __tablename__ = "restaurant_features"

    id = Column(Integer, primary_key=True)
    current_order_count = Column(Integer)
    average_delivery_time_30_mins = Column(Float)


class DatabaseService:
    def __init__(self, db_uri):
        self.engine = create_engine(db_uri)
        self.Session = sessionmaker(bind=self.engine)

    def get_restaurant_features(self, restaurant_id):
        session = self.Session()
        try:
            result = session.query(RestaurantFeatures).filter(RestaurantFeatures.id == restaurant_id).one_or_none()
            return (
                {
                    "id": result.id,
                    "current_order_count": result.current_order_count,
                    "average_delivery_time_30_mins": result.average_delivery_time_30_mins,
                }
                if result
                else None
            )
        finally:
            session.close()
