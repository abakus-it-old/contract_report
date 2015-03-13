{
    'name': "AbAKUS Contract report",
    'version': '1.1',
    'depends': ['sale', 'report'],
    'author': "Bernard DELHEZ, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Contract',
    'description': """
This modules adds the possibility to print service prestation reports for contract for AbAKUS it-solutions.

It also adds a setting wizart for the date selection of prestation range.

This module has been developed by Bernard Delhez, intern @ AbAKUS it-solutions, under the control of Valentin Thirion.

    """,
    'data': [
        'reports.xml',
        'account_analytic_account_report_wizard_view.xml',
        'contract_report.xml',
    ],
}
