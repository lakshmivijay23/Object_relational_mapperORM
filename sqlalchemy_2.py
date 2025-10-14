from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String


engine=create_engine(
    'postgresql+psycopg2://postgres:postgres@localhost:5432/mydb', echo=True
)

meta=MetaData()

people=Table(
    "people",
    meta,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column ('age', Integer))


meta.create_all(engine)

conn=engine.connect()
select_statement=people.select().where(people.c.age>20)
update_statement=people.update().where(people.c.name=="Mike").values(age=50)

result=conn.execute(select_statement)

for row in result.fetchall():
    print(row)






