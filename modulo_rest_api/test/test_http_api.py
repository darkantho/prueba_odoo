from odoo import fields, Command
from odoo.tests.common import TransactionCase, Form
from unittest.mock import patch

class TestRestAPI(TransactionCase):

    def setUp(self):
        super(TestRestAPI, self).setUp()
        self.partner = self.env['res.partner'].create({
            'name': 'Test Partner',
            'email': 'anthony1320081@gmail.com',
            'phone': '123456789',
            'mobile': '987654321',
            'vat': '0941274512001',
            'street': '123 Main Street',
            'city': 'Guayaquil',
            'zip': '090150',
            'country_id': self.env.ref('base.ec').id,
            'company_id': 'test_company',
            'is_company': True,
            'customer': True,
            'supplier': True,
            'company_type': 'company',
            'company_name': 'Test Company',
            'l10n_latam_identification_type_id': self.env.ref('l10n_ec.res_partner_identification_type_04').id,
            'l10n_latam_identification_id': '0941274512001',
            'property_account_position_id': self.env.ref('l10n_ec.account_fiscal_position_01').id,
            })

    @patch('requests.get')
    def test_get_invoices(self, mocked_get):
        # Mockeo la respuesta de la API
        mocked_get.return_value.status_code = 200
        mocked_get.return_value.json.return_value = {
            'status': 'success',
            'data': [{
                'id': 1,
                'createtime': '2024-03-25',
                'document_number': 'INV/001',
                'date': '2024-03-25',
                'customer': {
                    'document_type': 'TipoDocumento',
                    'document_number': 'NumeroDocumento',
                    'first_name': 'Nombre',
                    'last_name': 'Apellido',
                    'phone': 'Telefono',
                    'address': 'Direccion',
                    'email': 'correo@ejemplo.com',
                },
                'items': [
                    {
                        'reference': 'SKU123',
                        'name': 'Producto de ejemplo',
                        'price': 100.0,
                        'discount': 0.0,
                        'subtotal': 100.0,
                        'tax': 12.0,
                        'total': 112.0,
                    }
                ],
                'amount_total': 112.0,
            }]
        }

        # Obtengo las facturas
        response = self.env['http.request'].sudo().get('/invoices')

        # Verifico el código de estado y los datos devueltos
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'status': 'success',
            'data': [{
                'id': 1,
                'createtime': '2024-03-25',
                'document_number': 'INV/001',
                'date': '2024-03-25',
                'customer': {
                    'document_type': 'TipoDocumento',
                    'document_number': 'NumeroDocumento',
                    'first_name': 'Nombre',
                    'last_name': 'Apellido',
                    'phone': 'Telefono',
                    'address': 'Direccion',
                    'email': 'correo@ejemplo.com',
                },
                'items': [
                    {
                        'reference': 'SKU123',
                        'name': 'Producto de ejemplo',
                        'price': 100.0,
                        'discount': 0.0,
                        'subtotal': 100.0,
                        'tax': 12.0,
                        'total': 112.0,
                    }
                ],
                'amount_total': 112.0,
            }]
        })

    @patch('requests.post')
    def test_post_invoice(self, mocked_post):
        # Mockeo la respuesta de la API
        mocked_post.return_value.status_code = 200
        mocked_post.return_value.json.return_value = {
            'status': 'success',
            'message': 'Invoice created',
            'data': {
                'id': 1,
                'createtime': '2024-03-25',
                'document_number': 'INV/001',
                'date': '2024-03-25',
                'customer': {
                    'document_type': 'TipoDocumento',
                    'document_number': 'NumeroDocumento',
                    'first_name': 'Nombre',
                    'last_name': 'Apellido',
                    'phone': 'Telefono',
                    'address': 'Direccion',
                    'email': 'correo@ejemplo.com',
                },
                'items': [
                    {
                        'reference': 'SKU123',
                        'name': 'Producto de ejemplo',
                        'price': 100.0,
                        'discount': 0.0,
                        'subtotal': 100.0,
                        'tax': 12.0,
                        'total': 112.0,
                    }
                ],
                'amount_total': 112.0,
            }
        }

        # Datos de prueba para la solicitud POST
        data = {
            'customer': {
                'document_type': 'TipoDocumento',
                'document_number': 'NumeroDocumento',
                'first_name': 'Nombre',
                'last_name': 'Apellido',
                'phone': 'Telefono',
                'address': 'Direccion',
                'email': 'correo@ejemplo.com',
            },
            'items': [
                {
                    'SKU': 'SKU123',
                    'discount': 0.0,
                    'quantity': 1
                }
            ]
        }

        # Hago la solicitud POST
        response = self.env['http.request'].sudo().post('/invoices', json=data)

        # Verifico si la solicitud fue exitosa y si devuelve los datos esperados
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'status': 'success',
            'message': 'Invoice created',
            'data': {
                'id': 1,
                'createtime': '2024-03-25',
                'document_number': 'INV/001',
                'date': '2024-03-25',
                'customer': {
                    'document_type': 'TipoDocumento',
                    'document_number': 'NumeroDocumento',
                    'first_name': 'Nombre',
                    'last_name': 'Apellido',
                    'phone': 'Telefono',
                    'address': 'Direccion',
                    'email': 'correo@ejemplo.com',
                },
                'items': [
                    {
                        'reference': 'SKU123',
                        'name': 'Producto de ejemplo',
                        'price': 100.0,
                        'discount': 0.0,
                        'subtotal': 100.0,
                        'tax': 12.0,
                        'total': 112.0,
                    }
                ],
                'amount_total': 112.0,
            }
        })
    
    @patch('requests.delete')
    def test_delete_invoice(self, mocked_delete):
        # Mockeo la respuesta de la API
        mocked_delete.return_value.status_code = 200
        mocked_delete.return_value.json.return_value = {
            'status': 'success',
            'message': 'Invoice deleted',
            'data': {
                'id': self.invoice.id,
                'createtime': str(self.invoice.create_date),
                'document_number': self.invoice.name.split(' ')[1],
                'date': str(self.invoice.date),
                'customer': {
                    'document_type': self.invoice.partner_id.l10n_latam_identification_type_id.name,
                    'document_number': self.invoice.partner_id.vat,
                    'first_name': self.invoice.partner_id.name,
                    'last_name': self.invoice.partner_id.name,
                    'phone': self.invoice.partner_id.phone,
                    'address': self.invoice.partner_id.street,
                    'email': self.invoice.partner_id.email,
                },
                'items': [
                    {
                        'reference': line.product_id.default_code,
                        'name': line.product_id.name,
                        'price': line.price_total,
                        'discount': line.discount,
                        'subtotal': line.price_subtotal,
                        'tax': line.price_subtotal * line.tax_ids[0].amount / 100,
                        'total': line.price_total,
                    } for line in self.invoice.invoice_line_ids
                ],
                'amount_total': self.invoice.amount_total,
            }
        }

        # Hago la solicitud DELETE
        response = self.env['http.request'].sudo().delete(f'/invoices/{self.invoice.id}')

        # Verifico si la solicitud fue exitosa y si devuelve los datos esperados
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'status': 'success',
            'message': 'Invoice deleted',
            'data': {
                'id': self.invoice.id,
                'createtime': str(self.invoice.create_date),
                'document_number': self.invoice.name.split(' ')[1],
                'date': str(self.invoice.date),
                'customer': {
                    'document_type': self.invoice.partner_id.l10n_latam_identification_type_id.name,
                    'document_number': self.invoice.partner_id.vat,
                    'first_name': self.invoice.partner_id.name,
                    'last_name': self.invoice.partner_id.name,
                    'phone': self.invoice.partner_id.phone,
                    'address': self.invoice.partner_id.street,
                    'email': self.invoice.partner_id.email,
                },
                'items': [
                    {
                        'reference': line.product_id.default_code,
                        'name': line.product_id.name,
                        'price': line.price_total,
                        'discount': line.discount,
                        'subtotal': line.price_subtotal,
                        'tax': line.price_subtotal * line.tax_ids[0].amount / 100,
                        'total': line.price_total,
                    } for line in self.invoice.invoice_line_ids
                ],
                'amount_total': self.invoice.amount_total,
            }
        })