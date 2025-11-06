from odoo import models , fields
class CreateInvoiceWizard(models.TransientModel):
    _name ='create.invoice'


    quotation_id = fields.Many2one('quotation.sale')


    def action_confirm_invoice(self):
        self.ensure_one()
        quotation = self.quotation_id

        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': quotation.customer_id.id,
            'invoice_origin': quotation.ref,
            'quotation_id': quotation.id,
            'invoice_line_ids': [],
        }

        for line in quotation.line_ids:
            invoice_vals['invoice_line_ids'].append((0, 0, {
                'product_id': line.product_id.id,
                'quantity': line.quantity,
                'price_unit': line.unit_price,
                'name': line.description,
                'tax_ids': [(6, 0, line.tax_id.ids)] if line.tax_id else False,
            }))

        invoice = self.env['account.move'].create(invoice_vals)
        quotation.write({'hide_create_invoice': True})

        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': invoice.id,
            'target': 'current'
        }

