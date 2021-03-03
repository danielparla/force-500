from odoo import api, fields, models, exceptions, _


class SevoAgent(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'force500.agent'
    _description = 'Sevostudio Fire Extinguishing Agents'
    _check_company_auto = True
    _order = 'name desc'

    name = fields.Char(string="Name",
                       required=True)
    description = fields.Text(string="Description")
    responsible_lab = fields.Many2one(
        'res.partner',
        string="Laboratory",
        required=True,
        domain=[('category_id.name', 'ilike', "Laboratory")])