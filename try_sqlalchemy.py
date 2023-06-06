from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Person(Base):
  __tablename__ = "people"
  
  ssn = Column("ssn", Integer, primary_key=True)
  firstname = Column("firstname", String, unique=True, nullable=False)
  lastname = Column("lastname", String)
  gender = Column("gender", CHAR)
  age = Column("age", Integer)

  def __init__(self, ssn, firstname, lastname, gender, age):
    self.ssn = ssn
    self.firstname = firstname
    self.lastname = lastname
    self.gender = gender
    self.age = age
 
  def __repr__(self):
    return f'{self.ssn} : {self.firstname}'


class Thing(Base):
  __tablename__ = "things"
  
  tid = Column("tid", Integer, primary_key=True)
  description = Column("description", String)
  owner = Column(Integer, ForeignKey("people.ssn"))

  def __init__(self, tid, description, owner):
    self.tid = tid
    self.description = description
    self.owner = owner

  
  def __repr__(self):
    return f'({self.tid}) [{self.description}] owned by {self.owner}'

# Create engine for sqlite database
engine = create_engine("sqlite:///mydb.db", echo=True)

# Takes all the classes and creats them into database
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine) 
session = Session() # create Session instance

p1 = Person(1234, "Chala", "Geme", "m", 23)
p2 = Person(1233, "Mana", "Tassa", "f", 34)

session.add(p1)
session.add(p2)
session.commit()

session.add(Thing(1, "Car", p1.ssn))
session.add(Thing(2, "Houese", p2.ssn))
session.commit()
# results = session.query(Person).filter(Person.age > 20)
# results = session.query(Person).filter(Person.firstname.like("%na%"))
results = session.query(Person).filter(Person.firstname.in_(["Mana", "Chala"]))

# for r in results:
#   print(r)