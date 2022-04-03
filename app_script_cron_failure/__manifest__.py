# -*- coding: utf-8 -*-
##############################################################################
#
#    app-script.com.
#    Copyright (C) 2017-TODAY Cybrosys Technologies(<http://www.cybrosys.com>).
#    Author: Nagla Loai 
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': "Cron Failure Notification",
    'version': '10.0.1.0.1',
    'category': 'Extra Tools',
    'summary': """Cron jobs/Scheduled Actions failure Log Notification & Its PDF Reports""",
    'description': """
        This module will generate error Logs for Scheduled
        Actions / Cron jobs running in backend server
    """,
    'author': "App-script ",
    'company': "App-script",
    'website': "http://app-script.com/",
    'depends': ['base', 'mail', 'web', 'base_setup'],
    'data': [
        'views/logs_scheduled_actions_view.xml',
        'views/error_log_report_template.xml',
        'views/report.xml',
        'views/error_mail_template.xml',
        'security/ir.model.access.csv',
        'demo/ir_cron_demo.xml'
    ],
    'demo': [
        'demo/ir_cron_demo.xml'
    ],
    'images': [
        'static/description/banner.png'
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
