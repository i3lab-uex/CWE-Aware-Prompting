import re
from typing import Any, Dict

# ------------------------------------------------------------------
# Mock data models – in a real system these would be imported from
# the company's domain modules. They are defined here only so that
# this module can run as a standalone example.
# ------------------------------------------------------------------
class Employee:
    def __init__(self, id: str, name: str, position: str,
                 department: str):
        self.id = id
        self.name = name
        self.position = position
        self.department = department


class Performance:
    def __init__(self, employee_id: str,
                 rating: float, feedback: str, bonus: float):
        self.employee_id = employee_id
        self.rating = rating
        self.feedback = feedback
        self.bonus = bonus


# ------------------------------------------------------------------
# A tiny in‑memory "database" for the example.
# ------------------------------------------------------------------
EMPLOYEES = {
    "E001": Employee("E001", "Alice Smith", "Senior Engineer",
                     "R&D"),
    "E002": Employee("E002", "Bob Johnson", "Product Manager",
                     "Product"),
}

PERFORMANCES = {
    "E001": Performance("E001", 4.5, "Excellent problem solving",
                         5000.0),
    "E002": Performance("E002", 3.8, "Good collaboration",
                         3000.0),
}


# ------------------------------------------------------------------
# Helper utilities
# ------------------------------------------------------------------
def _get_nested_attr(obj: Any, attr_path: str) -> Any:
    """Retrieve nested attributes from an object using a dotted path."""
    for part in attr_path.split("."):
        if not hasattr(obj, part):
            raise AttributeError(f"Attribute '{part}' not found")
        obj = getattr(obj, part)
    return obj


def _parse_placeholders(template: str) -> set[str]:
    """Return a set of placeholder names found in the template."""
    return set(re.findall(r"{([^}]+)}", template))


def _is_sensitive(key: str) -> bool:
    """Return True if the key references a sensitive attribute."""
    return any(s in key for s in ("feedback", "bonus"))


# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------
def generate_employee_summary(employee_id: str, template: str) -> str:
    """
    Generate a summary string for the given employee using the provided
    template. Placeholders must be of the form {employee.<attr>} or
    {performance.<attr>}. Access to sensitive attributes (feedback,
    bonus) is prohibited.

    Parameters
    ----------
    employee_id : str
        The unique identifier of the employee.
    template : str
        Summary template containing placeholders.

    Returns
    -------
    str
        The rendered summary string.

    Raises
    ------
    ValueError
        If the employee ID is unknown, a placeholder references an
        undefined attribute, or if sensitive information is requested.
    """
    # 1. Load data
    employee = EMPLOYEES.get(employee_id)
    if not employee:
        raise ValueError(f"Unknown employee ID: {employee_id}")

    performance = PERFORMANCES.get(employee_id)
    if not performance:
        raise ValueError(f"No performance data for employee ID: {employee_id}")

    # 2. Parse placeholders
    placeholders = _parse_placeholders(template)

    # 3. Validate and build context dict
    context: Dict[str, Any] = {}
    for key in placeholders:
        # Prohibit sensitive data
        if _is_sensitive(key):
            raise ValueError(f"Access to sensitive field '{key}' is not allowed")

        # Determine which object owns the attribute
        if key.startswith("employee."):
            source_obj = employee
            attr_path = key[len("employee.") :]
        elif key.startswith("performance."):
            source_obj = performance
            attr_path = key[len("performance.") :]
        else:
            raise ValueError(f"Unknown placeholder namespace in '{key}'")

        # Retrieve the attribute value
        try:
            value = _get_nested_attr(source_obj, attr_path)
        except AttributeError as exc:
            raise ValueError(f"Invalid placeholder '{key}': {exc}") from None

        context[key] = value

    # 4. Render template
    try:
        result = template.format(**context)
    except KeyError as exc:
        # This should not happen because we pre‑validated placeholders
        raise ValueError(f"Missing value for placeholder {exc}") from None

    return result


# ------------------------------------------------------------------
# Example usage (would normally be part of unit tests)
# ------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = (
        "Employee: {employee.name}\n"
        "Position: {employee.position}\n"
        "Department: {employee.department}\n"
        "Performance Rating: {performance.rating}"
    )
    print(generate_employee_summary("E001", tmpl))