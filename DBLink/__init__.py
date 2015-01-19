from sqlalchemy import Column

#try to add TableControl to the pyForms controls


import pyForms

from . import TableControl
pyForms.registerControl("DBLink:Table", TableControl.Control)

from . import RowControl
pyForms.registerControl("DBLink:Row", RowControl.Control)