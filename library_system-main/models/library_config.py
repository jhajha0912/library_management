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
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LibraryScheduleConfig(models.Model):
    _name = "library.schedule.config"
    _description = "Library Schedule Configuration"
    _inherit = ['mail.thread']

    SCHEDULE = [('monday', 'Monday'),
                ('tuesday', 'Tuesday'),
                ('wednesday', 'Wednesday'),
                ('thursday', 'Thursday'),
                ('friday', 'Friday'),
                ('saturday', 'Saturday'),
                ('sunday', 'Sunday')]

    _sql_constraints = [
        ('name_uniq', 'unique(name)', "Schedule already exists !"),
    ]

    name = fields.Selection(SCHEDULE)


class LibrarySectionConfig(models.Model):
    _name = "library.section.config"
    _description = "Library Section Configuration"
    _inherit = ['mail.thread']

    _sql_constraints = [
        ('name_uniq', 'unique(name)', "Section already exists !"),
    ]

    name = fields.Char(string="Section Name")


class Library201YearLevelConfig(models.Model):
    _name = "library.year_level.config"
    _description = "Library Year Level Configuration"
    _inherit = ['mail.thread']

    _sql_constraints = [
        ('name_uniq', 'unique(name)', "Year Level already exists !"),
    ]

    name = fields.Char(string="Year Name")


class LibrarySubjectsConfig(models.Model):
    _name = "library.subject.config"
    _description = "Library Subject Configuration"
    _inherit = ['mail.thread']

    _sql_constraints = [
        ('name_uniq', 'unique(name)', "Subject already exists !"),
    ]

    name = fields.Char(string="Subject Name")
    year_level_id = fields.Many2one('library.201.year_level.config', string="Year Level", track_visibility='onchange')


class LibraryParentCategConfig(models.Model):
    _name = "library.parent.category.config"
    _description = "Library Parent Category Configuration"
    _inherit = ['mail.thread']

    _sql_constraints = [
        ('name_uniq', 'unique(name)', "Parent Category already exists !"),
    ]

    name = fields.Char(string="Parent Category Name")


class LibraryCategConfig(models.Model):
    _name = "library.category.config"
    _description = "Library Category Configuration"
    _inherit = ['mail.thread']

    _sql_constraints = [
        ('name_uniq', 'unique(name)', "Category already exists !"),
    ]

    name = fields.Char(string="Category Name")


class LibraryBookAuthorConfig(models.Model):
    _name = "library.author.config"
    _description = "Library Book Author Configuration"
    _inherit = ['mail.thread']

    _sql_constraints = [
        ('name_uniq', 'unique(name)', "Book Author already exists !"),
    ]

    name = fields.Char(string="Book Author Name")


class LibraryBookPublisherConfig(models.Model):
    _name = "library.publisher.config"
    _description = "Library Book Publisher Configuration"
    _inherit = ['mail.thread']

    _sql_constraints = [
        ('name_uniq', 'unique(name)', "Book Author already exists !"),
    ]

    name = fields.Char(string="Book Author Name")


class LibraryBookCopyrightConfig(models.Model):
    _name = "library.copyright.config"
    _description = "Library Book Copyright Configuration"
    _inherit = ['mail.thread']

    _sql_constraints = [
        ('name_uniq', 'unique(name)', "Book Copyright already exists !"),
    ]

    name = fields.Char(string="Book Copyright Name")


class LibraryBookEditionConfig(models.Model):
    _name = "library.edition.config"
    _description = "Library Book Edition Configuration"
    _inherit = ['mail.thread']

    _sql_constraints = [
        ('name_uniq', 'unique(name)', "Book Edition already exists !"),
    ]

    name = fields.Char(string="Book Edition")
