import re
from string import Formatter
from dataclasses import dataclass

# ----------------------------------------------------------------------
# Mock data structures and retrieval functions (replace with real DB calls)
# ----------------------------------------------------------------------


@dataclass
class Performance:
    rating: str          # e.g. "Excellent", "Needs Improvement"
    feedback: str        # Sensitive – should not be exposed
    bonus: float         # Sensitive – should not be exposed


@dataclass
class Employee:
    employee_id: str
    name: str
    position: str
    department: str
    performance: Performance


# In‑memory store for demonstration purposes
_EMPLOYEES_DB = {
    "E001": Employee(
        employee_id="E001",
        name="Alice Smith",
        position="Software Engineer",
        department="Engineering",
        performance=Performance(
            rating="Excellent",
            feedback="Great problem‑solving skills.",
            bonus=5000.00,
        ),
    ),
    "E002": Employee(
        employee_id="E002",
        name="Bob Johnson",
        position="Product Manager",
        department="Product",
        performance=Performance(
            rating="Meets Expectations",
            feedback="Consistent delivery.",
            bonus=3000.00,
        ),
    ),
}


def _get_employee_by_id(employee_id: str) -> Employee:
    """Retrieve an employee by ID or raise ValueError."""
    try:
        return _EMPLOYEES_DB[employee_id]
    except KeyError as exc:
        raise ValueError(f"Employee ID '{employee_id}' not found.") from exc


# ----------------------------------------------------------------------
# Core function
# ----------------------------------------------------------------------


_ALLOWED_FIELDS = {
    "employee.name",
    "employee.position",
    "performance.rating",
}


def construct_employee_report(employee_id: str, report_template: str) -> str:
    """
    Construct a performance summary for an employee.

    Parameters
    ----------
    employee_id : str
        The unique identifier of the employee.
    report_template : str
        A template string containing placeholders such as
        '{employee.name}', '{performance.rating}', etc.

    Returns
    -------
    str
        The formatted performance summary.

    Raises
    ------
    ValueError
        If the employee ID is invalid or if the template references a
        restricted field (e.g. feedback, bonus).
    """
    # 1️⃣ Validate and fetch employee data
    employee = _get_employee_by_id(employee_id)

    # 2️⃣ Inspect the template for placeholders
    formatter = Formatter()
    fields_in_template = {
        field_name
        for _, field_name, _, _ in formatter.parse(report_template)
        if field_name  # ignore empty fields
    }

    # 3️⃣ Ensure no restricted fields are used
    for field in fields_in_template:
        if field not in _ALLOWED_FIELDS:
            raise ValueError(
                f"Template references restricted or unknown field '{field}'. "
                "Allowed fields: employee.name, employee.position, performance.rating."
            )

    # 4️⃣ Build a mapping for formatting
    mapping = {
        "employee.name": employee.name,
        "employee.position": employee.position,
        "performance.rating": employee.performance.rating,
    }

    # 5️⃣ Format and return the report
    try:
        return report_template.format(**mapping)
    except KeyError as exc:
        # Should never happen due to prior validation, but guard anyway
        raise ValueError(f"Missing value for placeholder: {exc}") from exc


# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Employee Report:\n"
        "- Name: {employee.name}\n"
        "- Position: {employee.position}\n"
        "- Rating: {performance.rating}"
    )
    print(construct_employee_report("E001", template))