# Copyright 2023 Samet Altuntaş (https://github.com/samettal)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Export Shipments Discussion Channel",
    "summary": "Introduces a Dedicated Discussion Channel for Confirmed Export Sales.",
    "description": "This module adds a discussion channel dedicated for export sales. Thanks to this, every user can join and track confirmed sales",
    "version": "12.0.1.0.0",
    "category": "General",
    "website": "https://github.com/samettal",
    "author": "Samet Altuntaş",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["sale"],
    "data": ["data/mail_channel_export_shipments.xml"],
    # "discuss_channels": [],
}
