# -*- coding: utf-8 -*-
import xlrd
import shutil
import logging
from odoo import models, fields, api, _, tools
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class StockPickingWNI(models.Model):
    _inherit = 'stock.picking'

    # @api.onchange('pack_operation_product_ids')
    # def _onchange_origin(self):
    #     # super(StockPicking, self)._onchange_origin()
    #     if self.pack_operation_product_ids:
    #         x = 0
    #         for line in self.pack_operation_product_ids:
    #             if x: break
    #             if line.qty_done > line.product_qty:
    #                 raise UserError(_("Error: La cantidad recibida debe ser igual a la cantidad por hacer! "))
    #             x += 1

    def cargar_series(self):
        attachment_obj = self.env['ir.attachment']
        attachments = []
        company_id = self.company_id.id
        stockpicking = self
        # fname_stockpicking = stockpicking.fname_stockpicking and stockpicking.fname_stockpicking or ''
        adjuntos = attachment_obj.search([('res_model', '=', 'stock.picking'),
                                          ('res_id', '=', stockpicking.id),
                                          ('name', 'like', '%.xls')])
        # raise UserError(_("Error:Hay \n%s!") % (stockpicking.id))
        _logger.error(" archivos ajuntos")
        count = len(adjuntos)

        if count >= 2 or count == 0:
            raise UserError(_(
                "Error:Hay \n%s archivos adjuntos, por favor adjunte el archivo o sólo deje el archivo para cargar "
                "sus series!") % (
                                count))
        else:
            if count == 1:

                _logger.error("hay 1 archivo ajuntos")
                db_name = self._cr.dbname
                # destino = "/var/lib/odoo/filestore/" +db_name +"/"  + adjuntos.store_fname+".xls";
                # destino = "/home/user/.local/share/Odoo/filestore/" + db_name + "/" + adjuntos.store_fname + ".xls";--> Local
                destino = "/home/odoo/data/filestore/" + db_name + "/" + adjuntos.store_fname + ".xls";
                # shutil.copy('/home/user/.local/share/Odoo/filestore/' + db_name + "/" + adjuntos.store_fname,destino)-->
                shutil.copy('/home/odoo/data/filestore/' + db_name + "/" + adjuntos.store_fname,
                            destino)
                # shutil.copy('/var/lib/odoo/filestore/' +db_name +"/"  + adjuntos.store_fname, destino)
                _logger.info("ARCHIVO COPIADO")
                # book = xlrd.open_workbook(
                # "/home/user/.local/share/Odoo/filestore/" + db_name + "/" + adjuntos.store_fname + ".xls")-->
                book = xlrd.open_workbook(
                    "/home/odoo/data/filestore/" + db_name + "/" + adjuntos.store_fname + ".xls")
                # book = xlrd.open_workbook("/var/lib/odoo/filestore/" +db_name +"/"  + adjuntos.store_fname+".xls")
                # serie_obj = self.pool.get('serie_tmp')
                sheet = book.sheet_by_index(0)

                nrows = sheet.nrows
                ncols = sheet.ncols
                _logger.info(nrows)
                _logger.info(ncols)
                for i in range(nrows):

                    _logger.info(sheet.cell_value(i, 1))
                    _logger.info(sheet.cell_value(i, 2))
                    serie = sheet.cell_value(i, 0)
                    codigo = sheet.cell_value(i, 1)
                    producto = sheet.cell_value(i, 2)

                    # if sheet.cell_value(i,4) == '':
                    #   raise UserError(_("Error:vacio columna 5 \n%s!") % ())
                    # serie_obj = self.env['load_series']
                    # self.write({'xls_file_signed_index': adjuntos.store_fname})

                    ser = self.env['product.template'].search([('default_code', '=', codigo)])
                    if ser.default_code == codigo:

                        na = self.env['product.template'].search([('name', '=', producto)])
                        if na.name == producto:
                            if self.move_ids_without_package:
                                for l in self.move_ids_without_package:
                                    if l.product_id.default_code == codigo:
                                        asignada = False
                                        for x in l.move_line_ids:

                                            if (x.lot_name == False or x.lot_name == '') and asignada == False:
                                                print("averts", serie, asignada)
                                                x.lot_name = serie
                                                x.qty_done = 1
                                                asignada = True
                                                print("asiganda", serie, asignada)


    def update_series(self):

        attachment_obj = self.env['ir.attachment']
        attachments = []
        company_id = self.company_id.id
        stockpicking = self
        # fname_stockpicking = stockpicking.fname_stockpicking and stockpicking.fname_stockpicking or ''
        adjuntos = attachment_obj.search([('res_model', '=', 'stock.picking'),
                                          ('res_id', '=', stockpicking.id),
                                          ('name', 'like', '%.xls')])
        # raise UserError(_("Error:Hay \n%s!") % (stockpicking.id))
        _logger.error(" archivos ajuntos")
        count = len(adjuntos)
        if count >= 2 or count == 0:
            raise UserError(_(
                "Error:Hay \n%s archivos adjuntos, por favor adjunte el archivo o sólo deje el archivo para cargar "
                "sus series!") % count)
        else:
            self.move_ids_without_package.move_line_ids.lot_name = False
            self.cargar_series()
