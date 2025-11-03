from odoo import models , fields , api

class AccountMove(models.Model):
    _inherit = ['account.move']

    quotation_id = fields.Many2one('quotation.sale', string='Quotation')

    def action_view_quotation(self):
        self.ensure_one()
        action = self.env['ir.actions.actions']._for_xml_id('custom_sale.quotation_sale_action')
        view_id= self.env.ref('custom_sale.quotation_sale_view_form').id
        action['res_id'] = self.quotation_id.id
        action['views'] = [[view_id,'form']]
        return action

    # def action_view_quotation(self):
    #     self.ensure_one()
    #     if not self.quotation_id:
    #         return
    #
    #     action = self.env['ir.actions.actions']._for_xml_id('custom_sale.quotation_sale_action')
    #     view_id = self.env.ref('custom_sale.quotation_sale_view_form').id
    #     action.update({
    #         'res_id': self.quotation_id.id,
    #         'views': [[view_id, 'form']],
    #         'target': 'current',
    #     })
    #     return action















