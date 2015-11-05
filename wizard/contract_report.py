from openerp import models, fields, api, _
from openerp.osv import osv

class contract_report(models.Model):
    _name = 'contract.report'
    
    start_date = fields.Date(string="Start date")
    end_date = fields.Date(string="End date")
    statistics = fields.Boolean(string="Statistics")
    remove_prices = fields.Boolean(string="Remove prices")

class contract_report_wizard(osv.osv_memory):
    
    def _default_start_date(self):
        cr = self.env.cr
        uid = self.env.user.id
        contract_report_obj = self.pool.get('contract.report')
        contract_report_id = contract_report_obj.search(cr, uid, [('id','=',1)])
        if contract_report_id:
            contract_report = contract_report_obj.browse(cr, uid, contract_report_id[0])
            if contract_report and contract_report[0].start_date:
                return contract_report[0].start_date
    
    def _default_end_date(self):
        cr = self.env.cr
        uid = self.env.user.id
        contract_report_obj = self.pool.get('contract.report')
        contract_report_id = contract_report_obj.search(cr, uid, [('id','=',1)])
        if contract_report_id:
            contract_report = contract_report_obj.browse(cr, uid, contract_report_id[0])
            if contract_report and contract_report[0].end_date:
                return contract_report[0].end_date
        #return date.today().strftime('%Y-%m-%d')
    
    def _default_statistics(self):
        cr = self.env.cr
        uid = self.env.user.id
        contract_report_obj = self.pool.get('contract.report')
        contract_report_id = contract_report_obj.search(cr, uid, [('id','=',1)])
        if contract_report_id:
            contract_report = contract_report_obj.browse(cr, uid, contract_report_id[0])
            if contract_report:
                return contract_report[0].statistics
    
    def _default_remove_prices(self):
        cr = self.env.cr
        uid = self.env.user.id
        contract_report_obj = self.pool.get('contract.report')
        contract_report_id = contract_report_obj.search(cr, uid, [('id','=',1)])
        if contract_report_id:
            contract_report = contract_report_obj.browse(cr, uid, contract_report_id[0])
            if contract_report:
                return contract_report[0].remove_prices
        
    def save(self, cr, uid, ids, context=None):
        contract_report_wizard=self.browse(cr,uid,ids[0])
        contract_report_obj = self.pool.get('contract.report')
        #contract.report with id 1 is created in contract_report.xml as record
        contract_report_obj.write(cr,uid,1,{'start_date' : contract_report_wizard.start_date,
                                            'end_date':contract_report_wizard.end_date, 
                                            'statistics': contract_report_wizard.statistics,
                                            'remove_prices': contract_report_wizard.remove_prices})
        return {
                'type': 'ir.actions.act_window_close',
               }
               
               
    def reset_stats(self, cr, uid):
        self.pool.get('contract.report').write(cr,uid,1,{   'start_date' : None,
                                                            'end_date': None, 
                                                            'statistics': False,
                                                            'remove_prices': False}
                                                        )
    
    #get context from method print_timesheets_report in account.analytic.account (contract_report)
    def print_report(self, cr, uid, ids, context=None):
        self.save(cr, uid, ids, context)
        account_ids = context.get('account_ids')
        return self.pool['report'].get_action(cr, uid, account_ids, 'contract_report.report_contract', context=context)
        
    #get context from method action_service_report_sent in account.analytic.account (contract_report)
    def send_by_email(self, cr, uid, ids, context=None):    
        self.save(cr, uid, ids, context)
        compose_form_id = context.get('compose_form_id')
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': context,
        }

    _name = 'contract.report.wizard'
    start_date = fields.Date(string="Start date", default=_default_start_date)
    end_date = fields.Date(string="End date", default=_default_end_date)
    statistics = fields.Boolean(string="Statistics", default=_default_statistics)
    remove_prices = fields.Boolean(string="Remove prices", default=_default_remove_prices)