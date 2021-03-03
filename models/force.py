# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class SevoForceProject(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'force500.project'
    _description = 'Sevostudio force500 Projects'
    _check_company_auto = True
    _order = 'name desc'

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('force500.project.sequence') or _('New')
            result = super(SevoForceProject, self).create(vals)
            return result

    name = fields.Char(string='Project Reference',
                       required=True,
                       copy=False,
                       readonly=True,
                       index=True,
                       default=lambda self: _('New'))
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent')],
        string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    customer_id = fields.Many2one('res.partner',
                                  ondelete='restrict',
                                  string="Customer",
                                  index=True, required=True,
                                  default=lambda self: self.env.user.partner_id)
    salesperson_id = fields.Many2one(related='customer_id.user_id', string="Salesperson")
    user_id = fields.Many2one('res.users',
                              string='System User',
                              index=True, required=True,
                              default=lambda self: self.env.user,
                              help="Person entering the data")

    # @api.depends('room_ids')
    # def _regul_name(self):
    #    for r in self:
    #        for room in r.room_ids:
    #            name = room.regulation_name
    #        return name

    related_people = fields.Text(string="Created by")
    # regulation_name = fields.Char(string="Regulation",
    #                              default=_regul_name)

    date = fields.Datetime("Date current", required=True, readonly=False, select=True,
                           default=lambda self: fields.datetime.now())
    location = fields.Char(string="Building Location", required=True)
    building_reference = fields.Char(string="Building Reference")
    so_extern = fields.Char(string="SO Extern")
    room_ids = fields.One2many('force500.room', 'project_id', string="Rooms", copy=True)

    room_account = fields.Integer(string="Nº Rooms", compute='calc_room_sum')
    total_rooms_volume = fields.Float(string="Total Rooms Volume",
                                      compute='calc_room_sum')

    @api.onchange('room_ids')
    def calc_room_sum(self):
        for r in self:
            r.room_account = 0
            r.total_rooms_volume = 0
            r.total_nozzles = 0
            r.agent_kgs_max = 0
            for line in r.room_ids:
                r.room_account += 1
                r.total_rooms_volume += line.total_volume
                r.total_nozzles += line.total_suggest_nozzles
                r.agent_kgs_max += line.agent_kgs_max

    valves_id = fields.Many2one('product.product', string="Valves",
                                required=True)

    # agent_id = fields.Many2one('force500.agent', string="Agent Type", required=True)
    # agent_kgs = fields.Float(string="Agent (Kg.)")

    agent_kgs_adjusted = fields.Float(string="Adjusted Agent (Kg.)",
                                      compute='calc_adj_kgs')

    @api.onchange('agent_kgs_max')
    def calc_adj_kgs(self):
        for r in self:
            r.agent_kgs_adjusted = r.agent_kgs_max * 1.03

    agent_kgs_max = fields.Float(string="Max Agent (Kg.)",
                                 compute='calc_room_sum')

    flooding_factor = fields.Float(string="Flooding Factor (Kg/m3)",
                                   compute='calc_flooding')

    @api.onchange('agent_kgs_max', 'total_rooms_volume')
    def calc_flooding(self):
        for r in self:
            if r.total_rooms_volume > 0:
                r.flooding_factor = r.agent_kgs_max / r.total_rooms_volume

    total_nozzles = fields.Integer(string="Total Nozzles",
                                   required=True,
                                   compute='calc_room_sum')
    cylinder_id = fields.Many2one('force500.cylinder', string="Cylinder Size")  # Size
    cylinder_quantity = fields.Integer(string="Quantity of Cylinders",
                                       compute='calc_num_cyl')

    @api.depends('agent_kgs_max', 'max_filling')
    def calc_num_cyl(self):
        for r in self:
            if r.max_filling:
                r.cylinder_quantity = r.agent_kgs_max / r.max_filling

    #TODO hay que comprobar antes si quieren welded o seamless
    """def inverse_num_cyl(self):
        for r in self:
            if r.cylinder_quantity > 0:
                if r.manufacturing == 'welded':
                    weight = r.agent_kgs_max / r.cylinder_quantity
                    if weight > 180 :
                        print('ERROR AUMENTE LAS BOTELLAS')
                    if 180 >= weight > """


    cylinder_fill = fields.Float(string="Cylinder Fill (Kg./each)",
                                 related='cylinder_id.cyl_size')  # llenado
    min_filling = fields.Float(string="Min Filling Quantity",
                               related='cylinder_id.allowable_min')
    max_filling = fields.Float(string="Max Filling Quantity",
                               related='cylinder_id.allowable_max')
    cyl_manufacturing = fields.Selection([
        ('welded', "Welded"),
        ('seamless', "Seamless")],
        string="Manufacturing",
        default='welded')
    pressure = fields.Float(string="Cylinder Pressure",
                            required=True)
    order_line_ids = fields.Char(string="Materials")
    advice = fields.Char(string="Advice")
