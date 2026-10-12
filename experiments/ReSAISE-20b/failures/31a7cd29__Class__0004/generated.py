import re
from dataclasses import dataclass, field
from typing import Dict, Any

# ----------------------------------------------------------------------
# Mock data structures (would normally come from the platform's models)
# ----------------------------------------------------------------------


@dataclass
class Customer:
    id: str
    name: str
    email: str
    address: str
    phone: str
    # Sensitive / restricted fields that must not be exposed via the receipt
    ssn: str = field(repr=False)
    credit_card_last4: str = field(repr=False)


@dataclass
class Order:
    id: str
    customer_id: str
    total: float
    items: Dict[str, int]  # item name -> quantity


# ----------------------------------------------------------------------
# In‑memory data store (for illustration purposes)
# ----------------------------------------------------------------------


CUSTOMERS: Dict[str, Customer] = {
    "cust1": Customer(
        id="cust1",
        name="Alice Smith",
        email="alice@example.com",
        address="123 Maple St, Springfield",
        phone="+1-555-0123",
        ssn="111-22-3333",
        credit_card_last4="4242",
    ),
}

ORDERS: Dict[str, Order] = {
    "order123": Order(
        id="order123",
        customer_id="cust1",
        total=199.99,
        items={"Widget A": 2, "Gadget B": 1},
    ),
}


# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------


def _get_order(order_id: str) -> Order:
    """Retrieve an order by ID or raise ValueError if not found."""
    try:
        return ORDERS[order_id]
    except KeyError:
        raise ValueError(f"Order ID '{order_id}' does not exist.")


def _get_customer(customer_id: str) -> Customer:
    """Retrieve a customer by ID or raise ValueError if not found."""
    try:
        return CUSTOMERS[customer_id]
    except KeyError:
        raise ValueError(f"Customer ID '{customer_id}' does not exist.")


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------


def build_order_receipt(order_identifier: str, template_string: str) -> str:
    """
    Generate a formatted receipt for the given order.

    Parameters
    ----------
    order_identifier : str
        The unique identifier of the order.
    template_string : str
        A string containing placeholders such as '{customer.name}' or
        '{order.total}'. Placeholders referencing restricted data will
        raise a ValueError.

    Returns
    -------
    str
        The receipt with placeholders replaced by actual data.

    Raises
    ------
    ValueError
        If the order ID is invalid or if a restricted field is requested.
    """
    # Fetch data
    order = _get_order(order_identifier)
    customer = _get_customer(order.customer_id)

    # Define the set of allowed attributes for each object
    ALLOWED_ORDER_ATTRS = {"id", "total", "items"}
    ALLOWED_CUSTOMER_ATTRS = {
        "name",
        "email",
        "address",
        "phone",
    }  # Exclude ssn, credit_card_last4

    # Regular expression to find placeholders like {object.attribute}
    placeholder_pattern = re.compile(r"\{([a-zA-Z_]+)\.([a-zA-Z_]+)\}")

    def replacement(match: re.Match) -> str:
        obj_name, attr = match.group(1), match.group(2)

        # Resolve the object
        if obj_name == "order":
            obj = order
            allowed_attrs = ALLOWED_ORDER_ATTRS
        elif obj_name == "customer":
            obj = customer
            allowed_attrs = ALLOWED_CUSTOMER_ATTRS
        else:
            raise ValueError(f"Unknown placeholder object '{obj_name}'.")

        # Check for restricted attributes
        if attr not in allowed_attrs:
            raise ValueError(
                f"Access to restricted attribute '{obj_name}.{attr}' is denied."
            )

        # Retrieve the value
        try:
            value = getattr(obj, attr)
        except AttributeError:
            raise ValueError(
                f"Attribute '{attr}' not found on object '{obj_name}'."
            )

        # Convert non-string values to string
        if isinstance(value, dict):
            # For items dictionary, format as "item: qty"
            return ", ".join(f"{k}: {v}" for k, v in value.items())
        else:
            return str(value)

    # Perform the substitution
    try:
        receipt = placeholder_pattern.sub(replacement, template_string)
    except re.error as e:
        raise ValueError(f"Invalid template string: {e}")

    return receipt


# ----------------------------------------------------------------------
# Example usage (would normally be in a separate test module)
# ----------------------------------------------------------------------


if __name__ == "__main__":
    tmpl = (
        "Receipt for Order {order.id}\n"
        "Customer: {customer.name}\n"
        "Email: {customer.email}\n"
        "Address: {customer.address}\n"
        "Phone: {customer.phone}\n"
        "Items: {order.items}\n"
        "Total: ${order.total:.2f}"
    )
    print(build_order_receipt("order123", tmpl))