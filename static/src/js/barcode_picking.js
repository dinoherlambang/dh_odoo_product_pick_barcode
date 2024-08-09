odoo.define('dh_product_pick_barcode.barcode_picking', function (require) {
    "use strict";

    var core = require('web.core');
    var FormController = require('web.FormController');
    var _t = core._t;

    FormController.include({
        custom_events: _.extend({}, FormController.prototype.custom_events, {
            barcode_scanned: '_onBarcodeScanned',
        }),

        _onBarcodeScanned: function (ev) {
            var self = this;
            var barcode = ev.data.barcode;
            var quantity = parseInt($('.o_quantity_input').val()) || 1;

            this.do_notify(_t("Scanning"), _t("Processing barcode: ") + barcode, false);

            var model = this.model;
            var method = this.modelName === 'stock.picking' && this.record.data.picking_type_code === 'incoming'
                ? 'process_barcode_from_ui_incoming'
                : 'process_barcode_from_ui';

            this._rpc({
                model: model,
                method: method,
                args: [this.handle, barcode, quantity],
            }).then(function (result) {
                if (result.success) {
                    self.do_notify(_t("Success"), result.message, false);
                    self.reload();
                } else {
                    if (result.no_product_found) {
                        self.do_warn(_t("Product Not Found"), result.message);
                    } else if (result.excess) {
                        self.do_warn(_t("Excess Quantity"), result.message);
                    } else if (result.product_not_in_picking) {
                        self.do_warn(_t("Product Not in Picking"), result.message);
                    } else if (result.unexpected_product) {
                        self.do_warn(_t("Unexpected Product"), result.message);
                    } else {
                        self.do_warn(_t("Warning"), result.message);
                    }
                }
            }).guardedCatch(function (error) {
                self.do_warn(_t("Error"), _t("An error occurred while processing the barcode."));
            });
        }
    });
});