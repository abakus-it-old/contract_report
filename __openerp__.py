{
    'name': "AbAKUS Contract report",
    'version': '1.1',
    'depends': ['sale', 'report'],
    'author': "Bernard DELHEZ, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Contract',
    'description': 
    """
    This modules adds the possibility to print service prestation reports for contract for AbAKUS it-solutions.

    It also adds a setting wizard for the date selection of prestation range.

    This module has been developed by Bernard Delhez, intern @ AbAKUS it-solutions, under the control of Valentin Thirion.
    """,
    'data': [
        'contract_report_data.xml',
        'wizard/contract_report_view.xml',
        'report/contract_report.xml',
        'view/account_analytic_account_view.xml',
        'security/ir.model.access.csv',
    ],
}