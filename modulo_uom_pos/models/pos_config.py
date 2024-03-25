from odoo import models, fields, _, api


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


class POSSession(models.Model):
    _inherit = 'pos.session'

    def _pos_ui_models_to_load(self):
        result = super()._pos_ui_models_to_load()
        if self.config_id.product_multi_uom:
            result.append('product.template.uom.line')
        return result

    def _loader_params_product_template_uom_line(self):
        return {'search_params': {'domain': [], 'fields': ['product_uom_line_id', 'unit_of_measure_id', 'sale_price']}}

    def _get_pos_ui_product_template_uom_line(self, params):
        return self.env['product.template.uom.line'].search_read(**params['search_params'])

    def _loader_params_product_product(self):
        result = super()._loader_params_product_product()
        result['search_params']['fields'].append('product_uom_ids')
        result['search_params']['fields'].append('point_of_sale_uom')
        return result

class ProductTemplateUomLine(models.Model):
    _name = 'product.template.uom.line'
    _description = 'UOM Line'

    product_uom_line_id = fields.Many2one('product.template', string="Product UOM")
    unit_of_measure_id = fields.Many2one('uom.uom', string="unidad de medida")
    sale_price = fields.Float(string="precio de venta")