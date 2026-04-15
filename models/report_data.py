from odoo import models, fields, api


class AdvancedReportData(models.Model):
    _name = 'report.advanced.data'
    _description = 'Advanced Report'

    name = fields.Char(string="Report Title", required=True)
    report_type = fields.Selection([
        ('financial', 'Financial'),
        ('sales', 'Sales'),
    ], default='sales')
    date = fields.Date(string="Date", default=fields.Date.context_today)
    responsible_id = fields.Many2one('res.users', string="Analyst", default=lambda self: self.env.user)

    # --- الحقول الناقصة اللي سببت المشكلة ---
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string='Currency')
    # ---------------------------------------

    total_amount = fields.Float(string="Total", compute="_compute_total", store=True)
    line_ids = fields.One2many('report.advanced.line', 'report_id', string="Lines")
    notes = fields.Html(string="Summary")

    @api.depends('line_ids.subtotal')
    def _compute_total(self):
        for rec in self:
            rec.total_amount = sum(line.subtotal for line in rec.line_ids)


class AdvancedReportLine(models.Model):
    _name = 'report.advanced.line'
    _description = 'Report Line'

    report_id = fields.Many2one('report.advanced.data')
    product_id = fields.Many2one('product.product', string="Product")
    quantity = fields.Float(string="Qty", default=1.0)
    price_unit = fields.Float(string="Unit Price")
    subtotal = fields.Float(string="Subtotal", compute="_compute_subtotal", store=True)

    # يفضل إضافته هنا أيضاً لتسهيل عمل الـ Widgets في الـ Editable List
    currency_id = fields.Many2one(related='report_id.currency_id', depends=['report_id.currency_id'], store=True)

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price_unit