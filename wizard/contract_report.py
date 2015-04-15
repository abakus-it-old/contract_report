from openerp import models, fields, api
from openerp.osv import osv

class contract_report(models.Model):
    _name = 'contract.report'
    
    start_date = fields.Date(string="Start date")
    end_date = fields.Date(string="End date")

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
        
    def save(self, cr, uid, ids, context=None):
        contract_report_wizard=self.browse(cr,uid,ids[0])
        contract_report_obj = self.pool.get('contract.report')
        #contract.report with id 1 is created in contract_report.xml as record
        contract_report_obj.write(cr,uid,1,{'start_date' : contract_report_wizard.start_date,'end_date':contract_report_wizard.end_date})
        return {
                'type': 'ir.actions.act_window_close',
               }    

    _name = 'contract.report.wizard'
    start_date = fields.Date(string="Start date", default=_default_start_date)
    end_date = fields.Date(string="End date", default=_default_end_date) 