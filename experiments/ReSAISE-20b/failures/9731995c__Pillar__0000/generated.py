import re
from dataclasses import dataclass, fields
from typing import Dict

# ------------------------------------------------------------------
# Dummy data structures – in a real system these would be replaced
# by database models or external services.
# ------------------------------------------------------------------
@dataclass(frozen=True)
class Employee:
    id: str
    name: str
    position: str
    department: str


@dataclass(frozen=True)
class Performance:
    employee_id: str
    rating: float
    feedback: str   # Sensitive – must not be exposed via the API
    bonus: float    # Sensitive – must not be exposed via the API


# ------------------------------------------------------------------
# In‑memory data store (for demonstration purposes only)
# ------------------------------------------------------------------
_EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(id="E001", name="Alice Smith", position="Software Engineer",
                     department="Engineering"),
    "E002": Employee(id="E002", name="Bob Johnson", position="Product Manager",
                     department="Product"),
}

_PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance(employee_id="E001", rating=4.5,
                        feedback="Excellent problem‑solving skills.",
                        bonus=5000),
    "E002": Performance(employee_id="E002", rating=4.0,
                        feedback="Strong leadership.",
                        bonus=4000),
}


def _get_employee(employee_id: str) -> Employee:
    """Retrieve an employee by ID."""
    try:
        return _EMPLOYEES[employee_id]
    except KeyError as exc:
        raise ValueError(f"Employee with ID {employee_id!r} not found") from exc


def _get_performance(employee_id: str) -> Performance:
    """Retrieve a performance record by employee ID."""
    try:
        return _PERFORMANCES[employee_id]
    except KeyError as exc:
        raise ValueError(f"Performance data for employee ID {employee_id!r} not found") from exc


# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------
def generate_employee_summary(employee_id: str, template: str) -> str:
    """
    Generate a summary string for an employee based on the supplied template.

    Parameters
    ----------
    employee_id : str
        The unique identifier of the employee.
    template : str
        A string containing placeholders such as '{employee.name}',
        '{performance.rating}', etc.

    Returns
    -------
    str
        The rendered summary string with placeholders substituted.

    Raises
    ------
    ValueError
        If the template references sensitive data (feedback or bonus) or if
        any required attribute is missing.
    """
    # 1. Validate the template for disallowed placeholders
    # Regex captures words separated by dots inside curly braces.
    placeholder_pattern = re.compile(r"{([^{}]+)}")
    placeholders = placeholder_pattern.findall(template)

    for ph in placeholders:
        # Prevent access to sensitive fields
        if re.search(r"\b(feedback|bonus)\b", ph):
            raise ValueError("Access to sensitive information is prohibited")

    # 2. Load the employee and performance objects
    employee = _get_employee(employee_id)
    performance = _get_performance(employee_id)

    # 3. Prepare a mapping of allowed attributes
    # We expose only safe fields from both objects.
    def _safe_attr(obj, attr_path: str):
        """Retrieve nested attribute safely; raise if not allowed."""
        parts = attr_path.split(".")
        if len(parts) != 2:
            raise ValueError(f"Invalid placeholder '{attr_path}'")

        obj_name, field_name = parts
        if obj_name == "employee":
            target_obj = employee
            allowed_fields = {f.name for f in fields(Employee)}
        elif obj_name == "performance":
            target_obj = performance
            allowed_fields = {f.name for f in fields(Performance)}
        else:
            raise ValueError(f"Unknown object '{obj_name}' in placeholder")

        if field_name not in allowed_fields:
            raise ValueError(f"Attribute '{field_name}' is not available for {obj_name}")

        # Exclude sensitive fields
        if field_name in ("feedback", "bonus"):
            raise ValueError("Access to sensitive information is prohibited")

        return getattr(target_obj, field_name)

    # 4. Render the template
    def replacement(match):
        ph = match.group(1)
        return str(_safe_attr(None, ph))

    result = placeholder_pattern.sub(replacement, template)
    return result


# ------------------------------------------------------------------
# Example usage (commented out – remove comments to test)
# ------------------------------------------------------------------
# if __name__ == "__main__":
#     tmpl = ("Employee {employee.name} ({employee.position}) in "
#             "{employee.department} received a rating of "
#             "{performance.rating}.")
#     print(generate_employee_summary("E001", tmpl))