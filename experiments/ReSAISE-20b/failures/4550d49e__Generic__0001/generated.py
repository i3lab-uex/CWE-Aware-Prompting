import re
from typing import Any

# Assume these classes are defined elsewhere in the codebase.
# They are imported here for type checking and documentation purposes.
try:
    from employee_module import Employee, Performance  # noqa: F401
except ImportError:
    # Minimal stubs for illustration; in production these will be real implementations.
    class Employee:  # pragma: no cover
        def __init__(self, employee_id: str, name: str, position: str, department: str):
            self.id = employee_id
            self.name = name
            self.position = position
            self.department = department

    class Performance:  # pragma: no cover
        def __init__(self, rating: float, feedback: str, bonus: float):
            self.rating = rating
            self.feedback = feedback
            self.bonus = bonus


# In a real system, these would be provided by a database or service layer.
# For this implementation we use simple in‑memory dictionaries for lookup.
EMPLOYEES_DB = {
    "E001": Employee("E001", "Alice Smith", "Software Engineer", "Engineering"),
    "E002": Employee("E002", "Bob Johnson", "Product Manager", "Product"),
}

PERFORMANCES_DB = {
    "E001": Performance(4.5, "Excellent teamwork and leadership.", 1200.00),
    "E002": Performance(3.8, "Strong analytical skills.", 950.00),
}


# Regex to find all placeholders of the form {object.attribute}
_PLACEHOLDER_RE = re.compile(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

# Attributes that are considered sensitive and must not be exposed.
_RESTRICTED_FIELDS = {"feedback", "bonus"}


def _get_employee(employee_id: str) -> Employee:
    """Retrieve an employee instance by ID, raising ValueError if not found."""
    try:
        return EMPLOYEES_DB[employee_id]
    except KeyError as exc:
        raise ValueError(f"Employee ID '{employee_id}' not found.") from exc


def _get_performance(employee_id: str) -> Performance:
    """Retrieve a performance instance by employee ID, raising ValueError if not found."""
    try:
        return PERFORMANCES_DB[employee_id]
    except KeyError as exc:
        raise ValueError(f"Performance data for employee ID '{employee_id}' not found.") from exc


def construct_employee_report(employee_id: str, report_template: str) -> str:
    """
    Construct a performance report for the given employee ID using the provided template.

    Parameters
    ----------
    employee_id : str
        The unique identifier of the employee.
    report_template : str
        A template string containing placeholders such as `{employee.name}` or `{performance.rating}`.

    Returns
    -------
    str
        The formatted report string with all placeholders replaced by actual values.

    Raises
    ------
    ValueError
        If the employee ID is invalid, if a placeholder references a restricted field,
        or if a placeholder refers to an unknown attribute.
    """
    employee = _get_employee(employee_id)
    performance = _get_performance(employee_id)

    def replacement(match: re.Match) -> str:
        obj_name, attr = match.group(1), match.group(2)

        # Prevent access to restricted fields
        if attr in _RESTRICTED_FIELDS:
            raise ValueError(f"Access to restricted field '{attr}' is not allowed in the report template.")

        # Resolve the object reference
        if obj_name == "employee":
            source = employee
        elif obj_name == "performance":
            source = performance
        else:
            raise ValueError(f"Unknown object '{obj_name}' in placeholder '{{{obj_name}.{attr}}}'.")
        # Fetch the attribute
        if not hasattr(source, attr):
            raise ValueError(f"Attribute '{attr}' does not exist on object '{obj_name}'.")
        value = getattr(source, attr)
        return str(value)

    try:
        report = _PLACEHOLDER_RE.sub(replacement, report_template)
    except ValueError as exc:
        # Re‑raise with context
        raise ValueError(f"Failed to construct report: {exc}") from exc

    return report