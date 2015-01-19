from DBLink.datatypes import String, Integer, ForeignKey

from sqlalchemy import Column
import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.declarative

engine = sqlalchemy.create_engine("sqlite:///test.db", echo=False)
db = sqlalchemy.orm.Session(bind=engine)
DBBase = sqlalchemy.ext.declarative.declarative_base()


class Member(DBBase):
	__tablename__ = "members"

	MemberID = Column(Integer, primary_key=True)
	fullname = Column(String)
	age = Column(Integer)
	posts = sqlalchemy.orm.relationship("Post")


class Post(DBBase):
	__tablename__ = "posts"

	PostID = Column(Integer, primary_key=True)
	text = Column(String)
	MemberID = Column(Integer, ForeignKey('members.MemberID'))
	


DBBase.metadata.create_all(engine) #create tables

#newPost = Post(text="This is a test post", MemberID=1)