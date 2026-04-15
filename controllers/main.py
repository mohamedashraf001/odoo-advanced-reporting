from odoo import http
from odoo.http import request
import io
import json

try:
    import xlsxwriter
except ImportError:
    xlsxwriter = None


class ReportController(http.Controller):
    @http.route('/web/binary/download_report_excel', type='http', auth="user")
    def download_report_excel(self, ids, **kw):
        # تنظيف الـ IDs المستلمة من الـ URL
        clean_ids = ids.replace('[', '').replace(']', '').split(',')
        report_ids = [int(i) for i in clean_ids if i.strip()]
        reports = request.env['report.advanced.data'].browse(report_ids)

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Report')

        # التنسيقات
        bold = workbook.add_format({'bold': True, 'bg_color': '#EEEEEE', 'border': 1})

        # العناوين
        headers = ['Title', 'Type', 'Date', 'Product', 'Qty', 'Price', 'Subtotal']
        for col, head in enumerate(headers):
            sheet.write(0, col, head, bold)

        row = 1
        for report in reports:
            for line in report.line_ids:
                sheet.write(row, 0, report.name)
                sheet.write(row, 1, report.report_type)
                sheet.write(row, 2, str(report.date))
                sheet.write(row, 3, line.product_id.name)
                sheet.write(row, 4, line.quantity)
                sheet.write(row, 5, line.price_unit)
                sheet.write(row, 6, line.subtotal)
                row += 1

        workbook.close()
        output.seek(0)

        return request.make_response(
            output.getvalue(),
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', 'attachment; filename=Report.xlsx;')
            ]
        )