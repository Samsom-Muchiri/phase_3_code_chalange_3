from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from .review import Review
from .restaurant import Restaurant


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

    # Establish a one-to-many relationship with reviews
    reviews = relationship('Review')
    restaurants = relationship(
        "Restaurant", secondary="reviews")

    def full_name(self):

        return f"{self.first_name} {self.last_name}"

    def nnn(self):
        return "sam"

    def customer_reviews(self, session):
        return session.query(Review).filter_by(customer=self).all()

    def favorite_restaurant(self, session):

        restaurant_counts = {}

        # Query all reviews associated with this customer
        reviews = session.query(Review).filter_by(customer_id=self.id).all()

        for review in reviews:
            restaurant_id = review.restaurant_id

            if restaurant_id in restaurant_counts:
                restaurant_counts[restaurant_id] += 1
            else:
                restaurant_counts[restaurant_id] = 1

        # Check if there are reviews before finding the favorite
        if restaurant_counts:
            favorite_id = max(restaurant_counts, key=restaurant_counts.get)
            favorite = session.query(Restaurant).get(favorite_id)
            return favorite
        else:
            return None

    def add_review(self, session, restaurant, rating, comment):
        review = Review(customer=self, restaurant=restaurant,
                        rating=rating, comment=comment)
        session.add(review)
        return review

    def delete_reviews(self, session, restaurant):
        # Delete all reviews by this customer for the specified restaurant
        reviews_to_delete = [
            review for review in self.reviews if review.restaurant == restaurant]
        for review in reviews_to_delete:
            session.delete(review)
        session.commit()
