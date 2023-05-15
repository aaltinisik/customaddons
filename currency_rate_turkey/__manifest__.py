{
    "name": "Currency Rate Turkey",
    "version": "12.0.0.1",
    "website": "https://github.com/yibudak",
    "author": "yibudak",
    "category": "Currency",
    "summary": """This module adds currency rate fields and providers.""",
    "description": """This module adds currency rate fields and providers.""",
    "depends": ["currency_rate_update", "currency_rate_update_tcmb"],
    "python-dependencies": ["requests", "bs4"],
    "data": [
        "views/res_currency_view.xml",
        "views/res_currency_rate_view.xml",
        "views/res_partner_view.xml",
    ],
    "installable": True,
    "auto_install": False,
}
