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


class LibraryBooks(models.Model):
    _name = "library.books"
    _description = "Library Books"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _STATE = [
        ('draft', "Draft"),
        ('confirm', "Confirmed"),
        ('approve', "Approved"),
        ('publish', "Published")
    ]

    _STATUS = [
        ('available', "Available"),
        ('unavailable', "Unavailable"),
        ('book_loan', "Book Loaned"),
    ]

    name = fields.Char("Book Name", copy=False)
    image_medium = fields.Image(copy=False)
    description = fields.Text("Description", copy=False)
    category_id = fields.Many2one('library.category.config', string="Category", index=True)
    isbn = fields.Char("ISBN")
    book_title = fields.Char("Title", copy=False)
    book_author_id = fields.Many2one('library.author.config', string="Author", index=True)
    book_publisher_id = fields.Many2one('library.publisher.config', string="Publisher", index=True)
    book_copyright_id = fields.Many2one('library.copyright.config', string="Copyright", index=True)
    book_edition_id = fields.Many2one('library.edition.config', string="Edition", index=True)
    subject_id = fields.Many2one('library.subject.config', string="Subject", index=True)
    book_pages = fields.Char(copy=False)
    state = fields.Selection(_STATE, string="Status", default='draft', copy=False)
    bookshelves = fields.Integer("Bookshelve", copy=False)
    book_status = fields.Selection(_STATUS, string="Book Status", default='unavailable', copy=False)
    link = fields.Char("Link", copy=False)
    book_file = fields.Binary("File", copy=False)
    file_name = fields.Char("File Name")
    active = fields.Boolean(default=True)
    assignee_id = fields.Many2one('res.users', string='Assigned to', default=lambda self: self.env.user, copy=False)
    book_cost = fields.Float('Book Cost')
    book_qty = fields.Integer('Book Quantity')
    book_request_ids = fields.One2many('library.book.requests', 'book_id', string="Book Requests")
    count_request = fields.Integer('Book Loan Quantity', compute='_get_book_requests_count')

    @api.depends('book_request_ids')
    def _get_book_requests_count(self):
        for rec in self:
            rec.count_request = 0
            count_request = len(rec.book_request_ids.filtered_domain(
                [('state', 'in', ['in_progress', 'overdue'])]))
            if count_request > 0:
                rec.count_request = count_request

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_approve(self):
        for rec in self:
            rec.state = 'approve'

    def action_publish(self):
        for rec in self:
            rec.state = 'publish'
            rec.book_status = 'available'

    def action_view_book_requests(self):
        self.ensure_one()

        vals = {
            'name': 'Book Requests',
            'view_mode': 'tree,form',
            'res_model': 'library.book.requests',
            'type': 'ir.actions.act_window',
            'context': {},
            'domain': [('id', 'in', self.book_request_ids.ids), ('state', 'in', ['in_progress', 'overdue'])],
            'target': 'current',
        }
        return vals

    def unlink(self):
        for rec in self:
            if rec.state != 'draft':
                raise ValidationError(_("You may only delete a book record in 'Draft' state."))
        return super(LibraryBooks, self).unlink()


# class LibraryBookLoan(models.Model):
#     _name = "library.book.loan"
#     _description = "Library Book Loan"
#
#     _STATE = [
#         ('draft', "Draft"),
#         ('request', "Request"),
#         ('done', "Done"),
#         ('reject', "Rejected"),
#         ('cancel', "Cancelled")
#     ]
#
#     student_id = fields.Many2one('libray.personal.information', string="Student", ondelete='cascade', index=True)
#     book_title = fields.Char("Title")
#     date_request = fields.Date("Date Request", copy=False)
#     loan_days = fields.Integer("Loan Days")
#     due_date = fields.Date("Due Date")
#     state = fields.Selection(_STATE, "Status")


