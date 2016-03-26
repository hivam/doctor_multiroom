# -*- coding: utf-8 -*-
##############################################################################
#
#	OpenERP, Open Source Management Solution
#	Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU Affero General Public License as
#	published by the Free Software Foundation, either version 3 of the
#	License, or (at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU Affero General Public License for more details.
#
#	You should have received a copy of the GNU Affero General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import logging
_logger = logging.getLogger(__name__)
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
from datetime import date, datetime, timedelta

class doctor_room(osv.osv):
	_name = "doctor.room"
	_description = "It allows you to create multiple doctor rooms."

	_columns = {
		'codigo':fields.char('Código', size=3, required=True),
		'name':fields.char('Nombre Consultorio', required='True'),
		'multi_paciente': fields.boolean('Multi Paciente'), 
		'numero_pacientes':fields.integer('Numero de Pacientes',size=2)
	}


	def validar_numero_pacientes(self, cr, uid, ids, context=None):
		numero_pacientes= self.search(cr, uid, [], context=context)
		for pacientes in self.browse(cr, uid, numero_pacientes):
			total_pacientes=pacientes.numero_pacientes
		if total_pacientes > 1:
			return True
		return False

	_sql_constraints = [
		('name_unico','unique(name)', 'Ya existe un consultorio con este mismo nombre.'),
		('codigo_unico','unique(codigo)', u'Ya existe un consultorio con este mismo código.')
	]

	_constraints = [(validar_numero_pacientes, u'El número de pacientes tiene que ser mayor a 1', [u'Número de Pacientes'])]

	#Guardando el nombre del consultorio en mayúscula.
	def create(self, cr, uid, vals, context=None):
		vals.update({'name': vals['name'].upper()})
		return super(doctor_room, self).create(cr, uid, vals, context=context)
