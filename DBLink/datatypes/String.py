from sqlalchemy import String as rawString

from ..EditControl import EditControlBase
from ..Datatype import DatatypeBase
import pyForms.parser

class StringEditControl(EditControlBase):
	def __init__(self, obj, cellValue):
		super().__init__(obj, cellValue)
		self.children = pyForms.parser.parse('<textbox server placeholder="String" />', self.pageInstance)
		self.textbox = self.children[0]
		if self.cellValue is not None:
			self.textbox.text = self.cellValue
		else:
			self.textbox.text = ""

	def onRequest(self):
		super().onRequest()
		self.cellValue = self.textbox.text

class String(rawString, DatatypeBase):
	EditControl = StringEditControl


