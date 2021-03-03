from odoo import api, fields, models, exceptions, _


class SevoCylinder(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'force500.cylinder'
    _description = 'Sevostudio Cylinders'
    _check_company_auto = True
    _order = 'name desc'

    name = fields.Char(string="Name")
    description = fields.Text(string="Description")
    cyl_size = fields.Float(string="Size (L)")
    cyl_manufacturing = fields.Selection([
        ('welded', 'Welded'),
        ('seamless', 'Seamless')],
        string="Manufacturing")
    cyl_level = fields.Boolean(string="Liquid Level Indicator")
    dipt_diameter = fields.Float(string="Dip Tube Diameter (mm)")
    cyl_valve = fields.Float(string="Valve Outlet (mm)")
    allowable_min = fields.Float(string="Allowable Fill Min (Kg)")
    allowable_max = fields.Float(string="Allowable Fill Max (Kg)")
    cyl_valve_true = fields.Boolean(string="Valve Outlet Diameter")
    cyl_valve_diameter = fields.Selection([
        ('val1', '1"'),
        ('val2', '1 1/4"'),
        ('val3', '2 1/2"')],
        string="Valve Outlet Diameter")
    weight = fields.Float(string="Weight (Kg)")
    measure_a = fields.Integer(string="A (Diameter)(mm)")
    measure_b = fields.Integer(string="B (Height Nozzle)(mm)")
    measure_c = fields.Integer(string="C (Height total)(mm)")
    threading_type_true = fields.Boolean(string="Threading Type")
    threading_type = fields.Selection([
        ('F', "Female NTP"),
        ('M', "Male NTP")],
        string="Threading Type")
    image_measure = fields.Binary("Image")
