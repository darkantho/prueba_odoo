odoo.define('modulo_uom_pos.MultiUOMPopup', function(require) {
  'use strict';

  const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
  const Registries = require('point_of_sale.Registries');
  const { useListener } = require("@web/core/utils/hooks");
  const { useState } = owl;

  class MultiUOMPopup extends AbstractAwaitablePopup {
      setup() {
          super.setup();
      }

      selectItem(itemId, item_sale_price, item_label, selected_orderline) {
          if (this.env.pos.get_order().get_orderlines().length > 1){
              for(var line of this.env.pos.get_order().get_orderlines()){
                  if(line.get_product().id == selected_orderline.get_product().id){
                      if(line.uom_id == itemId && line.price == item_sale_price){
                          if(line.price_manually_set == true){
                              var final_qty = line.quantity + selected_orderline.quantity;
                              line.set_quantity(final_qty);
                              this.env.pos.get_order().remove_orderline(selected_orderline);
                          }
                          this.confirm();
                      }
                  }
              }
          }
          selected_orderline.price_manually_set = true;
          selected_orderline.set_unit_price(item_sale_price);
          selected_orderline.set_custom_uom_id(itemId);
          this.confirm();
      }
      cancel() {
          this.env.posbus.trigger('close-popup', {
              popupId: this.props.id,
              response: { confirmed: false, payload: null },
          });
      }
  }
  MultiUOMPopup.template = 'MultiUOMPopup';
  MultiUOMPopup.defaultProps = {
      confirmText: 'Select',
      cancelText: 'Cancel',
      body: '',
  };
  Registries.Component.add(MultiUOMPopup);
  return MultiUOMPopup;
});
