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

class doctor_schedule_inherit(osv.osv):
	_name = 'doctor.schedule'
	_inherit = 'doctor.schedule'

	_columns = {
		'consultorio_id': fields.many2one('doctor.room', 'Consultorio', required=True),
	}

	def _check_schedule(self, cr, uid, ids):
		return True

	def _check_consultorio_disponible(self, cr, uid, ids):
		for record in self.browse(cr, uid, ids):
			schedule_ids = self.search(cr, uid, [('date_begin', '<', record.date_end), ('date_end', '>', record.date_begin), '&', ('id', '<>', record.id), ('consultorio_id', '=', record.consultorio_id.id)])
			if schedule_ids:
				return False
		return True

	def _check_medico_disponible(self, cr, uid, ids):
		for record in self.browse(cr, uid, ids):
			doctors_ids = self.search(cr, uid, [('date_begin', '<', record.date_end), ('date_end', '>', record.date_begin), '&', ('id', '<>', record.id), ('professional_id', '=', record.professional_id.id)])
			if doctors_ids:
				return False
		return True

	_constraints = [
		(_check_schedule, 'Error ! The Office Doctor is busy.', ['date_begin', 'date_end']),
		(_check_consultorio_disponible, 'El consultorio seleccionado no está disponible en la fecha/hora especificada.', ['Consultorio']),
		(_check_medico_disponible, 'El doctor seleccionado no está disponible en la fecha/hora especificada.', ['Doctor']),
	]
