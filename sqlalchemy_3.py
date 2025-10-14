
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

# count()
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
