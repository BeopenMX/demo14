import base64

from odoo import models, fields, api, _


# 'mkt','monterrey','guadalajara','leon','mexico','puebla'

class Segmentos(models.Model):
    _name = "segmento"

    name = fields.Char(string="Nombre", copy=False)
    segmento_lines = fields.One2many('segmento.line', 'segmento_id', string='Region Lines', copy=True, auto_join=True)
    total_amount = fields.Float(string="Total", copy=False, compute="_compute_total_amount")

    @api.depends('segmento_lines.value')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(record.mapped('segmento_lines.value'))


class SegmentosLine(models.Model):
    _name = "segmento.line"

    segmento_id = fields.Many2one('segmento', string="Segmento", ondelete="cascade")
    value = fields.Float(string="Valor", copy=False)
    region = fields.Selection(string="Region", selection=[('mkt', 'MKT'), ('monterrey', 'Monterrey'),
                                                          ('guadalajara', 'Guadalajara'), ('leon', 'Leon'),
                                                          ('mexico', 'Mexico'), ('puebla', 'Puebla'), ],
                              required=False)
    display_name = fields.Char(string="Display name", readonly=True, store=True,
                               compute="_compute_dispay_name", )

    @api.depends('segmento_id.name', 'region')
    def _compute_dispay_name(self):
        for record in self:
            region = dict(self._fields['region'].selection).get(record.region) if record.region else ''
            record.display_name = '%s (%s)' % (record.segmento_id.name, region)

    def name_get(self):
    	return [(segmento.id, '%s' % segmento.display_name) for segmento in self]