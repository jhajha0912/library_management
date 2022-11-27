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
{
    'name': 'Library Management System',
    'version': '13.0.1.0',
    'depends': ['mail'],
    'author': 'Benjamin',
    'website': '',
    'category': 'Library',
    'data': [
        'data/email_template.xml',
        'security/library_group_security.xml',
        'security/ir.model.access.csv',
        'data/library_data.xml',
        'data/library_schedule_data.xml',
        'wizard/library_feedback_wizard_view.xml',
        'wizard/library_book_requests_wizard_view.xml',
        'wizard/library_change_password_wizard_view.xml',
        'views/library_dashboard_group_view.xml',
        'views/library_personal_information_view.xml',
        'views/library_book_requests_view.xml',
        'views/library_books_view.xml',
        'views/library_feedbacks_view.xml',
        'views/library_config_view.xml',
        'views/library_mission_vision_view.xml',
        'views/webclient_templates.xml',
        'views/library_menu.xml'
        ],
    'qweb': ["static/src/xml/base_inherit.xml"],
    'auto_install': False,
}
