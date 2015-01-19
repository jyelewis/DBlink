import cgi
from sqlalchemy.orm import class_mapper
import pyForms.ControlBase
import pyForms.parser

class Control(pyForms.ControlBase.Base):
	def __init__(self, obj):
		self._row = None
		self.session = None

		super().__init__(obj)

		self.saveButton = pyForms.parser.parse("<button server causesValidation>Save</button>", self.pageInstance)[0]
		self.saveButton.clickHandler = self.btnSave_click

		self._formControl = None
		self._editControls = [] # (columnname, editControlObj)

		self.onSave = None

		self.hiddenColumns = {}

	@property
	def row(self):
		return self._row

	@row.setter
	def row(self, newVal):
		self._row = newVal

		#init row
		self.hiddenColumns = {}
		for column in newVal.__table__.columns:
			if column.primary_key:
				self.hiddenColumns[column.name] = True

	def hideColumn(self, col):
		self.hiddenColumns[col.name] = True

	def showColumn(self, col):
		if col.name in self.hiddenColumns:
			del self.hiddenColumns[col.name]

	def fireEvents(self):
		self.saveButton.fireEvents()
		for editControl in self._editControls:
			editControl[1].fireEvents()

	def onRequest(self):
		self.saveButton.onRequest()
		for editControl in self._editControls:
			editControl[1].onRequest()

	def btnSave_click(self):
		for editControl in self._editControls:
			setattr(self.row, editControl[0], editControl[1].cellValue)

		if self.onSave is not None:
			self.onSave()


	def initEditControls(self):
		validatorGroupControl = pyForms.parser.parse('<validationGroup server></validationGroup>', self.pageInstance)[0]
		self._editControls = []
		for column in self.row.__table__.columns:
			print(column)
			if column.name not in self.hiddenColumns:
				tableRowControl = pyForms.parser.parse("<tr><td>"+ column.name +"</td></tr>", self.pageInstance)[0]
				
				tdControl = pyForms.parser.parse('<td></td>', self.pageInstance)[0]

				editControl = column.type.EditControl({
					'name': ''
					,'attrs': {}
					,'startContentsPos': None
					,'endContentsPos': None
					,'innerHTML': None
					,'isSelfClosing': None
					,'pageInstance': self.pageInstance
					,'customRegisterFunction': lambda x: None
				}, getattr(self.row, column.name))
				self._editControls.append((column.name, editControl))

				tdControl.children = [editControl]
				tableRowControl.children.append(tdControl)
				
				validatorGroupControl.children.append(tableRowControl)
		
		buttonRow = pyForms.parser.parse("<tr><td>&nbsp;</td><td></td></tr>", self.pageInstance)[0]
		buttonRow.children[1].children.append(self.saveButton)
		
		validatorGroupControl.children.append(buttonRow)
		self._formControl = validatorGroupControl



	def render(self):
		if self.row is None:
			raise Exception("Row never defined")

		if self.session is None:
			raise Exception("session never defined")

		if self._formControl is None:
			self.initEditControls()
		
		retStr  = '<div class="DBLinkEditView"><table><thead>'
		retStr += "<tr><td></td><td></td></tr></thead>" #two columns in head

		retStr += "<tbody>"

		retStr += self._formControl.render()
		retStr += '</tbody></table></div>'

		return retStr


