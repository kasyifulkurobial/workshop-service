from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class WorkshopService(models.Model):
    _name = 'workshop.service'
    _description = 'Workshop Service Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'
    _rec_name = 'name'

    name = fields.Char(
        string='Order Reference',
        required=True,
        copy=False,
        default='New',
        tracking=True,
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Customer',
        required=True,
        tracking=True,
    )
    vehicle_name = fields.Char(string='Vehicle / Equipment', required=True)
    license_plate = fields.Char(string='License Plate / Serial No.')
    technician_id = fields.Many2one(
        'res.users',
        string='Technician',
        tracking=True,
    )
    date_start = fields.Date(string='Service Date', default=fields.Date.today, required=True)
    date_end = fields.Date(string='Estimated End Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True, copy=False)

    line_ids = fields.One2many('workshop.service.line', 'service_id', string='Service Lines')

    total_amount = fields.Float(
        string='Subtotal',
        compute='_compute_total_amount',
        store=True,
    )
    amount_tax = fields.Float(
        string='Tax (11%)',
        compute='_compute_amount_tax',
        store=True,
    )
    amount_total = fields.Float(
        string='Grand Total',
        compute='_compute_amount_total',
        store=True,
    )
    duration_days = fields.Integer(
        string='Duration (Days)',
        compute='_compute_duration_days',
        store=True,
    )

    sale_order_id = fields.Many2one(
        'sale.order', string='Related Sale Order', readonly=True, copy=False,
    )
    picking_id = fields.Many2one(
        'stock.picking', string='Related Picking', readonly=True, copy=False,
    )
    notes = fields.Text(string='Internal Notes')

    @api.depends('line_ids.subtotal')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = sum(rec.line_ids.mapped('subtotal'))

    @api.depends('total_amount')
    def _compute_amount_tax(self):
        for rec in self:
            rec.amount_tax = rec.total_amount * 0.11

    @api.depends('total_amount', 'amount_tax')
    def _compute_amount_total(self):
        for rec in self:
            rec.amount_total = rec.total_amount + rec.amount_tax

    @api.depends('date_start', 'date_end')
    def _compute_duration_days(self):
        for rec in self:
            if rec.date_start and rec.date_end:
                rec.duration_days = (rec.date_end - rec.date_start).days
            else:
                rec.duration_days = 0

    def action_confirm(self):
        for rec in self:
            if not rec.line_ids:
                raise UserError('Cannot confirm: please add at least one service line.')
            rec.state = 'confirmed'

    def action_start(self):
        for rec in self:
            if rec.state != 'confirmed':
                raise UserError('Only confirmed orders can be started.')
            rec.state = 'in_progress'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        for rec in self:
            if rec.state == 'done':
                raise UserError('Cannot cancel a completed service order.')
            rec.state = 'cancelled'

    def action_reset_draft(self):
        for rec in self:
            if rec.state != 'cancelled':
                raise UserError('Only cancelled orders can be reset to draft.')
            rec.state = 'draft'

    def action_create_sale_order(self):
        self.ensure_one()
        
        if self.sale_order_id:
            raise UserError('Sale Order already exists for this service.')
            
        order_lines = []
        for line in self.line_ids:
            if not line.product_id:
                raise UserError('All service lines must have a product selected to create a Sale Order.')
                
            order_lines.append((0, 0, {
                'product_id': line.product_id.id,
                'name': line.name,
                'product_uom_qty': line.qty,
                'product_uom': line.uom_id.id,
                'price_unit': line.price_unit,
            }))

        sale_order_vals = {
            'partner_id': self.partner_id.id,
            'origin': self.name,
            'order_line': order_lines,
        }
        new_so = self.env['sale.order'].create(sale_order_vals)
        
        self.sale_order_id = new_so.id
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sale Order',
            'res_model': 'sale.order',
            'res_id': new_so.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_create_picking(self):
        self.ensure_one()
        
        if self.picking_id:
            raise UserError('Stock Picking already exists for this service.')
            
        part_lines = self.line_ids.filtered(lambda l: l.line_type == 'part' and l.product_id)
        if not part_lines:
            raise UserError('There are no Spare Parts to process for stock picking.')
            
        picking_type = self.env['stock.picking.type'].search([
            ('code', '=', 'outgoing'),
            ('company_id', '=', self.env.company.id)
        ], limit=1)
        
        if not picking_type:
            raise UserError('Cannot find an Outgoing operation type for stock picking.')
            
        location_id = picking_type.default_location_src_id.id
        if not location_id:
            internal_loc = self.env['stock.location'].search([
                ('usage', '=', 'internal'), 
                ('company_id', '=', self.env.company.id)
            ], limit=1)
            location_id = internal_loc.id

        location_dest_id = self.partner_id.property_stock_customer.id
        if not location_dest_id:
            customer_loc = self.env['stock.location'].search([
                ('usage', '=', 'customer')
            ], limit=1)
            location_dest_id = customer_loc.id
            
        if not location_id or not location_dest_id:
            raise UserError('Konfigurasi lokasi gudang atau customer tidak ditemukan di sistem.')
        
        picking_vals = {
            'partner_id': self.partner_id.id,
            'picking_type_id': picking_type.id,
            'location_id': location_id,
            'location_dest_id': location_dest_id,
            'origin': self.name,
        }
        new_picking = self.env['stock.picking'].create(picking_vals)
        
        for line in part_lines:
            self.env['stock.move'].create({
                'name': line.name,
                'product_id': line.product_id.id,
                'product_uom_qty': line.qty,
                'product_uom': line.uom_id.id,
                'picking_id': new_picking.id,
                'location_id': location_id,
                'location_dest_id': location_dest_id,
            })
            
        self.picking_id = new_picking.id
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Stock Picking',
            'res_model': 'stock.picking',
            'res_id': new_picking.id,
            'view_mode': 'form',
            'target': 'current',
        }