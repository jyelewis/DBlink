import pyForms.ControlBase
import pyForms.PageControllerClasses

class Control(pyForms.ControlBase.Base):
	def __init__(self, obj):
		super().__init__(obj)
		if not issubclass(self.pageInstance.page.clsController, pyForms.PageControllerClasses.TemplateController):
			raise Exception("content control in non template")
			return

	def render(self):
		#render the innerObj
		return self.pageInstance.page.innerPageInstance.renderRequest(self.pageInstance.request, self.pageInstance.response)