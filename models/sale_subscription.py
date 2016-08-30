# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
import datetime
from datetime import date
import pytz

class sale_subscription_report_methods(models.Model):
    _inherit = 'sale.subscription'
    contract_report_info = fields.Char(compute='_compute_contract_report_info',string="Contract report settings", store=False)
    report_partner_id = fields.Many2one('res.partner', 'Partner for the Report')

    @api.multi
    def action_service_report_sent(self):
        template = self.env.ref('contract_report.email_template_service_report', False)
        compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)
        ctx = dict(
            default_model='sale.subscription',
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template.id,
            default_composition_mode='comment',
            compose_form_id=compose_form.id,
        )

        view_id = self.env['ir.model.data'].get_object_reference('contract_report', 'view_contract_report_wizard_send_by_email')[1]
        self.env['contract.report.wizard'].reset_stats()
        return {
            'name':_("Send by Email Service Report"),
            'view_mode': 'form',
            'view_id': view_id,
            'view_type': 'form',
            'res_model': 'contract.report.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': ctx,
        }

    @api.multi
    def print_timesheets_report(self):
        view_id = self.env['ir.model.data'].get_object_reference('contract_report', 'view_contract_report_wizard_print')[1]
        self.env['contract.report.wizard'].reset_stats()
        return {
            'name':_("Print Service Report"),
            'view_mode': 'form',
            'view_id': view_id,
            'view_type': 'form',
            'res_model': 'contract.report.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'account_ids': self.ids,}
        }
    
    @api.one
    def _compute_contract_report_info(self):
        self.contract_report_info = ""
        contract_report = self.env['contract.report'].get_instance()
        sale_subscription_shared = self.env['sale.subscription.shared'].get_instance()
        self.contract_report_info = "Start date: %s, End date: %s, Statistics: %s, Remove prices: %s" %(sale_subscription_shared.start_date,sale_subscription_shared.end_date,str(contract_report.statistics),str(contract_report.remove_prices))
    
    @api.model
    def format_decimal_number(self, number, point_numbers=2, separator=','):
        number_string = str(round(round(number, point_numbers+1),point_numbers))
        for x in range(0, point_numbers):
            if len(number_string[number_string.rfind('.')+1:]) < 2:
                number_string += '0'
            else:
                break        
        return number_string.replace('.',separator)
    
    @api.model    
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
    
    @api.model
    def check_start_end_line_date(self, lineDate):
        sale_subscription_shared = self.env['sale.subscription.shared'].get_instance()
        if not sale_subscription_shared.start_date:
            start_date = datetime.datetime.strptime("1980-01-01", "%Y-%m-%d").date()
        else:
            start_date = datetime.datetime.strptime(sale_subscription_shared.start_date, "%Y-%m-%d").date()
        if not sale_subscription_shared.end_date:
            end_date = date.today()
        else:
            end_date = datetime.datetime.strptime(sale_subscription_shared.end_date, "%Y-%m-%d").date()
        line_date = datetime.datetime.strptime(lineDate, "%Y-%m-%d").date()

        return start_date <= line_date <= end_date
    
    @api.model
    def get_report_interval(self, contract_date_start, contract_date_end):
        if not contract_date_start:
            contract_date_start = datetime.datetime.strptime("1980-01-01", "%Y-%m-%d").date().strftime("%Y-%m-%d")
        if not contract_date_end:
            local_tz = pytz.timezone('Europe/Brussels')
            contract_date_end = datetime.datetime.now(local_tz).date().strftime("%Y-%m-%d")
        default_date_string = datetime.datetime.strptime(contract_date_start, "%Y-%m-%d").date().strftime('%d-%m-%Y')+" - "+datetime.datetime.strptime(contract_date_end, "%Y-%m-%d").date().strftime('%d-%m-%Y')
        
        sale_subscription_shared = self.env['sale.subscription.shared'].get_instance()
        if not sale_subscription_shared.start_date:
            start_date = datetime.datetime.strptime(contract_date_start, "%Y-%m-%d").date()
        else:
            start_date = datetime.datetime.strptime(sale_subscription_shared.start_date, "%Y-%m-%d").date()
        if not sale_subscription_shared.end_date:
            if date.today() <= datetime.datetime.strptime(contract_date_end, "%Y-%m-%d").date():
                end_date = date.today()
            else:
                end_date = datetime.datetime.strptime(contract_date_end, "%Y-%m-%d").date()
        else:
            if datetime.datetime.strptime(sale_subscription_shared.end_date, "%Y-%m-%d").date() > datetime.datetime.strptime(contract_date_end, "%Y-%m-%d").date():
                if date.today() <= datetime.datetime.strptime(contract_date_end, "%Y-%m-%d").date():
                    end_date = date.today()
                else:
                    end_date = datetime.datetime.strptime(contract_date_end, "%Y-%m-%d").date()
            else:
                end_date = datetime.datetime.strptime(sale_subscription_shared.end_date, "%Y-%m-%d").date()
        
        return start_date.strftime('%d-%m-%Y')+" - "+end_date.strftime('%d-%m-%Y')
    
    @api.model
    def format_date(self, a_date):
        try:
            result = datetime.datetime.strptime(a_date, "%Y-%m-%d").date().strftime('%d-%m-%Y')
            return result
        except:
            return ""
    
    @api.model
    def isStatistics(self):
        return self.env['contract.report'].get_statistics()
    
    @api.model
    def isRemovePrices(self):
        return self.env['contract.report'].get_remove_prices()
