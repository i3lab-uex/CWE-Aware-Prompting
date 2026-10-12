import re
from dataclasses import dataclass, asdict
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Mock data store and entity classes (would normally be replaced by real DB)
# --------------------------------------------------------------------------- #

@dataclass
class Customer:
    id: str
    name: str
    email: str  # sensitive
    phone: str

@dataclass
class Order:
    id: str
    customer_id: str
    total: float
    items: list

# In‑memory "database"
_CUSTOMERS: Dict[str, Customer] = {
    "cust1": Customer(id="cust1", name="Alice Smith", email="alice@example.com", phone="555-1234"),
    "cust2": Customer(id="cust2", name="Bob Jones", email="bob@example.com", phone="555-5678"),
}

_ORDERS: Dict[str, Order] = {
    "order1": Order(id="order1", customer_id="cust1", total=120.50, items=["Book", "Pen"]),
    "order2": Order(id="order2", customer_id="cust2", total=75.00, items=["Notebook"]),
}

def get_order_by_id(order_id: str) -> Order:
    return _ORDERS.get(order_id)

def get_customer_by_id(customer_id: str) -> Customer:
    return _CUSTOMERS.get(customer_id)

# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #

_ALLOWED_CUSTOMER_FIELDS = {"name", "phone"}          # fields allowed in receipt
_RESTRICTED_CUSTOMER_FIELDS = {"email"}               # explicitly disallowed
_PLACEHOLDER_PATTERN = re.compile(r"\{(?P<obj>[a-zA-Z_]+)\.(?P<field>[a-zA-Z_]+)\}")

def create_receipt_for_transaction(transaction_id: str, template_format: str) -> str:
    """
    Generate a receipt for the given transaction ID by substituting placeholders
    in *template_format* with data from the corresponding Order and Customer.

    Raises:
        ValueError: if transaction_id is unknown or a placeholder refers to
                    restricted customer data.
    """
    # ----------------------------------------------------------------------- #
    # 1. Retrieve order and customer
    # ----------------------------------------------------------------------- #
    order = get_order_by_id(transaction_id)
    if not order:
        raise ValueError(f"Transaction ID '{transaction_id}' does not exist.")

    customer = get_customer_by_id(order.customer_id)
    if not customer:
        raise ValueError(f"Customer ID '{order.customer_id}' for transaction "
                         f"'{transaction_id}' does not exist.")

    # ----------------------------------------------------------------------- #
    # 2. Prepare lookup dictionaries
    # ----------------------------------------------------------------------- #
    order_dict = asdict(order)
    customer_dict = {k: v for k, v in asdict(customer).items()
                     if k not in _RESTRICTED_CUSTOMER_FIELDS}

    # ----------------------------------------------------------------------- #
    # 3. Resolve placeholders
    # ----------------------------------------------------------------------- #
    def replace_placeholder(match: re.Match) -> str:
        obj_name = match.group("obj")
        field_name = match.group("field")

        if obj_name == "order":
            if field_name not in order_dict:
                raise ValueError(f"Order has no attribute '{field_name}'.")
            return str(order_dict[field_name])

        if obj_name == "customer":
            if field_name in _RESTRICTED_CUSTOMER_FIELDS:
                raise ValueError(f"Access to restricted customer field '{field_name}' denied.")
            if field_name not in _ALLOWED_CUSTOMER_FIELDS:
                raise ValueError(f"Customer has no allowed attribute '{field_name}'.")
            return str(customer_dict[field_name])

        raise ValueError(f"Unknown placeholder object '{obj_name}'.")

    # Perform the substitution
    receipt = _PLACEHOLDER_PATTERN.sub(replace_placeholder, template_format)

    return receipt

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    template = (
        "Receipt for Order #{order.id}\n"
        "Customer: {customer.name}\n"
        "Phone: {customer.phone}\n"
        "Total: ${order.total}\n"
        "Items: {order.items}"
    )
    print(create_receipt_for_transaction("order1", template))