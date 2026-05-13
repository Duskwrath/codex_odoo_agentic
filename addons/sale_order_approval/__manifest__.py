{
    "name": "Sale Order Approval",
    "summary": "Multi-level approval workflow for sale orders",
    "version": "19.0.1.0.0",
    "category": "Sales/Sales",
    "author": "OpenAI",
    "license": "LGPL-3",
    "depends": ["sale_management", "mail"],
    "data": [
        "security/sale_order_approval_groups.xml",
        "security/ir.model.access.csv",
        "views/sale_order_views.xml",
    ],
    "demo": [
        "demo/sale_order_approval_demo.xml",
    ],
    "installable": True,
    "application": False,
}
