# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2013 ZestyBeanz Technologies Pvt. Ltd.
#    (http://wwww.zbeanztech.com)
#    contact@zbeanztech.com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import osv, fields

class web_shortcut(osv.osv):
    _name = 'web.shortcut'
    _description = 'Model to define web shortcuts'
    
    def _get_action_id(self, cr, uid, ids, name, args, context=None):
        res = {}
        for shortcut_obj in self.browse(cr, uid, ids, context=context):
            menu_action_id = shortcut_obj.menu_id.action and shortcut_obj.menu_id.action.id or False
            res[shortcut_obj.id] = menu_action_id
        return res
    
    _columns = {
                'menu_id': fields.many2one('ir.ui.menu', 'Menu'),
                'modifier_key': fields.selection([('ctrl', 'Ctrl'), ('alt', 'Alt'), ('shift', 'Shift')], 'Modifier'),
                'other_keys': fields.char('Other Key(s)', size=128,
                                          help="Specify the key combination \n Eg : s + i \n shift + i"),
                'user_id': fields.many2one('res.users', 'Related User'),
                'action': fields.function(_get_action_id, type="char", size=64, string="Action", store=True)
                }
    
    def _check_other_key(self, cr, uid, ids, context=None):
        for shortcut_obj in self.browse(cr, uid, ids, context=context):
            other_key = shortcut_obj.other_keys
            other_key_list = other_key.split('+')
            other_key_list = filter(lambda a: a != '', other_key_list)
            for other_key_val in other_key_list:
                if other_key_val.lower() != 'shift' and other_key_val.lower() != 'ctrl' and other_key_val.lower() != 'alt':
                    if len(other_key_val) > 1:
                        return False
        return True
    
    def _check_multi_key(self, cr, uid, ids, context=None):
        for shortcut_obj in self.browse(cr, uid, ids, context=context):
            other_key = shortcut_obj.other_keys
            modifier_key = shortcut_obj.modifier_key
            other_key_list = other_key.split('+')
            other_key_list = filter(lambda a: a != '', other_key_list)
            for other_key_val in other_key_list:
                if other_key_val.lower() == modifier_key.lower():
                    return False
        return True
    
    def _check_duplication(self, cr, uid, ids, context=None):
        for config_obj in self.browse(cr, uid, ids, context=context):
            modifier_key = config_obj.modifier_key
            other_key = config_obj.other_keys
            other_key_list = other_key.split('+')
            other_key_list = filter(lambda a: a != '', other_key_list)
            other_key_list.append(modifier_key)
            all_config_ids = self.search(cr, uid, [('user_id', '=', uid), ('id', '!=', config_obj.id)])
            for all_config_obj in self.browse(cr, uid, all_config_ids, context=context):
                comp_list = []
                comp_list.extend(other_key_list)
                all_config_mod_key = all_config_obj.modifier_key
                all_config_other_key = all_config_obj.other_keys
                all_config_other_key_list = all_config_other_key.split('+')
                all_config_other_key_list = filter(lambda a: a != '', all_config_other_key_list)
                all_config_other_key_list.append(all_config_mod_key)
                for key in other_key_list:
                    if key in all_config_other_key_list:
                        all_config_other_key_list.remove(key)
                        comp_list.remove(key)
                    if not all_config_other_key_list and not comp_list:
                        return False
                
        return True
    
    _sql_constraints = [
                        ('shortcut_uniq', 'unique(menu_id, modifier_key, other_keys, user_id)', 
                         'Same Shortcut Defined Already!'),
                        ('menu_uniq', 'unique(menu_id, user_id)', 
                         'Shortcut Defined Already!')
                        ]
    _constraints = [
                    (_check_other_key, 'Invalid or no Other Keys defined', ['other_keys']),
                    (_check_duplication, 'Configuration already defined', ['modifier_key', 'other_keys']),
                    (_check_multi_key, 'Same keys defined in Other Key(S)', ['other_keys'])
                    ]
web_shortcut()

class web_shortcut_wizard_config(osv.osv_memory):
    _name = 'web.shortcut.wizard.config'
    _description = 'Configuration'
    _columns = {
                'menu_id': fields.many2one('ir.ui.menu', 'Menu', required=True),
                'modifier_key': fields.selection([('ctrl', 'Ctrl'), ('alt', 'Alt'), ('shift', 'Shift')],
                                                 'Modifier', required=True),
                'other_keys': fields.char('Other Key(s)', size=128, required=True,
                                          help="Specify the key combination \n Eg : s + i \n shift + i"),
                'wizard_id': fields.many2one('web.shorcut.wizard', 'Wizard'),
                'config_id': fields.integer('Config id')
                }
web_shortcut_wizard_config()

class web_shortcut_wizard(osv.osv_memory):
    _name = 'web.shorcut.wizard'
    _description = 'Configuration Wizard'
    
    def default_get(self, cr, uid, fields, context=None):
        web_shortcut_pool = self.pool.get('web.shortcut')
        res = super(web_shortcut_wizard, self).default_get(cr, uid, fields, context=context)
        web_shortcut_ids = web_shortcut_pool.search(cr, uid, [], context=context)
        shortcut_data = []
        for web_shortcut_obj in web_shortcut_pool.browse(cr, uid, web_shortcut_ids, context=context):
            vals = {
                    'menu_id': web_shortcut_obj.menu_id.id,
                    'modifier_key': web_shortcut_obj.modifier_key,
                    'other_keys': web_shortcut_obj.other_keys,
                    'config_id': web_shortcut_obj.id
                    }
            shortcut_data.append(vals)
        res['shortcut_ids'] = shortcut_data
        return res
    
    _columns = {
                'shortcut_ids': fields.one2many('web.shortcut.wizard.config', 'wizard_id', 'Configuration')
                }
    def unlink_records(self, cr, uid, ids, real_ids, save_ids, context=None):
        config_pool = self.pool.get('web.shortcut.wizard.config')
        web_shortcut_pool = self.pool.get('web.shortcut')
        for config_obj in config_pool.browse(cr, uid, save_ids, context=context):
            config_id = config_obj.config_id
            if config_id > 0:
                real_ids.remove(config_id)
        web_shortcut_pool.unlink(cr, uid, real_ids, context=context)
        return True
    
    def save_record(self, cr, uid, ids, context=None):
        config_pool = self.pool.get('web.shortcut.wizard.config')
        web_shortcut_pool = self.pool.get('web.shortcut')
        data = self.read(cr, uid, ids, context=context)[0]
        shortcut_ids = data.get('shortcut_ids', [])
        config_ids = []
        web_shortcut_ids = web_shortcut_pool.search(cr, uid, [], context=context)
        self.unlink_records(cr, uid, ids, web_shortcut_ids, shortcut_ids, context=context)
        for shotcut_config_obj in config_pool.browse(cr, uid, shortcut_ids, context=context):
            config_id = shotcut_config_obj.config_id
            vals = {
                    'menu_id': shotcut_config_obj.menu_id.id,
                    'modifier_key': shotcut_config_obj.modifier_key,
                    'other_keys': shotcut_config_obj.other_keys,
                    'user_id': uid
                    }
            if config_id == 0:
                config_id = web_shortcut_pool.create(cr, uid, vals, context=context)
                config_pool.write(cr, uid, shotcut_config_obj.id, {'config_id': config_id}, context=context)
            else:
                web_shortcut_pool.write(cr, uid, config_id, vals, context=context)
        return True
    
    def cancel(self, cr, uid, ids, context=None):
        act_window = self.pool.get('ir.actions.act_window')
        action_ids = act_window.search(cr, uid, [('res_model', '=', self._name)])
        if action_ids:
            return act_window.read(cr, uid, action_ids[0], [], context=context)
        return {}
    
web_shortcut_wizard()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: