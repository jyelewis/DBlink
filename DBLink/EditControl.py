import pyForms.ControlBase
import cgi

class EditControlBase(pyForms.ControlBase.Base):
	def __init__(self, obj, cellValue):
		super().__init__(obj)
		self.cellValue = cellValue

	def render(self):
		return "".join([x.render() for x in self.children])