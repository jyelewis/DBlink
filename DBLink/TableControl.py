import cgi
from sqlalchemy.orm import class_mapper
import pyForms.ControlBase
import pyForms.controlManager
import pyForms.parser


class Control(pyForms.ControlBase.Base):
	def __init__(self, obj):
		super().__init__(obj)

		self._query = None #list of rows
		self.session = None
		self.insertClass = None
		self._queryNeedsInit = True
		self._rows = None
		self._columns = None

		self.customButtons = []
		self.showEditButton = True
		self.showDeleteButton = True

		self._rowEditControl = None
		
		self._returnButton = pyForms.parser.parse('<button server>Return to list</button>', self.pageInstance)[0]
		def returnButtonClickHandler():
			self._rowEditControl = None
		self._returnButton.clickHandler = returnButtonClickHandler

		self._insertButton = pyForms.parser.parse('<button server>Insert new row</button>', self.pageInstance)[0]
		def insertButtonClickHandler():
			newRow = self.insertClass()
			def returnHandler():
				self.session.add(newRow)
				self.session.commit()
				self.reload()
			self.setEdit(newRow, returnHandler)
		self._insertButton.clickHandler = insertButtonClickHandler

	@property
	def query(self):
		return self._query

	@query.setter
	def query(self, newQuery):
		self._query = newQuery
		self._queryNeedsInit = True

	def reload(self):
		self._rows = None
		self._queryNeedsInit = True

	def initQuery(self):
		if self.query is None:
			raise Exception("No query was provided")

		self._rows = []
		for rowData in self.query:
			self._rows.append({
				 'buttons': self._generateButtons(rowData)
				,'obj': rowData})

		self._columns = [] #contains dictionarys {showInList: True, showInEdit: True, showInInsert: True, obj:Object}
		for colClass in self.query.column_descriptions:
			#for now assume colClass is a class
			for column in colClass['expr'].__table__.columns:
				visible = not column.primary_key
				self._columns.append({
					 'showInList':visible
					,'showInEdit':visible
					,'showInInsert':visible
					,'obj':column})

			for column in colClass['expr'].__table__.foreign_keys:
				print("PK found:", column)

		self._queryNeedsInit = False

	@property
	def buttons(self):
		fixedButtons = []

		def delButtonHandler(row):
			self.session.delete(row)
			self.session.commit()
			self.reload()

		if self.showEditButton and self.session is not None:
			fixedButtons.append(("Edit", self.setEdit))
			fixedButtons.append(("Delete", delButtonHandler))
		return fixedButtons + self.customButtons

	def fireEvents(self):
		self._returnButton.fireEvents()
		self._insertButton.fireEvents()

		if self._rowEditControl is not None:
			self._rowEditControl.fireEvents()

		if self._rows is not None:
			for row in self._rows:
				for button in row['buttons']:
					button.fireEvents()

	def onRequest(self):
		self._returnButton.onRequest()
		self._insertButton.onRequest()
		if self._rowEditControl is not None:
			self._rowEditControl.onRequest()

		if self._rows is not None:
			for row in self._rows:
				for button in row['buttons']:
					button.onRequest()

	def _setShow(self, columnToHide, dictKey, newVal):
		for index, column in enumerate(self._columns):
			if column['obj'] == columnToHide:
				column[dictKey] = newVal


	def hideColumnInList(self, col):
		self._setShow(col, 'showInList', False)

	def showColumnInList(self, col):
		self._setShow(col, 'showInList', True)

	def hideColumnOnEdit(self, col):
		self._setShow(col, 'showOnEdit', False)

	def showColumnOnEdit(self, col):
		self._setShow(col, 'showOnEdit', True)

	def hideColumnOnInsert(self, col):
		self._setShow(col, 'showOnInsert', False)

	def showColumnOnInsert(self, col):
		self._setShow(col, 'showOnInsert', True)

	def render(self):
		if self._rowEditControl is not None:
			return self.renderEditView()
		else:
			return self.renderTableView()

	def renderTableView(self):
		#custom render function
		#cgi.escape("str&")

		if self._queryNeedsInit:
			self.initQuery()

		retStr  = '<div class="DBLinkTableView"><table><thead>'
		#column.type.renderEdit()
		retStr += "<tr>"
		for column in self._columns:
			if column['showInList']:
				retStr	+= "<th>" + column['obj'].name + "</th>"

		retStr += "<td>"+ '' +"</td>"
		retStr += "</tr></thead>"

		retStr += "<tbody>"
		for row in self._rows:
			retStr += "<tr>"
			for column in self._columns:
				if column['showInList']:
					retStr += "<td>" + str(column['obj'].type.viewHTML(getattr(row['obj'], column['obj'].name))) + "</td>"

			for button in row['buttons']:
				retStr += "<td>" + button.render() + "</td>"

			retStr += "</tr>"

		
		retStr += '</tbody></table>'
		retStr += self._insertButton.render() + '</div>'


		return retStr

	def renderEditView(self):
		return self._returnButton.render() + self._rowEditControl.render()


	def setEdit(self, row, onReturn = None, isInsert = False):
		self._rowEditControl = pyForms.parser.parse('<DBLink:row server />', self.pageInstance)[0]
		editControl = self._rowEditControl
		editControl.row = row
		showKey = "showInInsert" if isInsert else 'showInEdit'
		for column in self._columns:
			if column[showKey]:
				editControl.showColumn(column['obj'])
			else:
				editControl.hideColumn(column['obj'])

		def returnHandler():
			if onReturn is not None:
				onReturn()
			self._rowEditControl = None
			self.session.commit()
		self._rowEditControl.onSave = returnHandler
		
		self._rowEditControl.session = self.session


	def _generateButtons(self, row):
		retButtons = []
		for buttonInfo in self.buttons:
			newButton = pyForms.parser.parse('<button server>'+buttonInfo[0]+'</button>', self.pageInstance)[0]
			newButton.clickHandler = generateHandler(buttonInfo, row)
			retButtons.append(newButton)
		return retButtons



def generateHandler(buttonInfo, row):
	return lambda: buttonInfo[1](row)







