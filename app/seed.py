from . import schemas, crud
from .database import SessionLocal
from alembic import command
from alembic.config import Config

# Sample data
users = [
    {"username": "john_doe", "email": "john@example.com", "password": "password123"},
    {"username": "jane_smith", "email": "jane@example.com", "password": "securepass456"},
]

stocks = [
    {"ticker_symbol": "AAPL", "number_of_shares": 10, "purchase_price": 150.00},
    {"ticker_symbol": "GOOGL", "number_of_shares": 5, "purchase_price": 2500.00},
    {"ticker_symbol": "MSFT", "number_of_shares": 15, "purchase_price": 300.00},
    {"ticker_symbol": "AMZN", "number_of_shares": 8, "purchase_price": 3200.00},
]

def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
def seed_database():
    # Run migrations
    run_migrations()
    db = SessionLocal()
    try:
        # Create users and their portfolios
        for user_data in users:
            # Check if user already exists
            existing_user = crud.get_user_by_username(db, user_data["username"])
            if existing_user:
                print(f"User {user_data['username']} already exists. Skipping.")
                continue
            user = schemas.UserCreate(**user_data)
            db_user = crud.create_user(db, user)
            print(f"Created user: {db_user.username}")

            # Create portfolio for the user
            existing_portfolio = crud.get_portfolio(db, db_user.id)
            if existing_portfolio:
                print(f"Portfolio for user {db_user.username} already exists. Skipping.")
                continue
            portfolio = crud.create_portfolio(db, db_user.id)
            print(f"Created portfolio for user: {db_user.username}")

            # Add stocks to the user's portfolio
            for stock_data in stocks:
                stock = schemas.StockCreate(**stock_data)
                db_stock = crud.add_stock(db, stock, portfolio.id)
                print(f"Added stock {db_stock.ticker_symbol} to {db_user.username}'s portfolio")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
    print("Database seeding completed.")