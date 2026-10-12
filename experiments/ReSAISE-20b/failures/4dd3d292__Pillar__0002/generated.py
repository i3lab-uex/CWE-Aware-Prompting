import re
from typing import Any

# Assuming these classes are defined elsewhere in the application.
class Customer:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

class Order:
    def __init__(self, order_id: str, customer: Customer, total: float):
        self.order_id = order_id
        self.customer = customer
        self.total = total

# Mock database of orders for demonstration purposes.
ORDERS_DB = {
    "A001": Order("A001", Customer("Alice Smith", "alice@example.com"), 123.45),
    "B002": Order("B002", Customer("Bob Jones", "bob@example.com"), 67.89),
}

def _resolve_placeholder(order: Order, placeholder: str) -> Any:
    """
    Resolve a single placeholder against the order object.
    Prevent access to protected attributes (starting with an underscore).
    """
    # Split the placeholder into attribute chain, e.g., 'customer.name'
    parts = placeholder.split('.')
    current_obj: Any = order
    for part in parts:
        if part.startswith('_'):
            raise ValueError(f"Access to protected attribute '{part}' is not allowed.")
        if not hasattr(current_obj, part):
            raise ValueError(f"Attribute '{part}' not found in object of type {type(current_obj).__name__}.")
        current_obj = getattr(current_obj, part)
    return current_obj

def create_purchase_receipt(order_id: str, receipt_template: str) -> str:
    """
    Generate a formatted receipt for the given order ID using the provided template.
    
    Parameters
    ----------
    order_id : str
        The identifier of the order to retrieve.
    receipt_template : str
        A template string containing placeholders like '{customer.name}' or '{order.total}'.
    
    Returns
    -------
    str
        The fully rendered receipt string.
    
    Raises
    ------
    ValueError
        If the order ID is invalid or if a placeholder attempts to access protected data.
    """
    # Retrieve the order; raise an error if not found.
    order = ORDERS_DB.get(order_id)
    if order is None:
        raise ValueError(f"Order ID '{order_id}' does not exist.")
    
    # Find all placeholders in the template.
    placeholder_pattern = re.compile(r'\{([^{}]+)\}')
    
    def replacement(match: re.Match) -> str:
        placeholder = match.group(1).strip()
        # Allow top-level 'order' as a reference to the order object itself.
        if placeholder == "order":
            return str(order)
        try:
            value = _resolve_placeholder(order, placeholder)
            return str(value)
        except ValueError as exc:
            # Re-raise with context
            raise ValueError(f"Error resolving placeholder '{{{placeholder}}}': {exc}") from None
    
    # Perform the replacement safely.
    receipt = placeholder_pattern.sub(replacement, receipt_template)
    
    return receipt

# Example usage:
if __name__ == "__main__":
    template = (
        "Receipt for Order {order_id}\n"
        "Customer: {customer.name} ({customer.email})\n"
        "Total: ${order.total:.2f}\n"
    )
    try:
        receipt = create_purchase_receipt("A001", template)
        print(receipt)
    except ValueError as e:
        print(f"Failed to create receipt: {e}")