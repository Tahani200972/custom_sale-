from odoo import models , fields , api

class AccountMove(models.Model):
    _inherit = ['account.move']

    quotation_id = fields.Many2one('quotation.sale', string='Quotation')














