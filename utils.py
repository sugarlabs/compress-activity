#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  utils.py
#  
#  Copyright 2012 Rafael Cordano <rafael.cordano@gmail.com>
#  Copyright 2012 Ignacio Rodríguez <nachoel01@gmail.com>
#  Copyright 2012 Ezequiel Pereira <eze2307@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import zipfile,gtk
import utils,commands
from sugar.graphics.toolbutton import ToolButton
import os, shutil
from gettext import gettext as _
try:
	os.mkdir('/tmp/Compress')
	os.mkdir('/tmp/Compress/Work')
except:
	pass
Archivos = None
Archivo_d = None
Dir = False
DirName = None
def Descomprimir(Archivo):
	pass
	
class Abrir():
	def __init__(self,box,texto):
		Ventana = gtk.FileChooserDialog("Abrir..",
     			None,
			gtk.FILE_CHOOSER_ACTION_OPEN,
			(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
			gtk.STOCK_OK, gtk.RESPONSE_OK))

		Ventana.set_default_response(gtk.RESPONSE_OK)

		Filtro = gtk.FileFilter()
		Filtro.set_name("Archivos ZIP")
		Filtro.add_pattern("*.zip")
		Ventana.add_filter(Filtro)

		Echo = Ventana.run()
		if Echo == gtk.RESPONSE_OK:
			File = Ventana.get_filename()
			utils.Archivo_d = File
			try:
				decompress(File,box)
				os.chdir('/tmp/Compress/Work')
				Ventana.destroy()
			except:
				Ventana.destroy()
			
		elif Echo == gtk.RESPONSE_CANCEL:
	    		Ventana.destroy()


class Abrir_Directorio():
	def __init__(self,widget,texto,files,estado,box):
		Ventana = gtk.FileSelection("Abrir..")

		Ventana.set_default_response(gtk.RESPONSE_OK)

		Estado = estado
		Echo = Ventana.run()
		if Echo == gtk.RESPONSE_OK:
			File = Ventana.get_filename()
			Ventana.destroy()
			texto.set_text(File)
			texto.show()
			estado = False
		elif Echo == gtk.RESPONSE_CANCEL:
			box.hide()
			Ventana.destroy()
#COPIADO DE JAMEDIA - FLAVIO DANESSE #
def describe_archivo(archivo):
    """ Devuelve el tipo de un archivo (imagen, video, texto).
    -z, --uncompress para ver dentro de los zip."""
    
    datos = commands.getoutput('file -b  %s%s%s' % ("\"", archivo, "\""))
    datostr = str(datos)
    final = datostr.lower()
    return final
# Esto ya no es parte de jamedia#
def describe_mime(archivo):
	datos = commands.getoutput('file  --mime-type -b %s%s%s' % ("\"", archivo, "\""))
	return str(datos)

def Boton(tooltip=None,icon=None,connect=None):
	if icon != None:
		Boton = ToolButton(icon)
	else:
		Boton = ToolButton('gtk-missing-image')
	if tooltip != None:
		Boton.set_tooltip(tooltip)
	if connect != None:
		Boton.connect("clicked",connect)
	return Boton
def decompress(archivo,box, destino='/tmp/Compress/Work',estado='Abrir',diario=False):
	Archivod = os.getcwd()+"/"+archivo
	# PARTE CONFUSA #
	if not diario:
		Mensaje = _("""Ups! Parece que el archivo esta dañado.O no es un zip ..Porfavor intente con otro""")
	else:
		Mensaje = _("""Oh..Parece que no selecciono un archivo zip""")
	# SI EL ESTADO ES ABRIR BORRA LOS DIRECTORIOS #
	if estado == 'Abrir':
		shutil.rmtree(destino)
		os.mkdir(destino)
	else:
		pass
	# ACA ABRE #
	archivo = open(archivo)
	try:
		zipped = zipfile.ZipFile(archivo)
	except zipfile.BadZipfile:		
		info = gtk.MessageDialog(type=gtk.MESSAGE_WARNING, buttons=gtk.BUTTONS_OK,message_format=Mensaje)
		a = info.run()
		if a == gtk.RESPONSE_OK:
			info.destroy()
			box.hide()
	try:
			zipped.extractall(destino)
			os.chdir(destino)
	
	except RuntimeError:
		info = gtk.MessageDialog(type=gtk.MESSAGE_WARNING, buttons=gtk.BUTTONS_OK,message_format=_("Archivos con contraseña aún no han sido implementados"))
		a = info.run()
		if a == gtk.RESPONSE_OK:
			info.destroy()
	
def compress(archivos_a_meter, archivo):
	zipped = zipfile.ZipFile(archivo, mode='a')
	# VARIOS ARCHIVOS #
	if os.path.isdir(os.getcwd()+"/"+archivos_a_meter):
		zipped = directory("./"+archivos_a_meter, zipped)
	else:
		zipped.write(archivos_a_meter)
def directory(dirname, zipped):
	for x in os.listdir(dirname):
		zipped.write(dirname+"/"+x)
	if os.path.isdir(dirname+"/"+x):
		zipped = directory(dirname+"/"+x, zipped)
	return zipped
