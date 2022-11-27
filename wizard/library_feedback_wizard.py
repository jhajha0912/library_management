# -*- encoding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2022.
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class LibraryFeedbackWizard(models.TransientModel):
    _name = 'library.feedback.wizard'

    book_id = fields.Many2one('library.books', 'Books')
    student_id = fields.Many2one('library.personal.information', 'Student')
    feedback = fields.Text('feedback')

    def action_confirm(self):
        feedback_obj = self.env['library.feedbacks']
        for rec in self:
            vals = {
                'name': self.env['ir.sequence'].next_by_code('feedbacks_number'),
                'student_id': rec.student_id.id,
                'book_id': rec.book_id.id,
                'feedback': rec.feedback,
                'state': 'feedback',
            }
            feedback_obj.sudo().create(vals)
            #
            # return {
            #     'name': 'Feedback',
            #     'view_type': 'form',
            #     'view_mode': 'form',
            #     'res_model': 'library.feedbacks',
            #     'res_id': record.id,
            #     'context': {},
            #     'type': 'ir.actions.act_window',
            #     'target': 'self'
            # }
