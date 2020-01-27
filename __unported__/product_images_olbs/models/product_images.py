# -*- encoding: utf-8 -*-
#########################################################################
# Copyright (C) 2009  Sharoon Thomas, Open Labs Business solutions      #
# Copyright (C) 2011 Akretion Sébastien BEAU sebastien.beau@akretion.com#
#                                                                       #
#This program is free software: you can redistribute it and/or modify   #
#it under the terms of the GNU General Public License as published by   #
#the Free Software Foundation, either version 3 of the License, or      #
#(at your option) any later version.                                    #
#                                                                       #
#This program is distributed in the hope that it will be useful,        #
#but WITHOUT ANY WARRANTY; without even the implied warranty of         #
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
#GNU General Public License for more details.                           #
#                                                                       #
#You should have received a copy of the GNU General Public License      #
#along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
#########################################################################
# import urllib.request
from odoo import api, fields, models, _
import base64, urllib
import os
import odoo.netsvc

#TODO find a good solution in order to roll back changed done on file system
#TODO add the posibility to move from a store system to an other (example : moving existing image on database to file system)

class product_images(models.Model):

    "Products Image gallery"
    _name = "product.images"
    _description = __doc__
    _table = "product_images"
    
    @api.model
    def unlink(self):
        local_media_repository = self.env['res.company'].get_local_media_repository()
        if local_media_repository:
            for image in self:
                path = os.path.join(local_media_repository, image.product_id.default_code, image.name)
                if os.path.isfile(path):
                    os.remove(path)          
        return super(product_images, self).unlink()

    @api.model
    def create(self,vals):
        if vals.get('name', False) and not vals.get('extention', False):
            vals['name'], vals['extention'] = os.path.splitext(vals['name'])
        return super(product_images, self).create(vals)

    @api.multi
    def write(self,vals):
        if vals.get('name', False) and not vals.get('extention', False):
            vals['name'], vals['extention'] = os.path.splitext(vals['name'])
        if vals.get('name', False) or vals.get('extention', False):
            local_media_repository = self.env['res.company'].get_local_media_repository()
            if local_media_repository:
#                 old_images = self.browse(cr, uid, ids, context=context)
                res=[]
                for old_image in self:
                    if vals.get('name', False) and (old_image.name != vals['name']) or vals.get('extention', False) and (old_image.extention != vals['extention']):
                        old_path = os.path.join(local_media_repository, old_image.product_id.default_code, '%s%s' %(old_image.name, old_image.extention))
                        res.append(super(product_images, self).write(old_image.id, vals))
                        if 'file' in vals:
                            #a new image have been loaded we should remove the old image
                            #TODO it's look like there is something wrong with function field in openerp indeed the preview is always added in the write :(
                            if os.path.isfile(old_path):
                                os.remove(old_path)
                        else:
                            #we have to rename the image on the file system
                            if os.path.isfile(old_path):
                                os.rename(old_path, os.path.join(local_media_repository, old_image.product_id.default_code, '%s%s' %(old_image.name, old_image.extention)))      
                return res
        return super(product_images, self).write(vals)

    @api.multi
    def get_image(self):
        product_product_obj = self.env['product.product']
        product_template_obj = self.env['product.template']
        for rec in self:
            each = rec.read(['link', 'url', 'name', 'file_db_store', 'product_id', 'product_t_id', 'name', 'extention'])[0]
            if each['link']:
                (filename, header) = urllib.request.urlretrieve(each['url'])
                f = open(filename , 'rb')
                img = base64.encodestring(f.read())
                f.close()
                rec.file = img
            else:
                local_media_repository = self.env['res.company'].get_local_media_repository()
                if local_media_repository:
                    if each['product_t_id']:
                        product_id = product_template_obj.browse(each['product_t_id'][0])
                        product_code = product_id.read(['default_code'])[0]['default_code']
                    else:
                        product_id = product_product_obj.browse(each['product_id'][0])
                        product_code = product_id.read(['default_code'])[0]['default_code']
                    full_path = os.path.join(local_media_repository, product_code, '%s%s'%(each['name'], each['extention']))
                    if os.path.exists(full_path):
                        try:
                            f = open(full_path, 'rb')
                            img = base64.encodestring(f.read())
                            f.close()
                        except Exception as e:
                           return False
                    else:
                        return False
                else:
                    img = each['file_db_store']
                    rec.file = img

    @api.multi
    def _get_image(self):
        res = {}
        for each in self:
            res[each] = self.get_image()
        return res


    @api.multi
    def _check_filestore(self, image_filestore):
        '''check if the filestore is created, if not it create it automatically'''
#         try:
        if not os.path.isdir(image_filestore):
            os.makedirs(image_filestore)
#         except Exception e:
#             raise osv.except_osv(_('Error'), _('The image filestore can not be created, %s'%e))
        return True

    @api.multi
    def _save_file(self, path, filename, b64_file):
        """Save a file encoded in base 64"""
        full_path = os.path.join(path, filename)
        self._check_filestore(path)
        ofile = open(full_path, 'w')
        try:
            ofile.write(base64.decodestring(b64_file))
        finally:
            ofile.close()
        return True

    @api.multi
    def _set_image(self,name, value, arg):
        local_media_repository = self.env['res.company'].get_local_media_repository()
        if local_media_repository:
#             image = self.browse(cr, uid, id, context=context)
            return self._save_file(os.path.join(local_media_repository, self.product_id.default_code), '%s%s'%(self.name, self.extention), value)
        return self.write({'file_db_store' : value})

    
    name = fields.Char('Image Title', size=100, required=True)
    extention = fields.Char('file extention', size=6)
    link = fields.Boolean('Link?', default=lambda *a: False, help="Images can be linked from files on your file system or remote (Preferred)")
    file_db_store = fields.Binary('Image stored in database')
    file = fields.Char(compute=_get_image, inverse=_set_image, type="binary", method=True, filters='*.png,*.jpg,*.gif')
    url = fields.Char('File Location', size=250)
    comments = fields.Text('Comments')
    product_id = fields.Many2one('product.product', 'Product')


    _sql_constraints = [('uniq_name_product_id', 'UNIQUE(product_id, name)',
                _('A product can have only one image with the same name'))]


