import re

# Assume these classes are defined elsewhere in the system.
# They should provide at least the following attributes:
#
# class Employee:
#     def __init__(self, emp_id: str, name: str, position: str, department: str,
#                  performance: 'Performance'):
#         ...
#
#     @classmethod
#     def get(cls, emp_id: str) -> 'Employee':
#         ...
#
# class Performance:
#     def __init__(self, rating: str, feedback: str, bonus: float):
#         ...
#
# For the purposes of this implementation we only rely on the public
# attributes mentioned above.

RESTRICTED_FIELDS = {"feedback", "bonus"}

PLACEHOLDER_PATTERN = re.compile(r"\{([^{}]+)\}")


def _extract_placeholder_value(obj, key: str):
    """
    Safely extract the value of a dotted attribute path from an object.
    Example: key='employee.name' will return obj.employee.name
    """
    parts = key.split(".")
    current_obj = obj
    for part in parts:
        if not hasattr(current_obj, part):
            raise ValueError(f"Invalid placeholder '{key}': attribute '{part}' not found.")
        current_obj = getattr(current_obj, part)
    return str(current_obj)


def create_performance_summary(emp_id: str, summary_template: str) -> str:
    """
    Generate a performance summary for the employee identified by ``emp_id``.
    The ``summary_template`` may contain placeholders in the form
    `{employee.attribute}` or `{performance.attribute}`.  Any attempt to
    access a restricted field such as ``feedback`` or ``bonus`` will raise
    :class:`ValueError`.  An invalid employee ID also raises
    :class:`ValueError`.

    Parameters
    ----------
    emp_id : str
        Unique identifier for the employee.
    summary_template : str
        Template string containing placeholders.

    Returns
    -------
    str
        The formatted performance summary.

    Raises
    ------
    ValueError
        If the employee ID is not found or if a restricted field is accessed.
    """
    # Retrieve employee data; raise ValueError if not found
    try:
        employee = Employee.get(emp_id)
    except Exception as exc:   # Generic catch because the underlying API may vary
        raise ValueError(f"Employee with ID '{emp_id}' not found.") from exc

    # Build a dictionary of allowed values
    allowed_values = {
        "employee.name": employee.name,
        "employee.position": employee.position,
        "employee.department": employee.department,
    }

    # Add performance attributes except restricted ones
    perf = getattr(employee, "performance", None)
    if perf is not None:
        for attr in dir(perf):
            if attr.startswith("_"):
                continue
            if attr in RESTRICTED_FIELDS:
                continue
            try:
                value = getattr(perf, attr)
                allowed_values[f"performance.{attr}"] = str(value)
            except Exception:
                continue

    # Replace placeholders
    def replace_match(match: re.Match) -> str:
        key = match.group(1).strip()
        if any(key.endswith(f".{field}") for field in RESTRICTED_FIELDS):
            raise ValueError(
                f"Access to restricted field '{key}' is not allowed."
            )
        if key not in allowed_values:
            # Attempt to resolve dynamically (e.g., nested attributes)
            try:
                return _extract_placeholder_value(employee, key)
            except ValueError as e:
                raise ValueError(f"Invalid placeholder '{key}'.") from e
        return allowed_values[key]

    try:
        result = PLACEHOLDER_PATTERN.sub(replace_match, summary_template)
    except ValueError as e:
        raise

    return result