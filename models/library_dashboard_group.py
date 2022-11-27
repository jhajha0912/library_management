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


class LibraryDashboardGroup(models.Model):
    _name = "library.dashboard.group"
    _description = "Library Announcements & Events"

    _TYPE = [
        ('announcement', 'Announcement'),
        ('event', 'Event')
    ]

    name = fields.Char("Name")
    description = fields.Text("Description")
    type = fields.Selection(_TYPE, "Type")
    sequence = fields.Integer("Sequence", copy=False)
    active = fields.Boolean(default=True)
