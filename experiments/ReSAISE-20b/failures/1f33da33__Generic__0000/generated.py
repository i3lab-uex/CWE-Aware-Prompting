import re
from typing import Dict

# Assume these classes exist in the application context.
# They are imported here for type hints; if they are defined elsewhere,
# this import will succeed. If not, the function will still work
# as long as the objects returned by `get_employee_by_id` expose the
# expected attributes.
try:
    from employee_module import Employee, Performance  # noqa: F401
except ImportError:
    # If the actual modules are named differently, adjust the import accordingly.
    pass


# ------------------------------------------------------------------------------
# Helper utilities
# ------------------------------------------------------------------------------

# Allowed fields that can appear in the template.
ALLOWED_EMPLOYEE_FIELDS = {"name", "position", "department"}
ALLOWED_PERFORMANCE_FIELDS = {"rating", "comments"}  # 'feedback' and 'bonus' are restricted

# Regular expression to capture the placeholder names.
PLACEHOLDER_RE = re.compile(r"{([^{}]+)}")


def _extract_placeholders(template: str) -> set[str]:
    """Return a set of placeholder names found in the template."""
    return {match.group(1) for match in PLACEHOLDER_RE.finditer(template)}


def _build_mapping(emp: "Employee", perf: "Performance") -> Dict[str, str]:
    """Create a flat mapping from placeholder names to their string values."""
    mapping: Dict[str, str] = {}

    # Employee fields
    for field in ALLOWED_EMPLOYEE_FIELDS:
        mapping[f"employee.{field}"] = str(getattr(emp, field))

    # Performance fields
    for field in ALLOWED_PERFORMANCE_FIELDS:
        mapping[f"performance.{field}"] = str(getattr(perf, field))

    return mapping


def _validate_placeholders(placeholders: set[str]) -> None:
    """
    Ensure that no restricted placeholders are used.
    Raises ValueError if a disallowed placeholder is found.
    """
    for ph in placeholders:
        # Split the namespace and field name
        if "." not in ph:
            raise ValueError(f"Invalid placeholder format: '{ph}'. Expected 'namespace.field'.")
        namespace, field = ph.split(".", 1)
        if namespace == "employee" and field not in ALLOWED_EMPLOYEE_FIELDS:
            raise ValueError(f"Access to restricted employee field '{field}'.")
        if namespace == "performance" and field not in ALLOWED_PERFORMANCE_FIELDS:
            raise ValueError(f"Access to restricted performance field '{field}'.")
        if namespace not in {"employee", "performance"}:
            raise ValueError(f"Unknown placeholder namespace '{namespace}'.")


# ------------------------------------------------------------------------------
# Core function
# ------------------------------------------------------------------------------

def create_performance_summary(emp_id: str, summary_template: str) -> str:
    """
    Generate a performance summary for the employee identified by `emp_id`
    using the provided `summary_template`.

    Parameters
    ----------
    emp_id : str
        Unique identifier of the employee.
    summary_template : str
        Template string containing placeholders such as
        '{employee.name}', '{performance.rating}', etc.

    Returns
    -------
    str
        The formatted performance summary.

    Raises
    ------
    ValueError
        If the employee ID is not found, or if the template references
        restricted fields (e.g., 'feedback', 'bonus') or an unknown namespace.
    """
    # --------------------------------------------------------------------------
    # Retrieve employee and performance data
    # --------------------------------------------------------------------------
    try:
        # The actual lookup logic depends on the surrounding application.
        # Here we assume a simple global registry for demonstration purposes.
        from employee_registry import get_employee_by_id, get_performance_by_emp_id  # noqa: F401
    except ImportError:
        raise RuntimeError(
            "Employee registry modules not found. "
            "Ensure that `get_employee_by_id` and `get_performance_by_emp_id` are available."
        )

    employee = get_employee_by_id(emp_id)
    if not employee:
        raise ValueError(f"Employee ID '{emp_id}' does not exist.")

    performance = get_performance_by_emp_id(emp_id)
    if not performance:
        raise ValueError(f"Performance data for employee ID '{emp_id}' is missing.")

    # --------------------------------------------------------------------------
    # Validate placeholders
    # --------------------------------------------------------------------------
    placeholders = _extract_placeholders(summary_template)
    _validate_placeholders(placeholders)

    # --------------------------------------------------------------------------
    # Build mapping and format
    # --------------------------------------------------------------------------
    mapping = _build_mapping(employee, performance)

    try:
        result = summary_template.format_map(mapping)
    except KeyError as exc:
        # This should not happen if validation passed, but guard anyway.
        raise ValueError(f"Missing value for placeholder: {exc}") from exc

    return result