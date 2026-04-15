{
    'name': 'Advanced Reporting System',
    'version': '18.0.1.0.0',
    'category': 'Reporting',
    'summary': 'Full Reporting Hub with PDF and Excel support',
    'author': 'Mohamed',
    'depends': ['base', 'product', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/report_wizard_view.xml',
        'views/report_data_views.xml',
        'reports/ir_actions_report.xml',
        'reports/report_template.xml',
    ],
    'installable': True,
    'application': True,
}