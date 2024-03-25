from odoo import models, fields, _


class PosConfig(models.Model):
      
      _inherit = 'pos.config'
      product_multi_uom = fields.Boolean(string='Habilitar multiples medidas', default=False)

class PosOrder(models.Model):
    
    _inherit = 'pos.order'
    uom = fields.Boolean(string='Uom', related='config_id.product_multi_uom', readonly=True)

class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'
    uom_id = fields.Many2one('uom.uom', string="Unidad de medida")

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    product_uom_ids = fields.One2many('product.template.uom.line', 'product_uom_line_id', string="Lineas descarte")
    point_of_sale_uom = fields.Boolean(string="UOM punto de venta")

class ProductTemplateUomLine(models.Model):
    _name = 'product.template.uom.line'
    _description = 'UOM Line'

    product_uom_line_id = fields.Many2one('product.template', string="Product UOM")
    unit_of_measure_id = fields.Many2one('uom.uom', string="unidad de medida")
    sale_price = fields.Float(string="precio de venta")