from odoo import models , fields , api

class QuotationSale(models.Model):
    _name = 'quotation.sale'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    customer_id = fields.Many2one('res.partner', string='Customer')
    ref = fields.Char(default='New', readonly=True)
    quotation_template_id = fields.Many2one('product.product')
    expiration = fields.Date(tracking=1)
    payment_terms_id = fields.Many2one('account.payment.term')
    state = fields.Selection([
        ('quotation', 'Quotation'),
        ('quotation_sent', 'Quotation Sent'),
        ('sale_order', 'Sale Order'),
    ])
    # SALE_ORDER_STATE = [
    #     ('draft', "Quotation"),
    #     ('sent', "Quotation Sent"),
    #     ('sale', "Sales Order"),
    #     ('cancel', "Cancelled"),

    line_ids = fields.One2many('quotation.sale.line', 'quotation_sale_id')


    amount_untaxed = fields.Float(string="Total Without Tax", compute="_compute_totals", store=True)
    amount_tax = fields.Float(string="Tax Amount", compute="_compute_totals", store=True)
    amount_total = fields.Float(string="Total With Tax", compute="_compute_totals", store=True)

    @api.depends('line_ids.price_subtotal', 'line_ids.price_total')
    def _compute_totals(self):
        for rec in self:
            rec.amount_untaxed = sum(line.price_subtotal for line in rec.line_ids)
            rec.amount_total = sum(line.price_total for line in rec.line_ids)
            rec.amount_tax = rec.amount_total - rec.amount_untaxed

    def action_quotation(self):
        for rec in self:
            rec.state = 'quotation'

    def action_quotation_sent(self):
        for rec in self:
            rec.state = 'quotation_sent'

    def action_sale_order(self):
        for rec in self:
            rec.state = 'sale_order'

    @api.model_create_multi
    def create(self, vals_list):
        res = super(QuotationSale, self).create(vals_list)
        for rec in res:
            if rec.ref == 'New' or not rec.ref:
                rec.ref = self.env['ir.sequence'].next_by_code('quotation_sale_seq') or 'New'
        return res


class QuotationSaleLine(models.Model):
    _name = 'quotation.sale.line'

    product_id = fields.Many2one('product.product', string='Product')
    description = fields.Char(string='Description')
    quantity = fields.Float(string='Quantity',default=1.0)
    unit_price = fields.Float(string='Unit Price')
    tax_id = fields.Many2one('account.tax', string='Tax',default=lambda self: self._get_default_tax())
    price_subtotal = fields.Float(string='Tax excel', compute='_compute_price_subtotal',store=True)
    price_total = fields.Float(string='Tax incl',compute='_compute_price_total',store=True)
    quotation_sale_id = fields.Many2one('quotation.sale')

    def _get_default_tax(self):
        return self.env['account.tax'].search([('amount', '=', 15)])

    @api.onchange('product_id')
    def _onchange(self):
        for rec in self:
            if rec.product_id:
                rec.description=rec.product_id.name
                rec.unit_price=rec.product_id.lst_price

    @api.depends('quantity', 'unit_price')
    def _compute_price_subtotal(self):
        for rec in self:
            rec.price_subtotal = rec.quantity * rec.unit_price

    @api.depends('quantity', 'unit_price', 'tax_id')
    def _compute_price_total(self):
        for rec in self:
            tax_amount=0
            if rec.tax_id:
                tax_amount= rec.price_subtotal * (rec.tax_id.amount / 100)
                rec.price_total = rec.price_subtotal+ tax_amount














