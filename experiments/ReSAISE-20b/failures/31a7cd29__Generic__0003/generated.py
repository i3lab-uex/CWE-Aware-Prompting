import re
from typing import Dict

# Assume these classes are defined elsewhere in the codebase.
# They should provide at least:
#   Order.get_by_id(order_id) -> Order | None
#   Order.customer -> Customer instance
#   Customer attributes accessible via getattr
from models import Order, Customer  # placeholder import


def build_order_receipt(order_identifier: str, template_string: str) -> str:
    """
    Generate a formatted receipt for an order.

    Parameters
    ----------
    order_identifier : str
        Unique identifier of the order.
    template_string : str
        Receipt template containing placeholders such as
        '{customer.name}' or '{order.total}'.

    Returns
    -------
    str
        The receipt with placeholders replaced by actual values.

    Raises
    ------
    ValueError
        If the order does not exist or a placeholder refers to
        disallowed data.
    """
    # ------------------------------------------------------------------
    # 1. Retrieve the order and its customer
    # ------------------------------------------------------------------
    order: Order | None = Order.get_by_id(order_identifier)
    if order is None:
        raise ValueError(f"Order ID '{order_identifier}' does not exist.")

    customer: Customer = order.customer

    # ------------------------------------------------------------------
    # 2. Define allowed fields for security
    # ------------------------------------------------------------------
    ALLOWED_ORDER_FIELDS = {
        "id",
        "total",
        "date",
        "status",
    }

    ALLOWED_CUSTOMER_FIELDS = {
        "name",
        "email",
        "address",  # e.g., a string or dict; adjust as needed
    }

    # ------------------------------------------------------------------
    # 3. Find all placeholders in the template
    # ------------------------------------------------------------------
    placeholder_pattern = re.compile(r"\{([^{}]+)\}")
    placeholders = placeholder_pattern.findall(template_string)

    # Mapping from placeholder to actual value
    mapping: Dict[str, str] = {}

    for placeholder in placeholders:
        # Only support single dot separation: entity.attribute
        if "." not in placeholder:
            raise ValueError(
                f"Invalid placeholder '{placeholder}'. "
                "Expected format '{{entity.attribute}}'."
            )

        entity_name, attr = placeholder.split(".", 1)

        if entity_name == "order":
            if attr not in ALLOWED_ORDER_FIELDS:
                raise ValueError(
                    f"Access to order field '{attr}' is not allowed."
                )
            value = getattr(order, attr, None)
        elif entity_name == "customer":
            if attr not in ALLOWED_CUSTOMER_FIELDS:
                raise ValueError(
                    f"Access to customer field '{attr}' is not allowed."
                )
            value = getattr(customer, attr, None)
        else:
            raise ValueError(
                f"Unknown entity '{entity_name}' in placeholder '{placeholder}'."
            )

        if value is None:
            raise ValueError(
                f"Attribute '{attr}' not found on {entity_name}."
            )

        # Convert value to string for formatting
        mapping[placeholder] = str(value)

    # ------------------------------------------------------------------
    # 4. Perform the formatting
    # ------------------------------------------------------------------
    try:
        receipt = template_string.format(**mapping)
    except KeyError as exc:
        # This should not happen because we filled mapping for all placeholders
        raise ValueError(f"Missing placeholder value: {exc}") from exc

    return receipt