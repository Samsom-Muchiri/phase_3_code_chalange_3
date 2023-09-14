from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship 
from .base import Base


class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(String)

    reviews = relationship('Review', back_populates='restaurant')
    customers = relationship('Customer', secondary='reviews')
    
    def all_reviews(self):
        review_strings = []
        for review in self.reviews:
            review_strings.append(f"Review for {self.name} by {review.customer.full_name()}: {review.rating} stars.")
        return review_strings

    @classmethod
    def fanciest(cls, session):
        # Find the restaurant with the highest price
        max_price = session.query(cls.price).order_by(cls.price.desc()).first()
        return session.query(cls).filter_by(price=max_price[0]).first()
