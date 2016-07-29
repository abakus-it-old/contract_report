from openerp import models, fields, api, _
import datetime
from datetime import date
import pytz

class account_analytic_account_report_methods(models.Model):
    _inherit = ['sale.subscription']
    contract_report_info = fields.Char(compute='_compute_contract_report_info',string="Contract report settings", store=False)

    @api.multi
    def action_service_report_sent(self):
        #assert len(self) == 1, 'This option should only be used for a single id at a time.'
        template = self.env.ref('contract_report.email_template_service_report', False)
        compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)
        ctx = dict(
            default_model='account.analytic.account',
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template.id,
            default_composition_mode='comment',
            mark_invoice_as_sent=True,
            compose_form_id=compose_form.id,
        )

        dummy, view_id = self.pool.get('ir.model.data').get_object_reference(self.env.cr, self.env.user.id, 'contract_report', 'view_contract_report_wizard_send_by_email')
        self.pool.get('contract.report.wizard').reset_stats(self.env.cr, self.env.user.id)
        return {
            'name':_("Send by Email Service Report"),
            'view_mode': 'form',
            'view_id': view_id,
            'view_type': 'form',
            'res_model': 'contract.report.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'domain': '',
            'context': ctx,
        }

    @api.multi
    def print_timesheets_report(self):
        dummy, view_id = self.pool.get('ir.model.data').get_object_reference(self.env.cr, self.env.user.id, 'contract_report', 'view_contract_report_wizard_print')
        self.pool.get('contract.report.wizard').reset_stats(self.env.cr, self.env.user.id)
        return {
            'name':_("Print Service Report"),
            'view_mode': 'form',
            'view_id': view_id,
            'view_type': 'form',
            'res_model': 'contract.report.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'domain': '',
            'context': {'account_ids': self.ids,}
        }
        #return self.pool['report'].get_action(cr, uid, ids, 'contract_report.report_contract', context=context)
    
    @api.one
    def _compute_contract_report_info(self):
        self.contract_report_info = ""
        cr = self.env.cr
        uid = self.env.user.id
        contract_report_obj = self.pool.get('contract.report')
        contract_report_id = contract_report_obj.search(cr, uid, [('id','=',1)])
        if contract_report_id:
            contract_report = contract_report_obj.browse(cr, uid, contract_report_id[0])
            if contract_report:
                self.contract_report_info = "Start date: %s, End date: %s, Statistics: %s, Remove prices: %s" %(contract_report.start_date,contract_report.end_date,str(contract_report.statistics),str(contract_report.remove_prices))
    
    def format_decimal_number(self, number, point_numbers=2, separator=','):
        number_string = str(round(round(number, point_numbers+1),point_numbers))
        for x in range(0, point_numbers):
            if len(number_string[number_string.rfind('.')+1:]) < 2:
                number_string += '0'
            else:
                break        
        return number_string.replace('.',separator)
        
    def decimal_to_hours(self, hoursDecimal):
        hours = int(hoursDecimal);
        minutesDecimal = ((hoursDecimal - hours) * 60);
        minutes = int(minutesDecimal);
        if minutes<10:
            minutes = "0"+str(minutes)
        else:
            minutes = str(minutes)
        hours = str(hours)
        return hours + ":" + minutes
     
    def check_start_end_line_date(self, lineDate):
        cr = self.env.cr
        uid = self.env.user.id
        contract_report_obj = self.pool.get('contract.report')
        contract_report_id = contract_report_obj.search(cr, uid, [('id','=',1)])
        if contract_report_id:
            contract_report = contract_report_obj.browse(cr, uid, contract_report_id[0])
            if contract_report:
                if not contract_report.start_date:
                    start_date = datetime.datetime.strptime("1980-01-01", "%Y-%m-%d").date()
                else:
                    start_date = datetime.datetime.strptime(contract_report.start_date, "%Y-%m-%d").date()
                if not contract_report.end_date:
                    end_date = date.today()
                else:
                    end_date = datetime.datetime.strptime(contract_report.end_date, "%Y-%m-%d").date()
                line_date = datetime.datetime.strptime(lineDate, "%Y-%m-%d").date()

                return start_date <= line_date <= end_date
            else:
                return True
        else:
            return True
        
    def get_report_interval(self, contract_date_start, contract_date_end):
        cr = self.env.cr
        uid = self.env.user.id
        contract_report_obj = self.pool.get('contract.report')
        contract_report_id = contract_report_obj.search(cr, uid, [('id','=',1)])
        if not contract_date_start:
            contract_date_start = datetime.datetime.strptime("1980-01-01", "%Y-%m-%d").date().strftime("%Y-%m-%d")
        if not contract_date_end:
            local_tz = pytz.timezone('Europe/Brussels')
            contract_date_end = datetime.datetime.now(local_tz).date().strftime("%Y-%m-%d")
        default_date_string = datetime.datetime.strptime(contract_date_start, "%Y-%m-%d").date().strftime('%d-%m-%Y')+" - "+datetime.datetime.strptime(contract_date_end, "%Y-%m-%d").date().strftime('%d-%m-%Y')
        if contract_report_id:
            contract_report = contract_report_obj.browse(cr, uid, contract_report_id[0])
            if not contract_report.start_date:
                start_date = datetime.datetime.strptime(contract_date_start, "%Y-%m-%d").date()
            else:
                start_date = datetime.datetime.strptime(contract_report.start_date, "%Y-%m-%d").date()
            if not contract_report.end_date:
                if date.today() <= datetime.datetime.strptime(contract_date_end, "%Y-%m-%d").date():
                    end_date = date.today()
                else:
                    end_date = datetime.datetime.strptime(contract_date_end, "%Y-%m-%d").date()
            else:
                if datetime.datetime.strptime(contract_report.end_date, "%Y-%m-%d").date() > datetime.datetime.strptime(contract_date_end, "%Y-%m-%d").date():
                    if date.today() <= datetime.datetime.strptime(contract_date_end, "%Y-%m-%d").date():
                        end_date = date.today()
                    else:
                        end_date = datetime.datetime.strptime(contract_date_end, "%Y-%m-%d").date()
                else:
                    end_date = datetime.datetime.strptime(contract_report.end_date, "%Y-%m-%d").date()
            return start_date.strftime('%d-%m-%Y')+" - "+end_date.strftime('%d-%m-%Y')
        else:
            return default_date_string
    
    def format_date(self, a_date):
        try:
            result = datetime.datetime.strptime(a_date, "%Y-%m-%d").date().strftime('%d-%m-%Y')
            return result
        except:
            return ""
    
    def isStatistics(self):
        cr = self.env.cr
        uid = self.env.user.id
        contract_report_obj = self.pool.get('contract.report')
        contract_report_id = contract_report_obj.search(cr, uid, [('id','=',1)])
        if contract_report_id:
            contract_report = contract_report_obj.browse(cr, uid, contract_report_id[0])
            return contract_report.statistics
        else:
            return False
            
    def isRemovePrices(self):
        cr = self.env.cr
        uid = self.env.user.id
        contract_report_obj = self.pool.get('contract.report')
        contract_report_id = contract_report_obj.search(cr, uid, [('id','=',1)])
        if contract_report_id:
            contract_report = contract_report_obj.browse(cr, uid, contract_report_id[0])
            return contract_report.remove_prices
        else:
            return False