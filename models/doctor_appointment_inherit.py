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
		time_begin = schedule_begin.strftime("%Y-%m-%d %H:%M:%S")

		values.update({
			'time_begin': time_begin,
			'professional_id': schedule_professional,
			'consultorio_id' : consultorio_id,

		})
		return {'value': values}
