import re
from dataclasses import dataclass
from typing import Dict, Any

# ------------------------------------------------------------------
# Sample data models (in a real application these would be ORM classes)
# ------------------------------------------------------------------
@dataclass
class Customer:
    id: str
    name: str
    email: str          # Sensitive field
    address: str

@dataclass
class Order:
    id: str
    customer_id: str
    total: float
    items: list

# ------------------------------------------------------------------
# In‑memory store (replace with database lookups in production)
# ------------------------------------------------------------------
CUSTOMERS: Dict[str, Customer] = {
    "cust_1": Customer(id="cust_1", name="Alice Smith",
                       email="alice@example.com", address="123 Main St"),
    "cust_2": Customer(id="cust_2", name="Bob Jones",
                       email="bob@example.com", address="456 Oak Ave"),
}

ORDERS: Dict[str, Order] = {
    "order_1001": Order(id="order_1001", customer_id="cust_1",
                        total=199.99, items=["Widget A", "Widget B"]),
    "order_1002": Order(id="order_1002", customer_id="cust_2",
                        total=49.99, items=["Gadget X"]),
}

# ------------------------------------------------------------------
# Allowed placeholders mapping
# ------------------------------------------------------------------
ALLOWED_PLACEHOLDERS = {
    "customer.name": lambda cust: cust.name,
    "order.total": lambda order: f"{order.total:.2f}",
    # Add more allowed placeholders as needed
}

# ------------------------------------------------------------------
# Core function
# ------------------------------------------------------------------
def generate_buyer_receipt(order_id: str, template: str) -> str:
    """
    Generate a formatted receipt for the buyer based on the provided template.

    Parameters
    ----------
    order_id : str
        Unique identifier of the order.
    template : str
        Receipt template containing placeholders like '{customer.name}'.

    Returns
    -------
    str
        The formatted receipt string.

    Raises
    ------
    ValueError
        If the order ID is invalid or if a restricted field is requested.
    """
    # Validate order existence
    order = ORDERS.get(order_id)
    if not order:
        raise ValueError(f"Invalid order ID: {order_id}")

    # Retrieve the associated customer
    customer = CUSTOMERS.get(order.customer_id)
    if not customer:
        raise ValueError(f"Customer for order {order_id} not found")

    # Find all placeholders in the template
    placeholder_pattern = re.compile(r"\{([^\}]+)\}")
    placeholders = placeholder_pattern.findall(template)

    # Build a mapping of placeholder to its value
    substitution: Dict[str, str] = {}
    for ph in placeholders:
        if ph not in ALLOWED_PLACEHOLDERS:
            raise ValueError(f"Restricted or unknown placeholder: {ph}")

        # Resolve the value
        try:
            if ph.startswith("customer."):
                value = ALLOWED_PLACEHOLDERS[ph](customer)
            elif ph.startswith("order."):
                value = ALLOWED_PLACEHOLDERS[ph](order)
            else:
                # This branch should never be reached due to the check above
                raise ValueError(f"Unsupported placeholder: {ph}")
        except Exception as exc:
            # Wrap any unexpected errors
            raise ValueError(f"Error processing placeholder '{ph}': {exc}") from exc

        substitution[ph] = value

    # Safely perform the substitutions
    def replace_match(match: re.Match) -> str:
        key = match.group(1)
        return substitution.get(key, "")

    receipt = placeholder_pattern.sub(replace_match, template)
    return receipt

# ------------------------------------------------------------------
# Example usage (for local testing only)
# ------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = (
        "Dear {customer.name},\n"
        "Thank you for your purchase!\n"
        "Your order total is ${order.total}.\n"
        "Enjoy your day!"
    )
    print(generate_buyer_receipt("order_1001", tmpl))