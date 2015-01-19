from sqlalchemy import ForeignKey as rawForeignKey

class ForeignKey(rawForeignKey):
	def renderEdit(self):
		return "render edit called on FK"