from database import db, Member, Post
import pyForms

class controller(pyForms.PageController):
	def setHTMLFile(self):
		self.HTMLFile = "webpages/control.html"

	def onInit(self, ctrls):
		
		#ctrls.tblTest.session = db
		#ctrls.tblTest.insertClass = Member
		#ctrls.tblTest.query = db.query(Member).order_by(Member.age)

		ctrls.tblTest.session = db
		ctrls.tblTest.insertClass = Post
		ctrls.tblTest.query = db.query(Post)

		#ctrls.rowTest.session = db
		#ctrls.rowTest.row = db.query(Member).filter(Member.age == 17).first()
		#ctrls.rowTest.showColumn(Member.MemberID)
		#ctrls.rowTest.hideColumn(Member.fullname)