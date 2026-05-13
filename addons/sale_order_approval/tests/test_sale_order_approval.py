from odoo.exceptions import AccessError, UserError
from odoo.tests.common import TransactionCase, tagged


@tagged("sale_order_approval")
class TestSaleOrderApproval(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "Approval Customer"})
        cls.product = cls.env["product.product"].create(
            {
                "name": "Approval Product",
                "list_price": 1000.0,
                "standard_price": 100.0,
            }
        )
        cls.sales_user = cls._create_user(
            "salesperson",
            [
                "base.group_user",
                "sales_team.group_sale_salesman",
            ],
        )
        cls.manager_user = cls._create_user(
            "sales_manager",
            [
                "base.group_user",
                "sale_order_approval.group_sale_approval_manager",
            ],
        )
        cls.finance_user = cls._create_user(
            "finance_manager",
            [
                "base.group_user",
                "sale_order_approval.group_sale_approval_finance",
            ],
        )
        cls.gm_user = cls._create_user(
            "general_manager",
            [
                "base.group_user",
                "sale_order_approval.group_sale_approval_gm",
            ],
        )

    @classmethod
    def _create_user(cls, login, group_xmlids):
        groups = [cls.env.ref(xmlid).id for xmlid in group_xmlids]
        return (
            cls.env["res.users"]
            .with_context(no_reset_password=True)
            .create(
                {
                    "name": login.replace("_", " ").title(),
                    "login": login,
                    "email": f"{login}@example.com",
                    "group_ids": [(6, 0, groups)],
                }
            )
        )

    @classmethod
    def _create_order(cls, untaxed_amount):
        quantity = untaxed_amount / 1000.0
        return (
            cls.env["sale.order"]
            .with_user(cls.sales_user)
            .create(
                {
                    "partner_id": cls.partner.id,
                    "order_line": [
                        (
                            0,
                            0,
                            {
                                "name": cls.product.name,
                                "product_id": cls.product.id,
                                "product_uom_qty": quantity,
                                "price_unit": 1000.0,
                            },
                        )
                    ],
                }
            )
        )

    def test_auto_approve_small_order(self):
        order = self._create_order(4000.0)

        order.with_user(self.sales_user).action_request_approval()

        self.assertEqual(order.approval_status, "approved")
        self.assertEqual(len(order.approval_log_ids), 1)
        self.assertEqual(order.approval_log_ids.action, "auto_approved")

    def test_manager_approval_route(self):
        order = self._create_order(10000.0)

        order.with_user(self.sales_user).action_request_approval()
        self.assertEqual(order.approval_status, "waiting_manager")

        order.with_user(self.manager_user).action_approve_order()

        self.assertEqual(order.approval_status, "approved")
        self.assertEqual(
            order.approval_log_ids.sorted(lambda log: log.id, reverse=True).mapped(
                "action"
            ),
            ["approved", "requested"],
        )

    def test_finance_then_general_manager_route(self):
        order = self._create_order(25000.0)

        order.with_user(self.sales_user).action_request_approval()
        self.assertEqual(order.approval_status, "waiting_finance")

        order.with_user(self.finance_user).action_approve_order()
        self.assertEqual(order.approval_status, "waiting_gm")

        order.with_user(self.gm_user).action_approve_order()
        self.assertEqual(order.approval_status, "approved")
        self.assertEqual(
            order.approval_log_ids.sorted(lambda log: log.id, reverse=True).mapped(
                "action"
            ),
            ["approved", "approved", "requested"],
        )

    def test_permission_restrictions(self):
        manager_order = self._create_order(10000.0)
        finance_order = self._create_order(25000.0)

        manager_order.with_user(self.sales_user).action_request_approval()
        finance_order.with_user(self.sales_user).action_request_approval()

        with self.assertRaises(AccessError):
            manager_order.with_user(self.sales_user).action_approve_order()

        with self.assertRaises(AccessError):
            finance_order.with_user(self.manager_user).action_approve_order()

    def test_rejection_flow_blocks_confirmation(self):
        order = self._create_order(12000.0)

        order.with_user(self.sales_user).action_request_approval()
        order.with_user(self.manager_user).action_reject_order("Budget rejected")

        self.assertEqual(order.approval_status, "rejected")
        self.assertIn("Budget rejected", order.approval_log_ids.mapped("note"))

        with self.assertRaises(UserError):
            order.with_user(self.sales_user).action_confirm()

    def test_confirmation_requires_approval(self):
        order = self._create_order(15000.0)

        with self.assertRaises(UserError):
            order.with_user(self.sales_user).action_confirm()

        order.with_user(self.sales_user).action_request_approval()
        with self.assertRaises(UserError):
            order.with_user(self.sales_user).action_confirm()

        order.with_user(self.manager_user).action_approve_order()
        order.with_user(self.sales_user).action_confirm()

        self.assertEqual(order.state, "sale")

    def test_chatter_messages_created_for_actions(self):
        order = self._create_order(22000.0)
        initial_message_count = len(order.message_ids)

        order.with_user(self.sales_user).action_request_approval()
        order.with_user(self.finance_user).action_approve_order()

        self.assertGreater(len(order.message_ids), initial_message_count)
        message_bodies = order.message_ids.mapped("body")
        self.assertTrue(any("Approval requested" in body for body in message_bodies))
        self.assertTrue(any("approved" in body.lower() for body in message_bodies))
