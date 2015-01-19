import pyForms
from database import db, Member, Post

class controller(pyForms.PageController):
	def setHTMLFile(self):
		self.HTMLFile = "webpages/index.html"

	def onInit(self, ctrls):
		pass

	def onLoad(self, ctrls):
		pass


	def onPrerender(self, ctrls):
		ctrls.lpMembers.dataSource = db.query(Member)


	def lpMembers_configureLoop(self, ctrls, loopCtrls, item, index):
		loopCtrls.pMemberName.innerHTML = item.fullname + " (" + str(item.age) + ")"
		def deleteHandler():
			member = db.query(Member).filter(Member.MemberID == item.MemberID).one()
			db.delete(member)
			db.commit()

		def viewHandler():
			member = db.query(Member).filter(Member.MemberID == item.MemberID).one()
			ctrls.pnlMembers.visible = False
			ctrls.pnlPosts.visible = True
			ctrls.h1MemberName.innerHTML = member.fullname
			print(member.posts)

		loopCtrls.btnDelete.clickHandler = deleteHandler
		loopCtrls.btnView.clickHandler = viewHandler

	def btnNewMember_click(self, ctrls):
		newMember = Member(fullname=ctrls.tbxName.text, age=int(ctrls.tbxAge.text))
		db.add(newMember)
		db.commit()

		ctrls.tbxName.text = ""
		ctrls.tbxAge.text  = ""





