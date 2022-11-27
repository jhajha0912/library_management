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
from datetime import date, datetime

from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class LibraryBookRequests(models.Model):
    _name = "library.book.requests"
    _rec_name = 'name'
    _description = "Library Book Requests"

    _STATE = [
        ('draft', "Draft"),
        ('request', "Requested"),
        ('confirm', "Confirmed"),
        ('approve', "Approved"),
        ('in_progress', "In Progress"),
        ('overdue', "Overdue"),
        ('done', "Done"),
        ('reject', "Rejected")
    ]

    name = fields.Char("Name")
    book_id = fields.Many2one('library.books', 'Books', ondelete='restrict', index=True)
    student_id = fields.Many2one('library.personal.information', "Student", ondelete='restrict', index=True)
    category_id = fields.Many2one('library.category.config', string="Category", index=True)
    image_medium = fields.Image(related="book_id.image_medium", copy=False)
    book_title = fields.Char("Title")
    book_author_id = fields.Many2one('library.author.config', "Author", index=True)
    book_edition_id = fields.Many2one('library.edition.config', "Edition", related="book_id.book_edition_id",
                                      store=True)
    book_publisher_id = fields.Many2one('library.publisher.config', "Publisher", related="book_id.book_publisher_id",
                                        store=True)
    subject_id = fields.Many2one('library.subject.config', string="Subject", index=True)
    requestor_id = fields.Many2one('res.users', "Requested By", ondelete='restrict')
    approver_id = fields.Many2one('res.users', "Done By")
    date_request = fields.Date("Date Request", copy=False)
    date_returned = fields.Date("Returned Date", copy=False)
    loan_days = fields.Integer("Loan Days", copy=False)
    due_date = fields.Date("Due Date", copy=False)
    state = fields.Selection(_STATE, "Status", default='draft', copy=False)
    cancel_reason = fields.Text()
    reject_reason = fields.Text()
    is_feedback = fields.Boolean()

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_approve(self):
        for rec in self:
            rec.state = 'approve'

    def action_done(self):
        for rec in self:
            rec.state = 'done'
            rec.book_id.book_status = 'available'
            rec.approver_id = self.env.user.id

    def action_start_loan(self):
        for rec in self:
            rec.state = 'in_progress'
            rec.book_id.book_status = 'book_loan'

    # def unlink(self):
    #     for rec in self:
    #         if rec.state != 'draft':
    #             raise ValidationError(_("You may only delete a book request record in 'Draft' state."))
    #     return super(LibraryBookRequests, self).unlink()


