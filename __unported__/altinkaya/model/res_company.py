from openerp.osv import osv, fields


class res_company(osv.osv):
    _inherit = "res.company"

    _columns = {
        'hash_code': fields.char('Hash Comm Code', size=200, help="Used in comm with ext services"),
        }
res_company()

