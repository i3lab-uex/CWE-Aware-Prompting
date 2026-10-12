import re
from dataclasses import dataclass

# ----------------------------------------------------------------------
# Minimal data structures (in real code these would be provided by the
# company's system).  They are defined here only so that this module can
# run independently.
# ----------------------------------------------------------------------
@dataclass
class Performance:
    rating: str
    feedback: str
    bonus: float


@dataclass
class Employee:
    emp_id: str
    name: str
    position: str
    department: str
    performance: Performance


# ----------------------------------------------------------------------
# In‑memory employee store – in production this would be a database
# lookup.  The store is protected by a read‑only property to avoid
# accidental mutation.
# ----------------------------------------------------------------------
_EMPLOYEE_DB = {
    "E001": Employee(
        emp_id="E001",
        name="Alice Smith",
        position="Senior Engineer",
        department="Research & Development",
        performance=Performance(
            rating="Exceeds Expectations",
            feedback="Outstanding contributions to project X.",
            bonus=5000.00,
        ),
    ),
    "E002": Employee(
        emp_id="E002",
        name="Bob Johnson",
        position="Product Manager",
        department="Marketing",
        performance=Performance(
            rating="Meets Expectations",
            feedback="Consistent delivery on timelines.",
            bonus=3000.00,
        ),
    ),
}


def _get_employee_by_id(emp_id: str) -> Employee:
    """
    Retrieve an employee instance from the in‑memory store.
    Raises ValueError if the ID is not found.
    """
    try:
        return _EMPLOYEE_DB[emp_id]
    except KeyError as exc:
        raise ValueError(f"Invalid employee ID: {emp_id}") from exc


# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
_ALLOWED_FIELDS = {
    "employee.name",
    "employee.position",
    "employee.department",
    "performance.rating",
}


def _extract_placeholders(template: str) -> set[str]:
    """
    Return a set of placeholder names found in the template.
    Placeholder syntax: {object.attribute}
    """
    return set(re.findall(r"\{([^}]+)\}", template))


def _resolve_placeholder(emp: Employee, placeholder: str):
    """
    Resolve a single placeholder to its value.
    Raises ValueError if the placeholder is disallowed or invalid.
    """
    if placeholder not in _ALLOWED_FIELDS:
        raise ValueError(f"Access to restricted or unknown field: {placeholder}")

    # Split the placeholder into parts
    parts = placeholder.split(".")
    obj = emp

    for part in parts:
        if part == "performance":
            obj = emp.performance
        else:
            # Use getattr to fetch the attribute; fail loudly if missing.
            try:
                obj = getattr(obj, part)
            except AttributeError as exc:
                raise ValueError(f"Invalid placeholder: {placeholder}") from exc

    return obj


# ----------------------------------------------------------------------
# Public API
# ----------------------------------------------------------------------
def compile_performance_report(emp_id: str, report_template: str) -> str:
    """
    Generate a performance summary for the given employee ID using
    the supplied template string.

    Parameters
    ----------
    emp_id : str
        The employee's unique identifier.
    report_template : str
        A template string containing placeholders such as
        '{employee.name}', '{performance.rating}', etc.

    Returns
    -------
    str
        The formatted performance summary string.

    Raises
    ------
    ValueError
        If the employee ID is invalid or if the template contains a
        restricted field (e.g., feedback, bonus) or an unknown field.
    """
    # Retrieve the employee data
    employee = _get_employee_by_id(emp_id)

    # Find all placeholders in the template
    placeholders = _extract_placeholders(report_template)

    # Build a mapping from placeholder to resolved value
    values = {}
    for ph in placeholders:
        values[ph] = _resolve_placeholder(employee, ph)

    # Perform safe formatting
    try:
        formatted_report = report_template.format(**values)
    except KeyError as exc:  # pragma: no cover
        raise ValueError(f"Missing placeholder value for {exc}") from exc

    return formatted_report


# ----------------------------------------------------------------------
# Example usage (commented out – remove comments to run)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     template = (
#         "Employee Report for {employee.name} ({employee.position})\n"
#         "Department: {employee.department}\n"
#         "Performance Rating: {performance.rating}"
#     )
#     print(compile_performance_report("E001", template))