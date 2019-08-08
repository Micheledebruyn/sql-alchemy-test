import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///:memory:', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class User(Base):
     __tablename__ = 'users'

     id = Column(Integer, primary_key=True)
     name = Column(String)
     fullname = Column(String)
     nickname = Column(String)

     def __repr__(self):
        return "<User(name='%s', fullname='%s', nickname='%s')>" % (
                             self.name, self.fullname, self.nickname)

Base.metadata.create_all(engine) # This creates the tables in DB

session = Session()
ed_user = User(name='ed', fullname='Ed Jones', nickname='edsnickname') # create an object with a state of transient
inspect = inspect(ed_user)

session.add(ed_user) # Add that object to the session, state of pending
session.add_all([
    User(name='wendy', fullname='Wendy Williams', nickname='windy'),
    User(name='mary', fullname='Mary Contrary', nickname='mary'),
    User(name='fred', fullname='Fred Flintstone', nickname='freddy')]) # Add objects to the session, state of pending

ed_user.nickname = 'eddie' # Change value on pending object

# print(session.dirty) # Show instances that have been changed
# print(session.new) # Show objects that are pending
#
session.commit() # It flushes to the database and turns the state of the objects into persistent

our_user = session.query(User).filter_by(name='ed').first() # Query object is created on session
