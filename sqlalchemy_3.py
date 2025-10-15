
# Create a profile table and a Students table

from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.orm import declarative_base
import sqlalchemy as db

"""
declarative_base() creates a base class that all your ORM models will inherit from.
It tells SQLAlchemy:
"Hey, every class that inherits from this Base is a database model/table."
So Base becomes the foundation for all your model classes.
"""

Base = declarative_base()
engine = db.create_engine('sqlite:///school.db', echo=True)

# Create a table model
class Students(Base):
    __tablename__ = 'Students'
    first_name = db.Column(db.String(50), primary_key=True)
    last_name = db.Column(db.String(50), primary_key=True)
    course = db.Column(db.String(50), primary_key=True
                       )
    score = db.Column(db.Float)

# create table
Base.metadata.create_all(engine)

"""
The session is your “handle” to talk to the database.
"""
# CREATE A SESSION OBJECT TO INITIATE QUERY 
# IN DATABASE
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

if not session.query(Students).first():
    print("Adding data to the Students table...")
    # Add some data
    Students_1 = Students(first_name='John', last_name='Doe', course='Math', score=85.5)
    Students_2 = Students(first_name='Jane', last_name='Smith', course='Science', score=92.0)
    Students_3 = Students(first_name='Alice', last_name='Johnson', course='History', score=78.0)
    Students_4 = Students(first_name='Bob', last_name='Brown', course='Math', score=88.5)

    session.add_all([Students_1, Students_2, Students_3, Students_4])
    session.commit()

else:
    print("Data already exists in the Students table.")
# VIEW THE ENTRIES IN THE RESULT

#SELECT first_name FROM Students
result = session.query(Students.first_name)#.all()
print("Query 1:", result)

# add columns to the query
result = result.add_columns(Students.last_name, 
                            Students.course, Students.score)
print("Query 2:", result)

for r in result:
    print(r.first_name, "|", r.last_name, "|", r.course, "|", r.score)

## count()
"""
The count() method is a synonym to the COUNT we use in the SQL queries. It returns the number of records present in the table
Syntax: sqlalchemy.orm.Query.count()
Return a count of rows this the SQL formed by this Query would return.
"""
count=session.query(Students).count() 
print("Count:", count)
# SELECT COUNT(*) FROM Students

# COUNt only math students
math_count = session.query(Students).filter(Students.course=="Math").count()
print("Math Count:", math_count)
#select count(*) from students where course="Math";

## distinct()
"""
It will return the distinct records based on the provided column names as a reference
Syntax: sqlalchemy.orm.Query.distinct(*expr)


Apply a DISTINCT to the query and return the newly resulting Query.
"""
# SELECT DISTINCT(first_name) FROM students;
result = session.query(Students).with_entities(
    db.distinct(Students.first_name)).all()

for r in result:
    print("Distinct First Names:", r)

## delete()
"""
The delete() method is used to delete records from a table.
Syntax: sqlalchemy.orm.Query.delete(synchronize_session='evaluate')
"""
# DELETE FROM Students WHERE first_name='John' AND last_name='Doe';
result=session.query(
    Students
).filter(Students.first_name=='John', Students.last_name=='Doe').delete(synchronize_session=False)

print("Rows deleted:", result)
result=session.query(Students).count()
print("Count after delete:", result)

## filter()
"""
The filter() method works like the WHERE clause in SQL.
"""

# SELECT * FROM Students WHERE score > 80;
result=session.query(Students).filter(Students.score>80).all()
for r in result:
    print("Score > 80:", r.first_name, r.last_name, r.course, r.score)

# SELECT first_name, last_name, SUM(score)
# AS total FROM students GROUP BY first_name, last_name;
result = session.query(Students) \
    .with_entities(
        Students.first_name,
        Students.last_name,
        db.func.sum(Students.score).label('total')
).group_by(
        Students.first_name,
        Students.last_name
).all()

# VIEW THE ENTRIES IN THE RESULT
for r in result:
    print(r.first_name, r.last_name, "| Score =", r[2])


# SELECT * FROM students ORDER BY score DESC, course;
result = session.query(Students) \
    .order_by(
        Students.score.desc(),
        Students.course
).all()

# VIEW THE ENTRIES IN THE RESULT
for r in result:
    print(r.first_name, r.last_name, r.course, r.score)


# join()
"""
The join() method is used to combine rows from two or more tables based on a related column between them.
"""

class Email(Base):
    __tablename__ = 'Email'

    email = db.Column(db.String(50), primary_key=True)
    first_name = db.Column(db.String(100))


# Check if Email table has data
if not session.query(Email).first():
    print("Adding data to the Email table...")
    email_1 = Email(email='john.doe@example.com', first_name='John')
    email_2 = Email(email='jane.smith@example.com', first_name='Jane')
    email_3 = Email(email='alice.johnson@example.com', first_name='Alice')
    session.add_all([email_1, email_2, email_3])
    session.commit()
else:
    print("Data already exists in the Email table.")

result = session.query(
    Students.first_name,
    Students.last_name,
    Email.email
).join(
    Email, Students.first_name == Email.first_name
)

print("Query:", result)
print()

for r in result:
    print(r.email, "|", r.first_name, r.last_name)

