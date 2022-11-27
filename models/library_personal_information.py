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
import random
from datetime import date
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class LibraryPersonalInformation(models.Model):
    _name = "library.personal.information"
    _description = "Library Personal Information"
    _order = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _sql_constraints = [
        ('id_no_uniq', 'unique(id_no)', "ID Number already exists !"),
    ]

    _TYPE = [
        ('student', "Student"),
        ('teacher', "Teacher"),
    ]

    _STATE = [
        ('draft', "Draft"),
        ('confirm', "Confirmed"),
        ('activate', "Activated"),
        ('graduate', "Graduated"),
        ('dropout', "Dropout")
    ]

    id_no = fields.Char('ID No.', copy=False)
    image_medium = fields.Image(copy=False)
    name = fields.Char('Name', compute="_compute_name", store=True)
    last_name = fields.Char('Last Name', tracking=True, index=True)
    first_name = fields.Char('First Name', tracking=True, index=True)
    middle_name = fields.Char('Middle Name', tracking=True, index=True)
    home_street = fields.Char('Home Street', tracking=True, copy=False)
    home_street2 = fields.Char('Home Street 2', tracking=True)
    home_city = fields.Char('Home City', tracking=True)
    home_state_id = fields.Many2one('res.country.state', 'Home State', domain="[('country_id','=',country_id)]",
                                    tracking=True)
    home_zip = fields.Char('Home Zip', tracking=True)
    home_phone = fields.Char('Phone No.', tracking=True)
    mobile_phone = fields.Char('Mobile No.', tracking=True)
    personal_email = fields.Char('Personal Email', tracking=True, required=True)
    country_id = fields.Many2one(
        'res.country', 'Nationality (Country)', tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], default="male", tracking=True)
    place_of_birth = fields.Char('Place of Birth', tracking=True)
    country_of_birth = fields.Many2one('res.country', string="Country of Birth", tracking=True)
    birthday = fields.Date('Date of Birth')
    father_name = fields.Char("Father's Name", tracking=True)
    mother_name = fields.Char("Mother's Name", tracking=True)
    emergency_contact = fields.Char("Emergency Contact", tracking=True)
    emergency_phone = fields.Char("Emergency Phone", tracking=True)
    user_id = fields.Many2one('res.users', string="Related User", copy=False, index=True)
    year_level_id = fields.Many2one('library.year_level.config', string="Year Level", tracking=True,
                                    copy=False, index=True)
    section_id = fields.Many2one('library.section.config', string="Section", tracking=True, copy=False, index=True)
    type = fields.Selection(_TYPE, "Type", default='student', copy=False)
    state = fields.Selection(_STATE, string='State', default='draft', tracking=True, copy=False)
    active = fields.Boolean(default=True)
    book_request_ids = fields.Many2many('library.book.requests', string='Book Requests')
    user_login = fields.Char('Username')
    temporary_password = fields.Char('Temporary Password')

    # @api.model
    # def create(self, vals):
    #     vals['name'] = self.env['ir.sequence'].next_by_code('class_number') or _('New')
    #     res = super(Library201, self).create(vals)
    #     return res

    @api.depends('last_name', 'first_name', 'middle_name')
    def _compute_name(self):
        for rec in self:
            if not rec.last_name and not rec.first_name and not rec.middle_name:
                rec.name = ''
            elif not rec.last_name and rec.first_name and not rec.middle_name:
                rec.name = "%s" % rec.first_name
            elif not rec.last_name and rec.first_name and rec.middle_name:
                rec.name = "%s %s" % (rec.first_name, rec.middle_name)
            elif rec.last_name and rec.first_name and not rec.middle_name:
                rec.name = "%s, %s" % (rec.last_name, rec.first_name)
            else:
                rec.name = "%s, %s %s" % (rec.last_name, rec.first_name, rec.middle_name)

    def generate_temporary_password(self, length=None):
        chars = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
        if not length:
            length = 8
        password = ''.join(random.sample(chars, length))
        return password

    def action_create_portal_user(self):
        for rec in self:
            rec.ensure_one()

            ResUsers = self.env['res.users']
            temporary_password = rec.generate_temporary_password()
            user = ResUsers.sudo().create({'name': rec.name,
                                           'login': rec.personal_email,
                                           'password': temporary_password,
                                           'email': rec.personal_email,
                                           'personal_info_id': rec.id,
                                           'image_1920': rec.image_medium,
                                           'groups_id': [(4, self.env.ref('base.group_user').id)]})

            rec.write({'user_id': user,
                       'user_login': user.login,
                       'temporary_password': temporary_password
                       })

    def action_confirm(self):
        for rec in self:
            if not rec.user_id:
                raise ValidationError(_("Please create user login first."))
            rec.state = 'confirm'

    def action_activate(self):
        for rec in self:
            rec.state = 'activate'

    def action_graduate(self):
        for rec in self:
            rec.write({'state': 'graduate', 'date_graduation': fields.Date.today()})

    def action_dropout(self):
        for rec in self:
            rec.write({'state': 'dropout'})

    def unlink(self):
        for rec in self:
            if rec.state != 'draft':
                raise ValidationError(_("You may only delete a personal information record in 'Draft' state."))
        return super(LibraryPersonalInformation, self).unlink()



