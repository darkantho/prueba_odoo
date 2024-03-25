odoo.define('modulo_uom_pos_cost_price.SearchCostPriceOrder', function (require) {
  "use strict";
  
  var models = require('point_of_sale.models');
  var utils = require('web.utils');
  var { PosGlobalState, Order, Orderline} = require('point_of_sale.models');
  const Registries = require('point_of_sale.Registries');
  var core = require('web.core');
  
  const PosGiftCardPosGlobalState = (PosGlobalState) => class PosGiftCardPosGlobalState extends PosGlobalState {
      constructor(obj) {
          super(obj);
      }
      async _processData(loadedData) {
          await super._processData(...arguments);
          this.point_of_sale_uom = loadedData['product.template.uom.line'];
      }
  }
  Registries.Model.extend(PosGlobalState, PosGiftCardPosGlobalState);
  
  const multiUOM = (Orderline) => class multiUOM extends Orderline {
      constructor(obj, options) {
          super(...arguments);
          this.uom_id = this.uom_id || this.product.uom_id[0]
      }
      init_from_JSON (json) {
          super.init_from_JSON(...arguments);
          this.uom_id = json.uom_id;
      }
      set_custom_uom_id(uom_id) {
          this.uom_id = uom_id;
      }
      get_custom_uom_id() {
          return this.uom_id;
      }
      get_unit() {
          var res = super.get_unit(...arguments);
          var unit_id = this.uom_id;
          if(!unit_id) {
              return res;
          }
          unit_id = unit_id[0] || unit_id;
          if(!this.pos) {
              return undefined;
          }
          return this.pos.units_by_id[unit_id];
      }
      export_as_JSON() {
          const json = super.export_as_JSON(...arguments);
          json.uom_id = this.uom_id;
          return json;
      }
  }
  Registries.Model.extend(Orderline, multiUOM);
  
  });