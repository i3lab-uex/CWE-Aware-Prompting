import re
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Dummy data structures to simulate the platform environment
# In a real system these would be imported from the actual application.
# --------------------------------------------------------------------------- #

class Customer:
    def __init__(self, name: str, email: str, phone: str, address: str):
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address

    # Example of a restricted attribute that should not be exposed in receipts
    @property
    def _ssn(self):
        return "123-45-6789"


class Order:
    def __init__(self, order_id: str, customer: Customer, total: float,
                 items: Dict[str, int], date: str):
        self.order_id = order_id
        self.customer = customer
        self.total = total
        self.items = items  # dict of item_name: quantity
        self.date = date

    def __repr__(self):
        return f"<Order {self.order_id}>"


# Simulated in‑memory "database" of orders
ORDER_DB: Dict[str, Order] = {}


def register_order(order: Order):
    """Register an order in the simulated database."""
    ORDER_DB[order.order_id] = order


# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #

PLACEHOLDER_PATTERN = re.compile(r"\{([^{}]+)\}")


def _safe_getattr(obj: Any, attr_chain: str) -> Any:
    """
    Safely retrieve a nested attribute specified by dot notation.
    Raises ValueError if any part of the chain is invalid or protected.
    """
    parts = attr_chain.split(".")
    current_obj = obj
    for part in parts:
        # Reject private or protected attributes (starting with underscore)
        if part.startswith("_"):
            raise ValueError(f"Access to protected attribute '{part}' is not allowed.")

        if hasattr(current_obj, part):
            current_obj = getattr(current_obj, part)
        else:
            raise ValueError(f"Attribute '{part}' does not exist on {current_obj!r}.")

        # If the attribute is a property, ensure it is not protected
        if isinstance(current_obj, property):
            raise ValueError(f"Access to property '{part}' is not allowed.")

    return current_obj


def create_receipt_for_transaction(transaction_id: str, template_format: str) -> str:
    """
    Generate a receipt string for the given transaction ID using the provided template.
    
    Args:
        transaction_id (str): Unique identifier of the order.
        template_format (str): Receipt template containing placeholders.

    Returns:
        str: Formatted receipt with all placeholders replaced by actual data.

    Raises:
        ValueError: If the transaction ID is unknown, or if a placeholder
                    references restricted/protected data.
    """
    # Retrieve the order; raise error if not found
    order = ORDER_DB.get(transaction_id)
    if order is None:
        raise ValueError(f"Order with ID '{transaction_id}' does not exist.")

    # Prepare a context that allows safe resolution of placeholders
    def replacer(match: re.Match) -> str:
        placeholder = match.group(1).strip()
        try:
            # Resolve the attribute chain starting from the order object
            value = _safe_getattr(order, placeholder)
        except ValueError as exc:
            raise ValueError(f"Invalid placeholder '{{{placeholder}}}': {exc}") from None

        # Convert the resolved value to string for insertion
        return str(value)

    # Perform substitution; any error will propagate as ValueError
    try:
        receipt = PLACEHOLDER_PATTERN.sub(replacer, template_format)
    except ValueError as exc:
        raise

    return receipt


# --------------------------------------------------------------------------- #
# Example usage (for demonstration; not part of the required implementation)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Create sample data
    cust = Customer(name="Alice Smith", email="alice@example.com",
                    phone="+1234567890", address="42 Wonderland Ave")
    order = Order(order_id="ORD-001",
                  customer=cust,
                  total=199.99,
                  items={"Widget": 2, "Gadget": 1},
                  date="2024-07-23")

    register_order(order)

    template = (
        "Receipt for Order #{order_id}\n"
        "Date: {date}\n\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Address: {customer.address}\n\n"
        "Items:\n{items}\n\n"
        "Total: ${total:.2f}"
    )

    # Since {items} is a dict, we format it specially
    # For the purpose of this demo, replace {items} manually
    formatted_items = "\n".join(f"  - {name}: {qty}" for name, qty in order.items.items())
    template = template.replace("{items}", formatted_items)

    receipt_text = create_receipt_for_transaction("ORD-001", template)
    print(receipt_text)