from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

# Create the engine and connect to the SQLite database
engine = create_engine('sqlite:///mydatabase.db', echo=True)

# Use a connection to execute raw SQL
with engine.connect() as conn:
    conn.execute(text("CREATE TABLE IF NOT EXISTS people (name TEXT, age INTEGER);"))
    conn.commit()  # Only needed if you're not using a session

# Use a session for inserting data
with Session(engine) as session:
    session.execute(
        text('INSERT INTO people (name, age) VALUES (:name, :age);'),
        {"name": "Mike", "age": 30}
    )
    session.commit()



