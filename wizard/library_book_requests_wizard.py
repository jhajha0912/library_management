# -*- encoding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2021 Taliform Inc.
#
# Author: Benjamin Cerdena Jr. <benjamin@taliform.com>
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
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class LibraryBookRequestsWizard(models.TransientModel):
    _name = 'library.book.requests.wizard'
    _description = "Book Requests Wizard"

    book_id = fields.Many2one('library.books', 'Books')
    category_id = fields.Many2one('library.category.config', string="Category")
    name = fields.Char("Book Name")
    book_title = fields.Char("Title")
    book_author_id = fields.Many2one('library.author.config', "Author")
    subject_id = fields.Many2one('library.subject.config', string="Subject")
    student_id = fields.Many2one('library.personal.information', "Student",
                                 default=lambda self: self.env.user.personal_info_id.id)
    requestor_id = fields.Many2one('res.users', "Requested By", default=lambda self: self.env.user)
    date_request = fields.Date("Date Request")
    loan_days = fields.Integer("Loan Days")
    due_date = fields.Date("Due Date", compute="_compute_due_date", copy=False)

    @api.depends('date_request', 'loan_days')
    def _compute_due_date(self):
        for rec in self:
            if rec.date_request and rec.loan_days:
                due_date = rec.date_request + relativedelta(days=rec.loan_days)
                rec.due_date = due_date
            else:
                rec.due_date = False

    def action_confirm(self):
        book_req_obj = self.env['library.book.requests']
        for rec in self:
            vals = {
                'name': self.env['ir.sequence'].next_by_code('book_req_number'),
                'student_id': rec.student_id.id,
                'book_id': rec.book_id.id,
                'category_id': rec.category_id.id,
                'book_title': rec.book_title,
                'book_author_id': rec.book_author_id.id,
                'book_publisher_id': rec.book_id.book_publisher_id.id,
                'book_edition_id': rec.book_id.book_edition_id.id,
                'subject_id': rec.subject_id.id,
                'requestor_id': rec.requestor_id.id,
                'date_request': rec.date_request,
                'loan_days': rec.loan_days,
                'due_date': rec.due_date,
                'state': 'request'
            }
            record = book_req_obj.sudo().create(vals)

            record.student_id.book_request_ids = [(4, record.id)]

            return {
                'name': 'Book Request',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'library.book.requests',
                'res_id': record.id,
                'context': {},
                'type': 'ir.actions.act_window',
                'target': 'self'
            }
