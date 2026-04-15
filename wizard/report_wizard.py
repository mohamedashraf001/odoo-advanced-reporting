from odoo import models, fields

class ReportFormatWizard(models.TransientModel):
    _name = 'report.format.wizard'
    _description = 'Report Format Wizard'

    format = fields.Selection([
        ('pdf', 'PDF Document'),
        ('excel', 'Excel Spreadsheet')
    ], string='Format', default='pdf', required=True)

    def action_print(self):
        active_ids = self.env.context.get('active_ids')
        if self.format == 'pdf':
            return self.env.ref('advanced_reporting_system.action_report_advanced_data').report_action(active_ids)
        else:
            return {
                'type': 'ir.actions.act_url',
                'url': f'/web/binary/download_report_excel?ids={active_ids}',
                'target': 'new',
            }