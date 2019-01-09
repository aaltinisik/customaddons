
from openerp import models, fields, api, _
import csv
import base64
import tempfile
import binascii
import xlrd


class wizard_import_script(models.TransientModel):
    _name = 'wizard.import.script'

    xls_file = fields.Binary('Upload XLS File')

    @api.multi
    def import_excel(self):
        fp = tempfile.NamedTemporaryFile(suffix=".xlsx")
        fp.write(binascii.a2b_base64(self.xls_file))
        fp.seek(0)
        workbook = xlrd.open_workbook(fp.name)
        sheet = workbook.sheet_by_index(0)
        rec_ids = []
        con_obj = self.env['res.country']
        state_obj = self.env['res.country.state']
        dist_obj = self.env['address.district']
        reg_obj = self.env['address.region']
        nei_obj = self.env['address.neighbour']
        for row_no in range(sheet.nrows):
            if row_no <= 0:
                fields = map(lambda row:row.value.encode('utf-8'), sheet.row(row_no))
            else:
                line = (map(lambda row:isinstance(row.value, unicode) and row.value.encode('utf-8') or str(row.value), sheet.row(row_no)))
                if line:
                    con_id = con_obj.search([('name', '=', line[0].strip())], limit=1)
                    if not con_id:
                        con_id = con_obj.create({'name': line[0].strip()})
                    
                    state_id = state_obj.search([('name', '=', line[1].strip()), ('country_id', '=', con_id.id)], limit=1)
                    if not state_id:
                        state_id = state_obj.create({'name': line[1].strip(),
                                                     'code': line[1].strip()[:2],
                                                     'country_id': con_id.id or False})
                    
                    dist_id = dist_obj.search([('name', '=', line[2].strip()), ('state_id', '=', state_id.id)], limit=1)
                    if not dist_id:
                        dist_id = dist_obj.create({'name': line[2].strip(),
                                                   'state_id': state_id.id or False})
                    
                    region_id = reg_obj.search([('name', '=', line[3].strip()), ('district_id', '=', dist_id.id)], limit=1)
                    if not region_id:
                        region_id = reg_obj.create({'name': line[3].strip(),
                                                    'district_id': dist_id.id or False})
                    
                    nei_id = nei_obj.search([('name', '=', line[4].strip()), ('region_id', '=', region_id.id)], limit=1)
                    if not nei_id:
                        nei_id = nei_obj.create({'name': line[4].strip(),
                                                 'code': line[5].strip(),
                                                 'region_id': region_id.id or False})
                    
                                                     
                                                     
                                                     
                                                     
                                                     
                                                     