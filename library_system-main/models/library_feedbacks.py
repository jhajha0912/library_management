# -*- encoding: utf-8 -*-
##############################################################################
#
# Copyright (c) Benjamin 2022
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
from datetime import date
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class LibraryFeedbacks(models.Model):
    _name = "library.feedbacks"
    _description = "Library Feedbacks"

    _STATE = [
        ('draft', "Draft"),
        ('feedback', "Feedback"),
    ]
    
    name = fields.Char("Name")
    student_id = fields.Many2one('library.personal.information', string="Student Name", index=True)
    book_id = fields.Many2one('library.books', 'Books', index=True)
    feedback = fields.Text("Feedback")
    state = fields.Selection(_STATE, "State")

    # @api.model
    # def create(self, vals):
    #     vals['name'] = self.env['ir.sequence'].next_by_code('feedbacks_number') or _('New')
    #     res = super(LibraryFeedbacks, self).create(vals)
    #     return res
