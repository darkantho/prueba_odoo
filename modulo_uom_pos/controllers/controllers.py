# -*- coding: utf-8 -*-
# from odoo import http


# class ModuloUomPos(http.Controller):
#     @http.route('/modulo_uom_pos/modulo_uom_pos', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/modulo_uom_pos/modulo_uom_pos/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('modulo_uom_pos.listing', {
#             'root': '/modulo_uom_pos/modulo_uom_pos',
#             'objects': http.request.env['modulo_uom_pos.modulo_uom_pos'].search([]),
#         })

#     @http.route('/modulo_uom_pos/modulo_uom_pos/objects/<model("modulo_uom_pos.modulo_uom_pos"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('modulo_uom_pos.object', {
#             'object': obj
#         })
