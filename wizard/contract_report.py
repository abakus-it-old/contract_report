# -*- coding: utf-8 -*-

from openerp import models, fields, api, _

class contract_report(models.Model):
    _name = 'contract.report'

    statistics = fields.Boolean(string="Statistics")
    remove_prices = fields.Boolean(string="Remove prices")
    
    @api.model
    def get_instance(self):
        return self.search([('id','=',1)], limit=1)
        
    @api.model
    def get_statistics(self):
        contract_report = self.search([('id','=',1)], limit=1)
        if contract_report:
            return contract_report.statistics
        return False
        
    @api.model
    def get_remove_prices(self):
        contract_report = self.search([('id','=',1)], limit=1)
        if contract_report:
            return contract_report.remove_prices
        return False
    
class contract_report_wizard(models.TransientModel):
    _name = 'contract.report.wizard'

    def _default_start_date(self):
        return self.env['sale.subscription.shared'].get_start_date()
    
    def _default_end_date(self):
        return self.env['sale.subscription.shared'].get_end_date()
    
    def _default_statistics(self):
        return self.env['contract.report'].get_statistics()
    
    def _default_remove_prices(self):
        return self.env['contract.report'].get_remove_prices()
    
    start_date = fields.Date(string="Start date", default=_default_start_date)
    end_date = fields.Date(string="End date", default=_default_end_date)
    statistics = fields.Boolean(string="Statistics", default=_default_statistics)
    remove_prices = fields.Boolean(string="Remove prices", default=_default_remove_prices)
    
    @api.multi
    def save(self):
        self.ensure_one()
        self.env['sale.subscription.shared'].browse(1).write({'start_date' : self.start_date, 'end_date':self.end_date})
        self.env['contract.report'].browse(1).write({'statistics' : self.statistics, 'remove_prices':self.remove_prices})                                            
        return {'type': 'ir.actions.act_window_close'}
               
    @api.model
    def reset_stats(self):
        self.env['sale.subscription.shared'].browse(1).write({'start_date' : None, 'end_date':None})
        self.env['contract.report'].browse(1).write({'statistics' : False, 'remove_prices':False})                                            

    #get context from method print_timesheets_report in sale.subscription (contract_report)
    @api.multi
    def print_report(self):
        self.save()
        account_ids = self.env.context['account_ids']
        return self.env['report'].get_action(self.env['sale.subscription'].browse(account_ids), 'contract_report.report_contract')
        
    #get context from method action_service_report_sent in sale.subscription (contract_report)
    @api.multi
    def send_by_email(self):    
        self.save()
        compose_form_id = self.env.context['compose_form_id']
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': self.env.context,
        }