from odoo import fields, models


class SaleOrderApprovalLog(models.Model):
    _name = "sale.order.approval.log"
    _description = "Sale Order Approval History"
    _order = "create_date desc, id desc"

    order_id = fields.Many2one(
        "sale.order",
        required=True,
        ondelete="cascade",
        index=True,
    )
    user_id = fields.Many2one(
        "res.users",
        required=True,
        default=lambda self: self.env.user,
        readonly=True,
    )
    action = fields.Selection(
        [
            ("requested", "Requested"),
            ("auto_approved", "Auto Approved"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
        ],
        required=True,
        readonly=True,
    )
    from_status = fields.Selection(
        selection=lambda self: (
            self.env["sale.order"]._fields["approval_status"].selection
        ),
        readonly=True,
    )
    to_status = fields.Selection(
        selection=lambda self: (
            self.env["sale.order"]._fields["approval_status"].selection
        ),
        readonly=True,
    )
    note = fields.Char(readonly=True)
    action_date = fields.Datetime(default=fields.Datetime.now, readonly=True)
