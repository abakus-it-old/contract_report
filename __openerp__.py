# -*- coding: utf-8 -*-

{
    'name': "AbAKUS Contract report",
    'version': '9.0.1.2',
    'depends': [
        'report',
        'project',
        'sale_contract',
        'sla',
    ],
    'author': "Bernard DELHEZ, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Contract',
    'description': 
    """Contract Report for AbAKUS Baseline Projects

This modules adds the possibility to print service prestation reports for contract for AbAKUS it-solutions.

It also adds a setting wizard for the date selection of prestation range.

This module has been developed by Bernard Delhez, intern @ AbAKUS it-solutions, under the control of Valentin Thirion.
    """,
    'data': [
        'wizard/contract_report_view.xml',
        'report/contract_report.xml',
        'views/account_analytic_account_view.xml',
        'security/ir.model.access.csv',
        'data/contract_report_data.xml',
        'data/contract_report_action_data.xml',
    ],
}
