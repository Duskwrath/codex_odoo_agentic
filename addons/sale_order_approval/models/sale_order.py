from odoo import _, fields, models
from odoo.exceptions import AccessError, UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    approval_status = fields.Selection(
        [
            ("draft", "Draft"),
            ("waiting_manager", "Waiting Sales Manager"),
            ("waiting_finance", "Waiting Finance Manager"),
            ("waiting_gm", "Waiting General Manager"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
        ],
        string="Approval Status",
        default="draft",
        copy=False,
        tracking=True,
    )
    approval_log_ids = fields.One2many(
        "sale.order.approval.log",
        "order_id",
        string="Approval History",
        readonly=True,
        copy=False,
    )

    def write(self, vals):
        tracked_fields = {
            "currency_id",
            "fiscal_position_id",
            "order_line",
            "partner_id",
            "payment_term_id",
            "pricelist_id",
        }
        should_reset = bool(tracked_fields.intersection(vals))
        records_to_reset = self.env["sale.order"]
        if should_reset:
            records_to_reset = self.filtered(
                lambda order: order.state in {"draft", "sent"}
                and order.approval_status != "draft"
            )
        result = super().write(vals)
        if should_reset:
            records_to_reset._reset_approval_if_needed()
        return result

    def action_request_approval(self):
        for order in self:
            order._ensure_approvable_state()
            next_status = order._get_initial_approval_status()
            if next_status == "approved":
                order._update_approval_status(
                    new_status="approved",
                    action="auto_approved",
                    note=_("Order auto-approved because untaxed amount is below 5,000."),
                )
                continue
            order._update_approval_status(
                new_status=next_status,
                action="requested",
                note=order._get_request_message(next_status),
            )
        return True

    def action_approve_order(self):
        for order in self:
            order._ensure_approvable_state()
            order._check_approval_access()
            next_status, note = order._get_next_status_after_approval()
            order._update_approval_status(
                new_status=next_status,
                action="approved",
                note=note,
            )
        return True

    def action_reject_order(self, reason=None):
        for order in self:
            order._ensure_approvable_state()
            order._check_approval_access()
            order._update_approval_status(
                new_status="rejected",
                action="rejected",
                note=reason or _("Order rejected during approval."),
            )
        return True

    def action_confirm(self):
        for order in self:
            if order.state not in {"draft", "sent"}:
                continue
            if order.amount_untaxed < 5000 and order.approval_status != "approved":
                order.action_request_approval()
            elif order.approval_status != "approved":
                raise UserError(order._get_confirmation_block_message())
        return super().action_confirm()

    def _reset_approval_if_needed(self):
        for order in self:
            if order.state not in {"draft", "sent"}:
                continue
            if order.approval_status == "draft":
                continue
            order.approval_status = "draft"
            order.message_post(
                body=_("Approval status reset to draft because the quotation was updated.")
            )

    def _ensure_approvable_state(self):
        self.ensure_one()
        if self.state not in {"draft", "sent"}:
            raise UserError(_("Approval actions are only allowed on quotations."))

    def _get_initial_approval_status(self):
        self.ensure_one()
        if self.amount_untaxed < 5000:
            return "approved"
        if self.amount_untaxed <= 20000:
            return "waiting_manager"
        return "waiting_finance"

    def _get_request_message(self, next_status):
        self.ensure_one()
        messages = {
            "waiting_manager": _("Approval requested from Sales Manager."),
            "waiting_finance": _("Approval requested from Finance Manager."),
        }
        return messages[next_status]

    def _get_next_status_after_approval(self):
        self.ensure_one()
        if self.approval_status == "waiting_manager":
            return "approved", _("Order approved by Sales Manager.")
        if self.approval_status == "waiting_finance":
            return "waiting_gm", _("Order approved by Finance Manager and sent to General Manager.")
        if self.approval_status == "waiting_gm":
            return "approved", _("Order approved by General Manager.")
        raise UserError(_("There is no approval action pending on this quotation."))

    def _get_confirmation_block_message(self):
        self.ensure_one()
        messages = {
            "draft": _("Request approval before confirming this quotation."),
            "waiting_manager": _("This quotation is waiting for Sales Manager approval."),
            "waiting_finance": _("This quotation is waiting for Finance Manager approval."),
            "waiting_gm": _("This quotation is waiting for General Manager approval."),
            "rejected": _("This quotation was rejected and cannot be confirmed."),
        }
        return messages.get(
            self.approval_status,
            _("This quotation cannot be confirmed until approval is completed."),
        )

    def _check_approval_access(self):
        self.ensure_one()
        group_by_status = {
            "waiting_manager": "sale_order_approval.group_sale_approval_manager",
            "waiting_finance": "sale_order_approval.group_sale_approval_finance",
            "waiting_gm": "sale_order_approval.group_sale_approval_gm",
        }
        required_group = group_by_status.get(self.approval_status)
        if not required_group:
            raise UserError(_("There is no approval action pending on this quotation."))
        if not self.env.user.has_group(required_group):
            raise AccessError(_("You do not have permission to approve or reject this quotation."))

    def _update_approval_status(self, new_status, action, note):
        """Apply an approval transition, log it, and notify followers."""
        self.ensure_one()
        previous_status = self.approval_status
        self.approval_status = new_status
        self.env["sale.order.approval.log"].create(
            {
                "order_id": self.id,
                "user_id": self.env.user.id,
                "action": action,
                "from_status": previous_status,
                "to_status": new_status,
                "note": note,
            }
        )
        self.message_post(body=note)
