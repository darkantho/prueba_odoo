# -*- coding: utf-8 -*-
{
    'name': "modulo_uom_pos",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'point_of_sale'],
    
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/point_of_sale.xml',
        'views/pos_config.xml',
    ],
    'assets':{
        'point_of_sale.assets':[
        'modulo_uom_pos/static/src/js/models.js',   
        'modulo_uom_pos/static/src/js/Screens/ProductScreen/ControlButton/UOMButton.js',
        'modulo_uom_pos/static/src/js/Screens/Popups/MultiUOMPopup.js',
        'modulo_uom_pos/static/src/xml//**/*',

        ]
    },
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}
