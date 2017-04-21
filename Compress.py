#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Ignacio Rodríguez <nachoel01@gmail.com>
# Rafael Cordano <rafael.cordano@gmail.com>
# Ezequiel Pereira <eze2307@gmail.com>
 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
try: # gtk3
	from sugar30.activity import activity
	from sugar3.activity.widgets import StopButton
	from sugar3.activity.widgets import ActivityToolbarButton
	from sugar3.graphics.toolbutton import ToolButton
	from sugar3.graphics.toolbarbox import ToolbarBox
	from gettext import gettext as _    # Traduccion
	import utils3 as utils
	from utils3 import Boton
	from gi.repository import Gtk
	Abrir = Boton(_("Abrir"),"Abrir")      
	Arriba = Boton(_('Arriba'),'up')
	Home = Boton(_('Directorio Zip'),'gtk-home')
	#open_from_journal = Boton(_("Open from journal"),"open-from-journal")
	Add = Boton(_('Añadir archivo'),"add")
	save  = Boton(_('Guardar archivo:'))
	Barra = ToolbarBox()
	from CompressCanvas3 import Canvas_box as PyApp
	from CompressCanvas3 import *
	class Compress(activity.Activity):
			def __init__(self, handle):
				activity.Activity.__init__(self, handle, True)
				canvas = PyApp()
				Actividad = ActivityToolbarButton(self)
				Parar = StopButton(self)
				Parar.set_tooltip(_('Parar - Gtk3'))
				#<-------------Separadores------------->#
				Separador = Gtk.SeparatorToolItem()
				Separador2  = Gtk.SeparatorToolItem()
				Separador3 = Gtk.SeparatorToolItem()
				Separador3.set_expand(True)
				Separador3.props.draw = False
				Barra.toolbar.insert(Actividad, 0)      
				Barra.toolbar.insert(Separador2, 1)
				Barra.toolbar.insert(Add, 2)
				Barra.toolbar.insert(Home,3)  
				Barra.toolbar.insert(Arriba,4)
				Barra.toolbar.insert(Separador3, 5)
				Barra.toolbar.insert(Abrir, 6) 
				Barra.toolbar.insert(save,7)     
				Barra.toolbar.insert(Separador3, 8)
				Barra.toolbar.insert(Parar, 9) 
	
				self.set_toolbar_box(Barra) # Barra
				self.set_canvas(canvas)
				self.show_all()
				save.hide()
except ImportError:
	import gtk
	from sugar.activity import activity
	from sugar.activity.widgets import StopButton
	from sugar.activity.widgets import ActivityToolbarButton
	from sugar.graphics.toolbutton import ToolButton
	from sugar.graphics.toolbarbox import ToolbarBox
	from gettext import gettext as _    # Traduccion
	import utils
	from utils import Boton
	Abrir = Boton(_("Abrir"),"Abrir")      
	Arriba = Boton(_('Arriba'),'up')
	Home = Boton(_('Directorio Zip'),'gtk-home')
	#open_from_journal = Boton(_("Open from journal"),"open-from-journal")
	Add = Boton(_('Añadir archivo'),"add")
	save  = Boton(_('Guardar archivo:'))
	Barra = ToolbarBox()
	from CompressCanvas import Canvas_box as PyApp
	from CompressCanvas import *
	class Compress(activity.Activity):
			def __init__(self, handle):
				activity.Activity.__init__(self, handle, True)
				canvas = PyApp()
				Actividad = ActivityToolbarButton(self)
				Parar = StopButton(self)
				Parar.set_tooltip(_('Parar - Gtk2'))
				#<-------------Separadores------------->#
				Separador = gtk.SeparatorToolItem()
				Separador2  = gtk.SeparatorToolItem()
				Separador3 = gtk.SeparatorToolItem()
				Separador3.set_expand(True)
				Separador3.props.draw = False
				Barra.toolbar.insert(Actividad, 0)      
				Barra.toolbar.insert(Separador2, 1)
				Barra.toolbar.insert(Add, 2)
				Barra.toolbar.insert(Home,3)  
				Barra.toolbar.insert(Arriba,4)
				Barra.toolbar.insert(Separador3, 5)
				Barra.toolbar.insert(Abrir, 6) 
				Barra.toolbar.insert(save,7)     
				Barra.toolbar.insert(Separador3, 8)
				Barra.toolbar.insert(Parar, 9) 
	
				self.set_toolbar_box(Barra) # Barra
				self.set_canvas(canvas)
				self.show_all()
				save.hide()


 
