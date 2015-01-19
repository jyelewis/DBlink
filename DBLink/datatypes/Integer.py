from sqlalchemy import Integer as rawInteger

from ..EditControl import EditControlBase
from ..Datatype import DatatypeBase
import pyForms.parser

class StringEditControl(EditControlBase):
	def __init__(self, obj, cellValue):
		super().__init__(obj, cellValue)
		self.children = pyForms.parser.parse("""
			<textbox server placeholder="Integer" />
			<validator:range server>Please enter a valid integer</validator:range>
		""", self.pageInstance)
		self.textbox = self.children[1]
		self.rangeValidator = self.children[3]
		self.rangeValidator.control = self.textbox
		try:
			self.textbox.text = int(self.cellValue)
		except:
			self.textbox.text = ""

	def onRequest(self):
		super().onRequest()
		try:
			self.cellValue = int(self.textbox.text)
		except:
			pass
			
class Integer(rawInteger, DatatypeBase):
	EditControl = StringEditControl
