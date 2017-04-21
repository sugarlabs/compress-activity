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
try:
	from Compress import *
	import utils3 as utils
	import shutil,os,pygtk
	from gi.repository import Gtk,Gdk,GdkPixbuf
	from sugar3.graphics.objectchooser import ObjectChooser
	from sugar3.datastore import datastore
	shutil.rmtree('/tmp/Compress')
	os.mkdir('/tmp/Compress')
	os.mkdir('/tmp/Compress/Work')
except:
	pass
from gettext import gettext as _
Archivo = None
# CONSTANTES #
Directorio = _("Nuevo directorio")
Hboxx = Gtk.HBox()
Uri = Gtk.Entry()
Uri.set_text(os.getcwd())
Uri.props.secondary_icon_stock = 'gtk-apply'
Uri.props.secondary_icon_activatable = True
Estado = False
entrada = Gtk.Entry()
entrada.props.secondary_icon_stock = 'gtk-apply'
entrada.props.secondary_icon_activatable = True
botons = Gtk.Button(Gtk.STOCK_OK)
save = utils.Boton(_('Guardar archivo'),'document-save')
entrada.set_text(_("Para que los cambios se guarden presione la tecla '↵' o el icono √ "))
###

class Canvas(Gtk.TreeView):
	def __init__(self):
		
		self.modelo = None
		self.treeview_arbol = None
		self.barra_de_estado = None
		Gtk.TreeView.__init__(self)
		try:
			Home.connect('clicked',self.home)
			Abrir.connect('clicked',self.open,True)		
			Arriba.connect('clicked',self.back)
			save.connect('clicked',self.copiar_al_diario)
#			open_from_journal.connect('clicked',self.open_diario)
			Add.connect('clicked',self.anadir)
		except:
			pass
	        Uri.connect('activate',self.change)
	        Uri.connect("icon-press", self.change)
		self.set_tooltip_text(_('Archivos en el directorio'))
		self.set_property("rules-hint", True)
		entrada.connect('icon-press',self.update,entrada)
		entrada.connect('activate',self.update_e,entrada)
		
		self.Copiado = None
		self.modelo = self.construir_lista()
		self.construir_columnas()
		self.seleccion = self.get_selection() # treeview.get_selection()
		self.seleccion.set_mode(Gtk.SelectionMode.SINGLE)
		self.seleccion.set_select_function(self.archivo_clickeado, self.modelo)
		self.connect("row-activated", self.doble_click)
		self.connect('button-release-event', self.menu_click)  
		self.connect('key-release-event', self.atras_button)   
		self.set_model(self.modelo)
		self.presentado = False
		self.show_all()
		self.icon_name = None
		if Estado:
			Hboxx.show()
		else:
			Hboxx.hide()
	def update(self,widget,a,b,entrada): # Icono
		botons.connect('clicked',self.descomprimir_final,entrada.get_text())
	def update_e(self,widget,entrada): # Enter en la entrada
		botons.connect('clicked',self.descomprimir_final,entrada.get_text())
	def compress_file(self,widget,archivo): # Comprime un archivo
			utils.compress(utils.Archivos,os.getcwd()+"/"+utils.Archivos+".zip")
			self.set_model(self.construir_lista())
	def open(self,widget,clickeado=False): # Abrir
		if not clickeado:
			try:
				utils.decompress(utils.Archivos,Hboxx,'/tmp/Compress/Work','Abrir')
				utils.Archivo_d = Uri.get_text()+"/"+utils.Archivos
				os.chdir('/tmp/Compress/Work')
			except:
				utils.Abrir(Hboxx,entrada)
		if clickeado:
				utils.Abrir(Hboxx,entrada)
		Uri.set_text(os.getcwd())
		Uri.show()
		self.set_model(self.construir_lista())	
	def archivo_clickeado(self, seleccion, modelo, archivo, seleccionado, a=None): # Cuando se selecciona
		iter= modelo.get_iter(archivo)
		directorio =  modelo.get_value(iter,0)
		utils.Archivos = directorio
		estado = utils.describe_archivo(os.getcwd()+"/"+utils.Archivos)
	
		if 'image' in estado:
			self.icon_name = 'imagen'
			save.set_tooltip(_('Guardar imagen: '+utils.Archivos+' al diario'))
		if 'text' in estado:
			self.icon_name = 'texto'
			save.set_tooltip(_('Guardar texto: '+utils.Archivos+' al diario'))
		if 'audio' in estado:
			self.icon_name = 'audio'
			save.set_tooltip(_('Guardar audio: '+utils.Archivos+' al diario'))

		if 'video' in estado:
			self.icon_name = 'video'
			save.set_tooltip(_('Guardar: '+utils.Archivos+' al diario'))
		if not 'directory' in estado and not 'no read permission' in estado:
			save.set_icon_name(self.icon_name)
			save.show()
		else:
			save.hide()
		return True
	def anadir(self,widget):
		Selector = Gtk.FileChooserDialog(_("Seleccione un archivo"),None,Gtk.FileChooserAction.OPEN,(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,Gtk.STOCK_OK, Gtk.ResponseType.OK))
		Selector.set_default_response(Gtk.ResponseType.CANCEL)
		if utils.Archivo_d != None:
			Echo = Selector.run()
			if Echo == Gtk.ResponseType.OK:
				File = Selector.get_filename()
				print 'ARCHIVO'
				print File
				utils.compress(File,utils.Archivo_d)
				print 'AÑADIDO'
				utils.decompress(utils.Archivo_d,Hboxx)
				print 'DESCOMPRIMIDO'
				Selector.destroy()
			elif Echo == Gtk.ResponseType.CANCEL:
				Selector.destroy()
		if utils.Archivo_d == None:
				self.errores('Copiar_a_nada')
		os.chdir('/tmp/Compress/Work')
		self.set_model(self.construir_lista())
		Uri.set_text(os.getcwd())
		Uri.show()
	def open_diario(self,widget): # Abrir un zip desde el diario.
			chooser = ObjectChooser()      
			resultado = chooser.run()
   			if resultado == Gtk.ResponseType.ACCEPT:
				Archivo_s = chooser.get_selected_object()
				Archivo = Archivo_s.get_file_path()
				try:
					print Archivo
					utils.Archivo_d = Archivo
					utils.decompress(Archivo,Hboxx,'/tmp/Compress/Work','Abrir',True)
		
				except IOError:
					Mensaje = _("""Oh..Parece que no selecciono un archivo zip""")
					info = Gtk.MessageDialog(type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.OK,message_format=Mensaje)
					a = info.run()
					if a == Gtk.ResponseType.OK:
						info.destroy()
						self.set_model(self.construir_lista())
						Uri.set_text(os.getcwd())
	def construir_lista(self):
		store = Gtk.ListStore(str)
		dirList=os.listdir(os.getcwd())
		dircontents = []
		for item in dirList: 
			if item[0] != '.':
				if os.path.isdir(item):
					dircontents.append(['/'+item])
				else:
					dircontents.append([item])
					
		dircontents.sort() 
		for act in dircontents:
			store.append([act[0]])
		return store
	def descomprimir_en(self,widget=None):
		if not self.presentado:
			label = Gtk.Label(_('Carpeta:'))

			#entrada.set_text('/tmp/Compress/Work')
			boton = Gtk.Button(Gtk.STOCK_OPEN)
			botona = Gtk.Button(Gtk.STOCK_CANCEL)
			botona.set_use_stock(True)
			botona.connect('clicked',lambda x:Hboxx.hide())
			boton.set_use_stock(True)
			boton.connect('clicked',utils.Abrir_Directorio,entrada,utils.Archivos,Estado,Hboxx)
			Hboxx.pack_start(label,False,False,0)
			Hboxx.pack_start(entrada,True,True,0)
			Hboxx.pack_start(boton,False,False,0)
			botons.set_use_stock(True)
			Hboxx.pack_start(botons,False,False,0)
			Hboxx.pack_start(botona,False,False,0)
			
			Hboxx.show_all()
			self.presentado = True
		else:
			Hboxx.show_all()
	def descomprimir_final(self,widget,dire):
		utils.decompress(utils.Archivos,Hboxx,dire,'Descomprimir')
		Hboxx.hide()
		os.chdir(dire)
		Uri.set_text(os.getcwd())
		Uri.show()
		self.set_model(self.construir_lista())
	def descomprimir(self,widget):
		self.descomprimir_en()
		Estado = True
	def construir_columnas(self):
		columna= Gtk.TreeViewColumn(_('Archivos en el directorio'))
		celda_de_texto = Gtk.CellRendererText() # para el texto
		columna.pack_start(celda_de_texto, True)
		self.append_column (columna)
		columna.set_attributes(celda_de_texto, text=0)
	def doble_click(self, widget, row, col): # Clickeado
		model = widget.get_model()
		target = model[row][0]
		Archivo = utils.describe_archivo(os.getcwd()+"/"+utils.Archivos)
		if target[0] != "/":
				utils.Archivos = target
				ventana = Gtk.Window()
				ventana.set_title(target)																									
				ventana.connect('destroy',lambda x: ventana.destroy)
				if 'image' in Archivo:
					try:
						pix = GdkPixbuf.Pixbuf.new_from_file(target)
						image = Gtk.Image()
						image.set_from_pixbuf(pix)
						ventana.add(image)
						image.show()
						ventana.show()
					except IOError:
						self.ops(_('imagen'))
				if not 'binary' in Archivo:
					try:
						ventana.set_size_request(Gdk.Screen.width()/2,Gdk.Screen.height()/2)
						texta = Gtk.ScrolledWindow()
						texs = Gtk.TextBuffer()
						text = Gtk.TextView()
						text.set_buffer(texs)
						texta.add(text)
						text.set_editable(False)
						texs.set_text(open(target).read())
						ventana.add(texta)
						ventana.show_all()
					except IOError:
						self.ops(_('archivo'))
		else:
			try:
				os.chdir(os.getcwd()+target)
				self.set_model(self.construir_lista())
			except:
				self.ops(_('directorio'))
			Uri.set_text(os.getcwd())
			Uri.show()
	def create_columns(self, treeView):
		rendererText = Gtk.CellRendererText()
		img = celda_de_imagen = Gtk.CellRendererPixbuf()
		column = Gtk.TreeViewColumn(_('Archivos en el directorio'))
		column.set_sort_column_id(0)
		column.pack_start(rendererText,False)    
		column.set_attributes(rendererText, text=0)
		self.append_column(column)     
	def close(self,widget):
		shutil.rmtree('/tmp/Compress/Work')
		os.mkdir('/tmp/Compress/Work')
		utils.Archivo_d = None
		self.set_model(self.construir_lista())
	def menu_click(self,widget,event):
		Boton = event.button
		Tiempo = event.time
		Menu = Gtk.Menu()
		Archivo = utils.describe_archivo(os.getcwd()+"/"+utils.Archivos)
		if Boton == 3:
			if utils.Archivo_d == None:
				if 'zip' in Archivo:
					Abrir = Gtk.MenuItem(_('Abrir zip'))
					Abrir.connect('activate',self.open)
					Menu.append(Abrir)
				else:
					pass
			else:
				Close = Gtk.MenuItem(_('Cerrar zip:  %s'%utils.Archivo_d))
				Close.connect('activate',self.close)
				Menu.append(Close)
			Menu.append(Gtk.SeparatorMenuItem())
			Copy = Gtk.MenuItem(_('Copiar'))
			Copy.connect('activate',self.copy)
			if 'zip' in Archivo:
				Des = Gtk.MenuItem(_('Descomprimir'))
				Des.connect('activate',self.descomprimir)
			Cut = Gtk.MenuItem(_('Cortar'))
			Cut.connect('activate',self.cut)
			Delete = Gtk.MenuItem(_('Borrar'))
			Delete.connect('activate',self.sure)
			CompressFile= Gtk.MenuItem(_('Comprimir este archivo'))
			CompressFile.connect('activate',self.compress_file,utils.Archivos)
			Menu.append(CompressFile)
			try:
				Menu.append(Des)
			except:
				pass
			Menu.append(Gtk.SeparatorMenuItem())
			if utils.Archivo_d != None:
				Copyw = Gtk.MenuItem(_('Copiar al zip'))
				Copyw.connect('activate',self.copy,True)
				Menu.append(Copyw)
			Menu.append(Copy)
			
			Menu.append(Cut)
			Back = Gtk.MenuItem(_('Atras'))
			Back.connect('activate',self.back)
			if os.listdir('/tmp/Compress/') != ['Work']:
				Paste = Gtk.MenuItem(_('Pegar'))
				Paste.connect('activate',self.paste)
				Menu.append(Paste)
			Menu.append(Gtk.SeparatorMenuItem())
			Menu.append(Delete)
			Menu.append(Back)
			Menu.show_all()
			Menu.popup(None, None, None, None,Boton, Tiempo)
	def atras_button(self,widget,event):
		Boton = event.keyval
		if Boton == 65288:
			self.back()
		if Boton == 65535: # Solo existe en la 1.5 y en las magallanes
			self.sure()
	def delete(self,widget=None):
		try:
			try:
				os.remove(os.getcwd()+"/"+utils.Archivos)
			except:
				shutil.rmtree(os.getcwd()+utils.Archivos)
		except:
			self.errores('Desconocido')

		self.set_model(self.construir_lista())
	def cut(self,widget):
		try:
			self.Copiado = utils.Archivos
#			os.system('mv '+ os.getcwd()+"/"+utils.Archivos+" "+'/tmp/Compress/'+utils.Archivos)
			shutil.move(os.getcwd()+"/"+utils.Archivos,'/tmp/Compress/'+utils.Archivos)
			self.set_model(self.construir_lista())
		except:
			self.errores('Cortar')
	def paste(self,widget):
		try:
			
			#os.system('mv /tmp/Compress/'+self.Copiado+" " + os.getcwd()+"/")
			shutil.move('/tmp/Compress/'+self.Copiado,os.getcwd()+"/")			
			self.set_model(self.construir_lista())
		except:
			List = os.listdir('/tmp/Compress')
			if List == ['Work']:
				self.errores("Pegar_None")
			else:
				self.errores('Pegar')
	def back(self,widget=None):
		os.chdir(os.getcwd()+"/..")
		self.set_model(self.construir_lista())
		Uri.set_text(os.getcwd())
		Uri.show()
	def change(self,widget,a=None,b=None):
		try:
			os.chdir(widget.get_text())
			self.set_model(self.construir_lista())
		except:
			self.ops(_('directorio'))
	def copy(self,widget,W=False):
		try:
			self.Copiado = utils.Archivos
			if not W:
				try:
					shutil.copy(os.getcwd()+"/"+utils.Archivos,'/tmp/Compress/')
				except:
					shutil.copytree(os.getcwd()+"/"+utils.Archivos,'/tmp/Compress/'+utils.Archivos)
				
			if W:
				try:
					utils.compress("./"+utils.Archivos,utils.Archivo_d)
					utils.decompress(utils.Archivo_d,Hboxx)
					
				except:
					self.errores('Copiar_a_nada')
			
		except:
			self.errores('Copiar')
	def sure(self,widget=None):
		info = Gtk.MessageDialog(type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.YES_NO,
			message_format=_("Seguro que desea borrar el archivo: %s" %utils.Archivos))
		respuesta = info.run()
		if respuesta == Gtk.ResponseType.YES:
			self.delete()
			info.destroy()
		else:
			info.destroy()
	def ops(self,donde):
		info = Gtk.MessageDialog(type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.OK,
			message_format=_("Error al acceder al "+donde+" razón:\n%s" %self.razon(str(Uri.get_text()),donde)))
		respuesta = info.run()
		if respuesta == Gtk.ResponseType.OK:
			Ant = os.getcwd()
			os.chdir(Ant)
			Uri.set_text(os.getcwd())
			Uri.show()
			info.destroy()
	def razon(self,directorio,razon):
		if not os.path.exists(directorio):
			return _("El "+razon+" no existe")
		else:
			try:
				open(directorio)
			except:
				return _("No tiene acceso a ese "+razon )
		try:
			open(directorio+"/")
		except:
			return _(directorio+" no es un directorio")
	def home(self,widget=None):
		os.chdir('/tmp/Compress/Work')
		Uri.set_text(os.getcwd())
		Uri.show()
		self.set_model(self.construir_lista())
	def copiar_al_diario(self,widget):
		descripcion = utils.describe_archivo(utils.Archivos)
		mime = utils.describe_mime(utils.Archivos)
		if not 'directory' in descripcion:
			acopiar = datastore.create()
			acopiar.metadata['title'] = utils.Archivos
			acopiar.metadata['mime_type'] = mime
			acopiar.set_file_path(os.getcwd()+"/"+utils.Archivos)
			datastore.write(acopiar)
			acopiar.destroy()
	def errores(self,Evento=None):
		if Evento == "Copiar":
			info = Gtk.MessageDialog(type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.OK,message_format=_("Error al intentar copiar: %s "%utils.Archivos))
			a = info.run()
			if a == Gtk.ResponseType.OK:
				info.destroy()
		if Evento == "Cortar":
			info = Gtk.MessageDialog(type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.OK,message_format=_("Error al intentar cortar: %s "%utils.Archivos))
			a = info.run()
			if a == Gtk.ResponseType.OK:
				info.destroy()		
		if Evento == "Pegar_None":
			info = Gtk.MessageDialog(type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.OK,message_format=_("Error: No hay nada en el portapapeles" ))
			a = info.run()
			if a == Gtk.ResponseType.OK:
				info.destroy()	
		if Evento == "Pegar":
			info = Gtk.MessageDialog(type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.OK,message_format=_("Error al intentar pegar un archivo" ))
			a = info.run()
			if a == Gtk.ResponseType.OK:
				info.destroy()	
		if Evento == 'Copiar_a_nada':
			info = Gtk.MessageDialog(type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.OK,message_format=_("¡Ups! Parece que aún no abrio ningun archivo"))
			a = info.run()
			if a == Gtk.ResponseType.OK:
				info.destroy()			
		if Evento == 'Desconocido':
			info = Gtk.MessageDialog(type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.OK,message_format=_("Error desconocido"))
			a = info.run()
			if a == Gtk.ResponseType.OK:
				info.destroy()			
class Canvas_box(Gtk.EventBox):
    def __init__(self):
		Gtk.EventBox.__init__(self)

		vbox = Gtk.VBox(False, 8)
		xhbox = Gtk.HBox()
		sw = Gtk.ScrolledWindow()
		sw.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
		sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

		xhbox.pack_start(Uri,True,True,0)
		hbox = Gtk.HBox()
		vbox.pack_start(xhbox,False,False,0)
		vbox.pack_start(hbox,True,True,0)
		Logo = Gtk.Image()
		Logo.set_from_file('icons/ceibaljam.svg')
		hbox.pack_start(sw, True, True, 0)
		sw.add(Canvas())
		hx = Gtk.HBox()
		Logo2 = Gtk.Image()
		Logo.set_tooltip_text('http://www.ceibaljam.org')
		Logo2.set_from_file('icons/sugarlabs.svg')
		Logo2.set_tooltip_text('http://www.wiki.sugarlabs.org')
		self.add(vbox)
		vbox.pack_start(Hboxx,False,False,0)
		if Gdk.Screen.width() >= 1200:
			vbox.pack_start(hx,False,False,0)
			hx.pack_start(Logo2,True,True,0)		
			hx.pack_start(Logo,True,True,100)
		else:
			Uri.set_size_request(int(Gdk.Screen.width()-157.797),int(45.466))
			Uri.show()
			LogoChico = Gtk.Image()
			LogoChico.set_from_file('icons/ceibaljam_chico.svg')
			
			LogoChico.show()
			xhbox.pack_start(LogoChico,False,False,0)
		self.show_all()
		
if __name__ == "__main__":
	a = Gtk.Window()
	a.add(Canvas_box())
	a.show_all()
	a.set_title('COMPRESS CANVAS GTK3')

	a.connect('destroy',lambda x: Gtk.main_quit())
	a.set_size_request(500,500)
	Gtk.main()
