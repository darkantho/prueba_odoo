from odoo import http
from odoo.http import request
import json

class ModuloRestApi(http.Controller):
    @http.route('/invoices/', auth='public', methods=['GET'], csrf=False)
    def list_invoices(self, **kwargs):
        invoices = request.env['account.move'].sudo().search([('move_type', 'in', ['in_invoice', 'out_invoice']), ('state', '=', 'posted')])
        invoice_data = []
        for invoice in invoices:          
            customer = request.env['res.partner'].sudo().search([('id', '=', invoice.partner_id.id)]).read()
            invoice_data.append({
                'id': invoice.id,
                'createtime': str(invoice.create_date),
                'document_number': invoice.name.split(' ')[1],
                'date': str(invoice.date),
                'customer': {
                    'document_type': customer[0]['l10n_latam_identification_type_id'][1],
                    'document_number': customer[0]['vat'],
                    'first_name': customer[0]['name'] ,
                    'last_name': customer[0]['name'],
                    'phone': customer[0]['phone'],
                    'address': customer[0]['street'],
                    'email': customer[0]['email'],
                },
                'items': [
                    {
                        'reference': line.product_id.default_code,
                        'name': line.product_id.name,
                        'price': line.price_total,
                        'discount': line.discount,
                        'subtotal': line.price_subtotal,
                        # 'quantity': line.quantity,
                        # 'tax': line.tax_ids[0].amount,
                        'tax': line.price_subtotal * line.tax_ids[0].amount / 100,
                        'total': line.price_total,
                    } for line in invoice.invoice_line_ids
                ],
                'amount_total': invoice.amount_total,
            })
        
        response_data = {
            'status': 'success',
            'data': invoice_data
        }
        
        # Convertir el diccionario a formato JSON
        json_response = json.dumps(response_data)
        
        # Crear la respuesta HTTP con el contenido JSON
        http_response = request.make_response(json_response)
        
        # Establecer el tipo de contenido como JSON
        http_response.headers['Content-Type'] = 'application/json'
        
        return http_response

    @http.route('/invoices/', auth='public', methods=['POST'], csrf=False)
    def create_invoice(self, **kwargs):
      request_data = json.loads(request.httprequest.data)
      customer = request_data.get('customer')
      invoice_items = request_data.get('items')
      partner = request.env['res.partner'].sudo().search([('vat', '=', customer.get('document_number'))])
      
      if not partner:
          
          partner = request.env['res.partner'].sudo().create({
          'name': customer.get('first_name') + ' ' + customer.get('last_name'),
          'l10n_latam_identification_type_id': customer.get('document_type'),
          'vat': customer.get('document_number'),
          'phone': customer.get('phone'),
          'street': customer.get('address'),
          'email': customer.get('email'),
          })
      
      invoice_lines = []
      for item in invoice_items:
          product = request.env['product.product'].sudo().search([('default_code', '=', item.get('SKU'))])
          print(product.taxes_id.ids,"-----------------")
          invoice_lines.append((0, 0, {
              'product_id': product.id,
              'name': product.name,
              'price_unit': product.list_price,
              'discount': item.get('discount'),
              'quantity': item.get('quantity'),
              'tax_ids': [(6, 0, product.taxes_id.ids)],
          }))
      
      invoice = request.env['account.move'].sudo().create({
          'partner_id': partner.id,
          'invoice_line_ids': invoice_lines,
          'move_type': 'out_invoice',
      })
      
      invoice.action_post()
          
      response_data = {
          'status': 'success',
          'message': 'Invoice created',
          'data': {
                'id': invoice.id,
                'createtime': str(invoice.create_date),
                'document_number': invoice.name.split(' ')[1],
                'date': str(invoice.date),
                'customer': {
                    'document_type': customer.get('document_type'),
                    'document_number': customer.get('document_number'),
                    'first_name': customer.get('first_name'),
                    'last_name': customer.get('last_name'),
                    'phone': customer.get('phone'),
                    'address': customer.get('address'),
                    'email': customer.get('email'),
                },
                'items': [
                    {
                        'reference': line.product_id.default_code,
                        'name': line.product_id.name,
                        'price': line.price_total,
                        'discount': line.discount,
                        'subtotal': line.price_subtotal,
                        # 'quantity': line.quantity,
                        # 'tax': line.tax_ids[0].amount,
                        'tax': line.price_subtotal * line.tax_ids[0].amount / 100,
                        'total': line.price_total,
                    } for line in invoice.invoice_line_ids
                ],
                'amount_total': invoice.amount_total,
            }
      }

      json_response = json.dumps(response_data)
      http_response = request.make_response(json_response)      
      http_response.headers['Content-Type'] = 'application/json'
      return http_response

    @http.route('/invoices/<int:invoice_id>/', auth='public', methods=['DELETE'], csrf=False)
    def delete_invoice(self, invoice_id, **kwargs):
        invoice = request.env['account.move'].sudo().search([('id', '=', invoice_id)])
        response_data = {}
      
        if invoice and invoice.state != 'posted':
            customer = request.env['res.partner'].sudo().search([('id', '=', invoice.partner_id.id)]).read()[0]
            response_data = {
                'status': 'success',
                'message': 'Invoice deleted',
                "data": {
                'id': invoice.id,
                'createtime': str(invoice.create_date),
                'document_number': invoice.name.split(' ')[1],
                'date': str(invoice.date),
                'customer': {
                    'document_type': customer.get('l10n_latam_identification_type_id')[1],
                    'document_number': customer.get('vat'),
                    'first_name': customer.get('name'),
                    'last_name': customer.get('name'),
                    'phone': customer.get('phone'),
                    'address': customer.get('address'),
                    'email': customer.get('email'),
                },
                'items': [
                    {
                        'reference': line.product_id.default_code,
                        'name': line.product_id.name,
                        'price': line.price_total,
                        'discount': line.discount,
                        'subtotal': line.price_subtotal,
                        # 'quantity': line.quantity,
                        # 'tax': line.tax_ids[0].amount,
                        'tax': line.price_subtotal * line.tax_ids[0].amount / 100,
                        'total': line.price_total,
                    } for line in invoice.invoice_line_ids
                ],
                'amount_total': invoice.amount_total,
              }
            }
            invoice.unlink()
        else:
            response_data = {
                'status': 'error',
                'message': 'La factura no fue encontrada o ya fue confirmada y no se puede eliminar',
            }
        
        json_response = json.dumps(response_data)
        http_response = request.make_response(json_response)
        http_response.headers['Content-Type'] = 'application/json'
        return http_response

