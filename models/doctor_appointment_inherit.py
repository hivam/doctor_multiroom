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
import time
from datetime import date, datetime, timedelta

class doctor_appointment(osv.osv):
	_name = 'doctor.appointment'
	_inherit = 'doctor.appointment'

	_columns = {
		'consultorio_id': fields.many2one('doctor.room', 'Consultorio', required=True),
	}

	def onchange_start_time(self, cr, uid, ids, schedule_id, professional_id, time_begin, context=None):
		values = {}
		if not schedule_id:
			return values

		schedule = self.pool.get('doctor.schedule').browse(cr, uid, schedule_id, context=context)
		schedule_professional = schedule.professional_id.id
		consultorio_id=schedule.consultorio_id.id
		schedule_begin = datetime.strptime(schedule.date_begin, "%Y-%m-%d %H:%M:%S")

		date_begin_calculate=self.pool.get('doctor.appointment').onchange_calcular_hora_inicio_con_agenda(cr, uid, ids, schedule_id, time_begin)
		_logger.info(date_begin_calculate)
		if time_begin:
			_logger.info('Si tiene fecha')
			date_begin=date_begin_calculate
			values.update({
				'time_begin': date_begin,
				'professional_id': schedule_professional,
				'consultorio_id' : consultorio_id,
 			})

		
		if not time_begin:
			_logger.info('No tiene fecha')
			time_begin = schedule_begin.strftime("%Y-%m-%d %H:%M:%S")
			values.update({
				'time_begin': time_begin,
				'professional_id': schedule_professional,
				'consultorio_id' : consultorio_id,
			})


		return {'value': values}

	def create(self, cr, uid, vals, context=None):
		modelo_buscar = self.pool.get('doctor.schedule')
		consultorio_id = modelo_buscar.browse(cr, uid, vals['schedule_id'], context=context).consultorio_id.id
		if consultorio_id:
			vals.update({'consultorio_id': consultorio_id })
		return super(doctor_appointment, self).create(cr, uid, vals, context)

	#se sobrescribe y se retorna true simplemente para evitar la validacion
	def _check_appointment(self, cr, uid, ids, context=None):
		return True

	def _chech_cita(self, cr, uid, ids, context=None):
		fecha_hora_actual = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:00")
		fecha_hora_actual = datetime.strptime(fecha_hora_actual, "%Y-%m-%d %H:%M:00")
		fecha_usuario_ini = fecha_hora_actual.strftime('%Y-%m-%d 00:00:00')
		for record in self.browse(cr, uid, ids, context=context):
			if record.schedule_id:
				if record.schedule_id.consultorio_id.multi_paciente:
						return True
			else:
				if record.time_begin < fecha_usuario_ini:
					return True
				else:
					appointment_ids = self.search(cr, uid,
												  [('time_begin', '<', record.time_end), ('time_end', '>', record.time_begin),
												   ('aditional', '=', record.aditional), ('state', '=', record.state),
												   ('id', '<>', record.id)])
					if appointment_ids:
						return False
		
		return True

	_constraints = [
		(_check_appointment, 'Error ! Already exists an appointment at that time.', ['time_begin', 'time_end']),
		(_chech_cita, '¡Atención! Ya hay una cita programada para la hora seleccionada.', ['Desde', 'Hasta']),
	]
