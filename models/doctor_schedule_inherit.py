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
from datetime import date, datetime, timedelta

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

	def onchange_hora_inicio(self, cr, uid, ids, consultorio_id, date_begin, context=None):
		res={'value':{}}
		fecha_hora_actual = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:00")
		fecha_hora_actual = datetime.strptime(fecha_hora_actual, "%Y-%m-%d %H:%M:00")
		fecha_inicio_agenda = datetime.strptime(date_begin, "%Y-%m-%d %H:%M:%S")
		fecha_usuario_ini = fecha_hora_actual.strftime('%Y-%m-%d 00:00:00')
		fecha_usuario_fin = fecha_hora_actual.strftime('%Y-%m-%d 23:59:59')

		if fecha_inicio_agenda < fecha_hora_actual:
			if consultorio_id:
				f_ini = self.pool.get('doctor.doctor').fecha_UTC(fecha_usuario_ini,context=context)
				f_fin = self.pool.get('doctor.doctor').fecha_UTC(fecha_usuario_fin,context=context)
				agenda_ids = self.search(cr,uid,[('date_begin','>=', f_fin), ('date_begin', '<=', f_ini), ('consultorio_id', '=', consultorio_id)],context=None)
				ultima_agenda_id = agenda_ids and max(agenda_ids)
				
				if ultima_agenda_id:
					hora_inicio_agenda = self.browse(cr,uid,ultima_agenda_id,context=context).date_end
					res['value']['date_begin'] = str(hora_inicio_agenda)

				if not ultima_agenda_id or hora_inicio_agenda < str(fecha_hora_actual):
					res['value']['date_begin'] = str(fecha_hora_actual + timedelta(minutes=2))
			
		return res

	_constraints = [
		(_check_schedule, 'Error ! The Office Doctor is busy.', ['date_begin', 'date_end']),
		(_check_consultorio_disponible, 'El consultorio seleccionado no está disponible en la fecha/hora especificada.', ['Consultorio']),
		(_check_medico_disponible, 'El doctor seleccionado no está disponible en la fecha/hora especificada.', ['Doctor']),
	]
