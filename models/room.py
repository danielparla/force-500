from odoo import api, fields, models, exceptions, _


class SevoRoom(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'force500.room'
    _description = 'Sevostudio rooms'
    _check_company_auto = True
    _order = 'name desc'

    # Total measures

    @api.onchange('ceiling', 'sub_floor', 'room_height', 'roof_height', 'floor_height')
    def calc_total_height(self):
        for r in self:
            r.total_height = r.room_height
            if r.ceiling:
                r.total_height += r.roof_height
            if r.sub_floor:
                r.total_height += r.floor_height

    @api.onchange('ceiling', 'sub_floor', 'room_volume', 'roof_volume', 'floor_volume')
    def calc_total_volume(self):
        for r in self:
            r.total_volume = r.room_volume
            if r.ceiling:
                r.total_volume += r.roof_volume
            if r.sub_floor:
                r.total_volume += r.floor_volume

    @api.onchange('ceiling', 'sub_floor', 'room_deduct', 'roof_deduct', 'floor_deduct')
    def calc_total_deduct(self):
        for r in self:
            r.total_deduct = r.room_deduct
            if r.ceiling:
                r.total_deduct += r.roof_deduct
            if r.sub_floor:
                r.total_deduct += r.floor_deduct

    @api.onchange('ceiling', 'sub_floor', 'room_final_volume', 'roof_final_volume', 'floor_final_volume')
    def calc_total_fin_volume(self):
        for r in self:
            r.total_final_volume = r.room_final_volume
            if r.ceiling:
                r.total_final_volume += r.roof_final_volume
            if r.sub_floor:
                r.total_final_volume += r.floor_final_volume

    @api.onchange('ceiling', 'sub_floor', 'room_min_nozzles', 'roof_min_nozzles', 'floor_min_nozzles')
    def calc_total_min_nozz(self):
        for r in self:
            r.total_min_nozzles = r.room_min_nozzles
            if r.ceiling:
                r.total_min_nozzles += r.roof_min_nozzles
            if r.sub_floor:
                r.total_min_nozzles += r.floor_min_nozzles

    @api.onchange('ceiling', 'sub_floor', 'room_suggest_nozzles', 'roof_suggest_nozzles', 'floor_suggest_nozzles')
    def calc_total_sug_nozz(self):
        for r in self:
            r.total_suggest_nozzles = r.room_suggest_nozzles
            if r.ceiling:
                r.total_suggest_nozzles += r.roof_suggest_nozzles
            if r.sub_floor:
                r.total_suggest_nozzles += r.floor_suggest_nozzles

    @api.onchange('altitude')
    def calc_correct_factor(self):
        for r in self:
            if r.altitude <= -1000:
                r.correction = 1.13
            elif -1000 < r.altitude < 1000:
                r.correction = 1
            elif 1000 <= r.altitude < 1500:
                r.correction = 0.885
            elif 1500 <= r.altitude < 2000:
                r.correction = 0.83
            elif 2000 <= r.altitude < 2500:
                r.correction = 0.785
            elif 2500 <= r.altitude < 3000:
                r.correction = 0.735
            elif 3000 <= r.altitude < 3500:
                r.correction = 0.69
            elif 3500 <= r.altitude < 4000:
                r.correction = 0.65
            elif 4000 <= r.altitude < 4500:
                r.correction = 0.61
            elif 4500 < r.altitude:
                r.correction = 0.565

    @api.onchange('fire_type1', 'fire_type2', 'regulation_name')
    def calc_concent(self):
        for r in self:
            r.concentration = 4.5
            if r.regulation_name is False:
                break
            elif 'EN15004' in r.regulation_name:
                if r.fire_type1 == 'a':
                    r.concentration = 5.3
                elif r.fire_type1 == 'b':
                    r.concentration = 5.85
                elif r.fire_type1 == 'c':
                    r.concentration = 0
                elif r.fire_type1 == 'd':
                    r.concentration = 5.6
            elif 'NFPA' in r.regulation_name:
                if r.fire_type2 == 'a':
                    r.concentration = 4.5
                elif r.fire_type2 == 'b':
                    r.concentration = 5.9
                elif r.fire_type2 == 'c':
                    r.concentration = 4.7

    def inverse_concent(self):
        for r in self:
            r.concentration = r.concentration

    name = fields.Char(string="Name",
                       required=True)

    @api.onchange('kgs_room_nozzle', 'kgs_roof_nozzle', 'kgs_floor_nozzle')
    def calc_max_agent(self):
        for r in self:
            r.agent_kgs_max = r.kgs_room_nozzle + r.kgs_roof_nozzle + r.kgs_floor_nozzle

    def _default_force500_project(self):
        project = self.env['force500.project'].search([('name', '=', 'SevoForceProject')], limit=1).id
        print(project)
        return project

    project_id = fields.Many2one('force500.project', string="Project",
                                 default=_default_force500_project,
                                 index=True, readonly=True)
    regulation_id = fields.Many2one('sevostudio.regulation', string="Regulation",
                                    required=True)
    regulation_name = fields.Char(string="Regulation", related='regulation_id.name')

    total_surface = fields.Float(string="Surface Room (m2)",
                                 related='room_surface')
    total_height = fields.Float(string="Total Height (m)",
                                compute='calc_total_height')
    total_volume = fields.Float(string="Total Volume (m3)",
                                compute='calc_total_volume')
    total_deduct = fields.Float(string="Total Deductions (m3)",
                                compute='calc_total_deduct')
    total_final_volume = fields.Float(string="Total Final Volume (m3)",
                                      compute='calc_total_fin_volume')
    total_min_nozzles = fields.Integer(string="Total Min Nozzles",
                                       compute='calc_total_min_nozz')
    total_suggest_nozzles = fields.Integer(string="Total Suggest Nozzles",
                                           compute='calc_total_sug_nozz')
    agent_kgs_max = fields.Float(string='Max Agent (Kg.)',
                                 compute='calc_max_agent')
    altitude = fields.Float(string="Enclosure Altitude (m)",
                            required=True)
    correction = fields.Float(string="Correction Factor",
                              compute='calc_correct_factor')
    temperature = fields.Float(string="Enclosure Temperature (ºC)",
                               required=True)
    fire_type1 = fields.Selection([
        ('a', 'Type A'),
        ('b', 'Type B'),
        ('c', 'Type C (Special Risk)'),
        ('d', 'Type A+')],
        string="Fire Type",
        defutl='a')
    fire_type2 = fields.Selection([
        ('a', 'Type A'),
        ('b', 'Type B'),
        ('c', 'Type C (Special Risk)')],
        string="Fire Type",
        defutl='a')
    concentration = fields.Float(string="Predicted Design Concentration (%)",
                                 default=4.5,
                                 compute='calc_concent',
                                 inverse='inverse_concent')

    """-----------------------ROOM measures--------------------"""

    # SURFACE
    @api.onchange('room_width', 'room_length')
    def calc_room_surface(self):
        for r in self:
            r.room_surface = r.room_width * r.room_length

    def inverse_room_surface(self):
        for r in self:
            r.room_surface = r.room_surface

    # VOLUME
    @api.onchange('room_height', 'room_surface')
    def calc_room_volume(self):
        for r in self:
            r.room_volume = r.room_surface * r.room_height

    # FINAL VOLUME
    @api.onchange('room_volume', 'room_deduct')
    def calc_room_final_volume(self):
        for r in self:
            r.room_final_volume = r.room_volume - r.room_deduct

    # MIN NOZZLES
    @api.onchange('room_width', 'room_length', 'room_surface', 'room_height')
    def calc_min_room_nozzles(self):
        for r in self:
            if r.room_width > 9.8 or r.room_length > 9.8:
                nozz_width = 0
                nozz_length = 0
                if r.room_width > 9.8:
                    nozz_width = int(r.room_width / 9.81) + 1
                if r.room_length > 9.8:
                    nozz_length = int(r.room_length / 9.81) + 1
                r.room_min_nozzles = nozz_width + nozz_length
            else:
                nozz_area = int(r.room_surface / 96.05) + 1
                nozz_height = int(r.room_height / 5.01) + 1
                r.room_min_nozzles = nozz_area * nozz_height

    # Suggest NOZZLES
    @api.onchange('room_min_nozzles')
    def calc_sugg_nozz_room(self):
        for r in self:
            r.room_suggest_nozzles = r.room_min_nozzles

    def inverse_sugg_nozz_room(self):
        for r in self:
            r.room_suggest_nozzles = r.room_suggest_nozzles

    # KGS / NOZZLES
    @api.onchange('correction', 'concentration', 'room_final_volume', 'temperature')
    def calc_kgs_room_nozz(self):
        for r in self:
            r.kgs_room_nozzle = (r.correction * 1.01 * r.concentration * r.room_final_volume) / (
                    (100 - r.concentration) * (0.0664 + (0.000274 * r.temperature)))

    room_width = fields.Float(string="Width (m)")
    room_length = fields.Float(string="Length (m)")
    room_surface = fields.Float(string="Surface (m2)",
                                required=True,
                                compute='calc_room_surface',
                                inverse='inverse_room_surface')
    room_height = fields.Float(string="Height (m)",
                               required=True)
    room_volume = fields.Float(string="Volume (m3)",
                               required=True,
                               default=0,
                               compute='calc_room_volume')
    room_deduct = fields.Float(string="Deductions (m3)", default=0)
    room_final_volume = fields.Float(string="Final Volume (m3)",
                                     compute='calc_room_final_volume')
    room_min_nozzles = fields.Integer(string="Min Nozzles",
                                      required=True,
                                      compute='calc_min_room_nozzles')
    room_suggest_nozzles = fields.Integer(string="Suggest Nozzles",
                                          compute='calc_sugg_nozz_room',
                                          inverse='inverse_sugg_nozz_room')
    kgs_room_nozzle = fields.Float(string="Each Nozzle (Kg)", default=0,
                                   compute='calc_kgs_room_nozz')
    room_image_drawing = fields.Binary(string="Drawing")
    room_details = fields.Text(string="Details")
    ceiling = fields.Boolean(string="Ceiling")
    sub_floor = fields.Boolean(string="Sub-Floor")

    # ROOF measures
    # SURFACE
    @api.onchange('roof_width', 'roof_length')
    def calc_roof_surface(self):
        for r in self:
            r.roof_surface = r.roof_width * r.roof_length

    def inverse_roof_surface(self):
        for r in self:
            r.roof_surface = r.roof_surface

    # VOLUME
    @api.onchange('roof_height', 'roof_surface')
    def calc_roof_volume(self):
        for r in self:
            r.roof_volume = r.roof_surface * r.roof_height

    # FINAL VOLUME
    @api.onchange('roof_volume', 'roof_deduct')
    def calc_roof_final_volume(self):
        for r in self:
            r.roof_final_volume = r.roof_volume - r.roof_deduct

    # MIN NOZZLES
    @api.onchange('roof_width', 'roof_length', 'roof_surface', 'roof_height')
    def calc_min_roof_nozzles(self):
        for r in self:
            if r.roof_width > 9.8 or r.roof_length > 9.8:
                nozz_width = 0
                nozz_length = 0
                if r.roof_width > 9.8:
                    nozz_width = int(r.roof_width / 9.81) + 1
                if r.roof_length > 9.8:
                    nozz_length = int(r.roof_length / 9.81) + 1
                r.roof_min_nozzles = nozz_width + nozz_length
            else:
                nozz_area = int(r.roof_surface / 96.05) + 1
                nozz_height = int(r.roof_height / 5.01) + 1
                r.roof_min_nozzles = nozz_area * nozz_height

    # Suggest NOZZLES
    @api.onchange('roof_min_nozzles')
    def calc_sugg_nozz_roof(self):
        for r in self:
            r.roof_suggest_nozzles = r.roof_min_nozzles

    def inverse_sugg_nozz_roof(self):
        for r in self:
            r.roof_suggest_nozzles = r.roof_suggest_nozzles

    # KGS / NOZZLES
    @api.onchange('correction', 'concentration', 'roof_volume', 'temperature')
    def calc_kgs_roof_nozz(self):
        for r in self:
            r.kgs_roof_nozzle = (r.correction * 1.01 * r.concentration * r.roof_volume) / (
                    (100 - r.concentration) * (0.0664 + (0.000274 * r.temperature)))

    roof_width = fields.Float(string="Width (m)")
    roof_length = fields.Float(string="Length (m)")
    roof_surface = fields.Float(string="Surface (m2)",
                                compute='calc_roof_surface',
                                inverse='inverse_roof_surface')
    roof_height = fields.Float(string="Height (m)")
    roof_volume = fields.Float(string="Volume (m3)",
                               compute='calc_roof_volume', default=0)
    roof_deduct = fields.Float(string="Deductions (m3)", default=0)
    roof_final_volume = fields.Float(string="Final Volume (m3)",
                                     related='roof_volume',
                                     compute='calc_roof_final_volume')
    roof_min_nozzles = fields.Integer(string="Min Nozzles",
                                      compute='calc_min_roof_nozzles')
    roof_suggest_nozzles = fields.Integer(string="Suggest Nozzles",
                                          compute='calc_sugg_nozz_roof',
                                          inverse='inverse_sugg_nozz_roof')
    kgs_roof_nozzle = fields.Float(string="Each Nozzle (Kg)", compute='calc_kgs_roof_nozz')
    roof_image_drawing = fields.Binary(string="Drawing")
    roof_details = fields.Text(string="Details")

    # FLOOR measures
    # SURFACE
    @api.onchange('floor_width', 'floor_length')
    def calc_floor_surface(self):
        for r in self:
            r.floor_surface = r.floor_width * r.floor_length

    def inverse_floor_surface(self):
        for r in self:
            r.floor_surface = r.floor_surface

    # VOLUME
    @api.onchange('floor_height', 'floor_surface')
    def calc_floor_volume(self):
        for r in self:
            r.floor_volume = r.floor_surface * r.floor_height

    # FINAL VOLUME
    @api.onchange('floor_volume', 'floor_deduct')
    def calc_floor_final_volume(self):
        for r in self:
            r.floor_final_volume = r.floor_volume - r.floor_deduct

    # MIN NOZZLES
    @api.onchange('floor_width', 'floor_length', 'floor_surface', 'floor_height')
    def calc_min_floor_nozzles(self):
        for r in self:
            if r.floor_width > 9.8 or r.floor_length > 9.8:
                nozz_width = 0
                nozz_length = 0
                if r.floor_width > 9.8:
                    nozz_width = int(r.floor_width / 9.81) + 1
                if r.floor_length > 9.8:
                    nozz_length = int(r.floor_length / 9.81) + 1
                r.floor_min_nozzles = nozz_width + nozz_length
            else:
                nozz_area = int(r.floor_surface / 96.05) + 1
                nozz_height = int(r.floor_height / 5.01) + 1
                r.floor_min_nozzles = nozz_area * nozz_height

    # Suggest NOZZLES
    @api.onchange('floor_min_nozzles')
    def calc_sugg_nozz_floor(self):
        for r in self:
            r.floor_suggest_nozzles = r.floor_min_nozzles

    def inverse_sugg_nozz_floor(self):
        for r in self:
            r.floor_suggest_nozzles = r.floor_suggest_nozzles

    # KGS / NOZZLES
    @api.onchange('correction', 'concentration', 'floor_volume', 'temperature')
    def calc_kgs_floor_nozz(self):
        for r in self:
            r.kgs_floor_nozzle = (r.correction * 1.01 * r.concentration * r.floor_volume) / (
                    (100 - r.concentration) * (0.0664 + (0.000274 * r.temperature)))

    floor_width = fields.Float(string="Width (m)")
    floor_length = fields.Float(string="Length (m)")
    floor_surface = fields.Float(string="Surface (m2)",
                                 compute='calc_floor_surface',
                                 inverse='inverse_floor_surface')
    floor_height = fields.Float(string="Height (m)")
    floor_volume = fields.Float(string="Volume (m3)",
                                compute='calc_floor_volume', default=0)
    floor_deduct = fields.Float(string="Deductions (m3)", default=0)
    floor_final_volume = fields.Float(string="Final Volume (m3)",
                                      related='floor_volume',
                                      compute='calc_floor_final_volume')
    floor_min_nozzles = fields.Integer(string="Min Nozzles",
                                       compute='calc_min_floor_nozzles')
    floor_suggest_nozzles = fields.Integer(string="Suggest Nozzles",
                                           compute='calc_sugg_nozz_floor',
                                           inverse='inverse_sugg_nozz_floor')
    kgs_floor_nozzle = fields.Float(string="Each Nozzle (Kg)", default=0,
                                    compute='calc_kgs_floor_nozz')
    floor_image_drawing = fields.Binary(string="Drawing")
    floor_details = fields.Text(string="Details")
