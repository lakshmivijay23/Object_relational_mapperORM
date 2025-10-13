🔧 Key Components

Engine: Manages database connectivity and provides access to the database via connections.

Connection: Obtained from the Engine, used for executing SQL statements directly (Core).

Session: ORM facade over Connection; handles transactions and execution in ORM-style.

📌 Working with Engine and Connection

engine.connect() provides a Connection object.

Use a context manager (with) to manage the lifecycle and resources properly.

SQL can be written as textual SQL using text().

Example:

from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text("SELECT 'hello world'"))
    print(result.all())


Transactions are implicitly begun when a connection is opened.

Default behavior: ROLLBACK unless you call commit() explicitly.

You can either:

Commit as you go using conn.commit().

Use engine.begin() for an automatic transaction block with commit/rollback.

🗃️ Fetching Data from Result

Returned rows can be accessed using:

Tuple unpacking

Indexing (e.g., row[0])

Attribute access (e.g., row.x)

Dictionary-style access via .mappings()

💡 Sending Parameters

Use bound parameters to prevent SQL injection and allow query reusability:

result = conn.execute(text("SELECT * FROM table WHERE y > :y"), {"y": 5})


Avoid inserting Python variables directly into SQL strings.

📦 Sending Multiple Parameters ("executemany")

To insert multiple rows at once:

conn.execute(
    text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
    [{"x": 1, "y": 2}, {"x": 3, "y": 4}]
)


This is faster and more efficient for bulk operations.

🧠 Using the ORM’s Session

ORM's Session behaves similarly to Connection.

Use it with with Session(engine) as session:

stmt = text("SELECT x, y FROM some_table WHERE y > :y")
with Session(engine) as session:
    result = session.execute(stmt, {"y": 6})


Call session.commit() to persist changes (e.g., after INSERT/UPDATE).

Session manages connections under the hood and obtains a new one as needed.

❓ Q&A: SQLAlchemy Core and ORM Execution Basics

Q1: What is the difference between engine.connect() and engine.begin()?
A:

connect() gives you a connection and you must call commit() manually.

begin() wraps the entire block in a transaction and automatically commits or rolls back depending on success or error.

Q2: What is the benefit of using the text() construct?
A: It allows you to write raw SQL statements safely, while still supporting bound parameters for security and efficiency.

Q3: What happens if you don't call commit() after executing DML (INSERT/UPDATE/DELETE)?
A: The transaction is rolled back automatically at the end of the connection block, and changes are not saved.

Q4: How do you safely pass variables into a SQL statement?
A: Use bound parameters with text() and pass a dictionary:

text("SELECT * FROM table WHERE x = :val"), {"val": 5}


Q5: How does the Session object relate to the Connection?
A: The Session internally uses a Connection. When session.execute() is called, it retrieves a connection from the Engine.

Q6: What's the best way to insert many rows at once?
A: Use executemany style by passing a list of dictionaries to execute():

conn.execute(text("INSERT INTO ..."), [{"x": 1}, {"x": 2}])


Q7: Is text() the recommended way to work with SQLAlchemy?
A: No — text() is primarily for quick tests or raw SQL use cases. SQLAlchemy's Core Expression Language or ORM Query API is preferred for most use.