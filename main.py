from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.restaurant import Restaurant
from models.customer import Customer
from models.review import Review
from models.base import Base

# Define the database file and create the engine
DATABASE_URI = "sqlite:///restaurant_reviews.db"
engine = create_engine(DATABASE_URI)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Check if tables exist before creating them
try:
    Base.metadata.create_all(engine)
except Exception as e:
    pass  # Tables already exist, so do nothing

# Create sample data if it doesn't already exist


def add_customer(session, first_name, last_name):
    existing_customer = session.query(Customer).filter_by(
        first_name=first_name, last_name=last_name).first()
    if not existing_customer:
        customer = Customer(first_name=first_name, last_name=last_name)
        session.add(customer)


def add_restaurant(session, name, price):
    existing_restaurant = session.query(
        Restaurant).filter_by(name=name).first()
    if not existing_restaurant:
        restaurant = Restaurant(name=name, price=price)
        session.add(restaurant)


def add_review(session, customer, restaurant, rating, comment):
    review = Review(customer=customer, restaurant=restaurant,
                    rating=rating, comment=comment)
    session.add(review)


add_customer(session, 'Stanley', 'Mwangi')
add_customer(session, 'Lydia', 'Nyamoita')
add_customer(session, 'Valent', 'Carols')
add_customer(session, 'Denis', 'Luki')

add_restaurant(session, 'Debonairs Pizza', 1200)
add_restaurant(session, 'Mama Rocks', 500)
add_restaurant(session, 'Slate', 1500)
add_restaurant(session, 'Mawimbi', 2000)

# Add sample reviews
customer1 = session.query(Customer).filter_by(
    first_name='Stanley', last_name='Mwangi').first()
customer2 = session.query(Customer).filter_by(
    first_name='Lydia', last_name='Nyamoita').first()
restaurant1 = session.query(Restaurant).filter_by(
    name='Debonairs Pizza').first()
restaurant2 = session.query(Restaurant).filter_by(name='Mama Rocks').first()
restaurant4 = session.query(Restaurant).filter_by(name='Mawimbi').first()

if customer1 and restaurant1:
    add_review(session, customer1, restaurant1, 4, 'Great pizza!')

if customer2 and restaurant1:
    add_review(session, customer2, restaurant1, 5, 'Best pizza in town!')

if customer1 and restaurant4:
    add_review(session, customer1, restaurant4, 3, 'Best Steak ever!')

# Commit changes
session.commit()

# Test the new methods
print("Customers:")
for customer in session.query(Customer).all():
    print(f"Customer: {customer.first_name} {customer.last_name}")
    # No need to pass the session argument
    favorite = customer.favorite_restaurant(session)
    if favorite:
        print(f"Favorite Restaurant: {favorite.name}")
    else:
        print("No favorite restaurant found.")

    # Test adding a review
    new_review = customer.add_review(
        session, restaurant4, 4, 'Excellent food, drink and surrounding!')
    session.commit()
    print(f"Added review: {new_review.comment}")

print("Restaurants:")
for restaurant in session.query(Restaurant).all():
    print(f"{restaurant.name}, Price: {restaurant.price}")
    reviews = [review.full_review() for review in restaurant.reviews]
    if reviews:
        print(f"Reviews: {reviews}")
    else:
        print("No reviews for this restaurant")

# Close the session
session.close()
