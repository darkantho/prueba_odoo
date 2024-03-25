odoo.define('modulo_uom_pos.UOMButton', function(require) {
	'use strict';

	const PosComponent = require('point_of_sale.PosComponent');
	const ProductScreen = require('point_of_sale.ProductScreen');
	const Registries = require('point_of_sale.Registries');
	const { useListener } = require("@web/core/utils/hooks");
	let core = require('web.core');
	let _t = core._t;

	class UOMButton extends PosComponent {
		setup() {
			super.setup();
			useListener('click', this.onClick);
		}

		get filter_uom(){
            var list = []
            var currentOrder = this.env.pos.get_order();
            var selected_line = currentOrder.get_selected_orderline().product.product_tmpl_id;
            var selected_orderline = currentOrder.get_selected_orderline();
            if(this.env.pos.point_of_sale_uom){
                for(var uom_id of this.env.pos.point_of_sale_uom){
                    if(selected_line == uom_id.product_uom_line_id[0]){
                        list.push({
                            id: uom_id.unit_of_measure_id[0],
                            label : uom_id.unit_of_measure_id[1],
                            sale_price : uom_id.sale_price,
                            symbol: this.env.pos.currency.symbol,
                            selected_orderline : selected_orderline,
                        });
                    }
                }
            }
            return list;
        }

		async onClick() {
		    if(this.env.pos.get_order().get_selected_orderline()){
		        if(this.env.pos.get_order().get_selected_orderline().product.point_of_sale_uom){
		            if(this.env.pos.get_order().get_selected_orderline().product.product_uom_ids.length > 0){
		                const { confirmed } = await this.showPopup('MultiUOMPopup', {
                            title: this.env._t("Product Multi UOM"),
                            list: this.filter_uom,
                        });
                    } else {
                        this.showNotification(_.str.sprintf(this.env._t('No hay otra UM en este producto.')),2000);
                        return;
                    }
		        } else {
		            this.showNotification(_.str.sprintf(this.env._t('No tiene unidades de medida')),2000);
		            return;
		        }
		    } else {
		        this.showNotification(_.str.sprintf(this.env._t('agrege un producto primero')),2000);
		        return;
		    }
		}
	}
	UOMButton.template = 'UOMButton';
	ProductScreen.addControlButton({
		component: UOMButton,
		condition: function() {
			return this.env.pos.config.product_multi_uom;
		},
	});
	Registries.Component.add(UOMButton);
	return UOMButton;
});