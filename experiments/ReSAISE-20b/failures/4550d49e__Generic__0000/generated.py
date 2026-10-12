import re
from typing import Dict

# --------------------------------------------------------------------
# Mocked data structures (replace with real implementations)
# --------------------------------------------------------------------

class Performance:
    """Represents an employee's performance data."""
    def __init__(self, rating: str, feedback: str = "", bonus: float = 0.0):
        self.rating = rating
        self.feedback = feedback
        self.bonus = bonus


class Employee:
    """Represents an employee."""
    def __init__(
        self,
        emp_id: str,
        name: str,
        position: str,
        department: str,
        performance: Performance,
    ):
        self.emp_id = emp_id
        self.name = name
        self.position = position
        self.department = department
        self.performance = performance


# --------------------------------------------------------------------
# In‑memory repository of employees (replace with real data source)
# --------------------------------------------------------------------

_EMPLOYEE_DB: Dict[str, Employee] = {}

def _load_mock_data() -> None:
    """Populate the in‑memory database with some example employees."""
    _EMPLOYEE_DB["E001"] = Employee(
        emp_id="E001",
        name="Alice Smith",
        position="Software Engineer",
        department="Engineering",
        performance=Performance(rating="Exceeds Expectations", feedback="Great work!", bonus=1200.0),
    )
    _EMPLOYEE_DB["E002"] = Employee(
        emp_id="E002",
        name="Bob Johnson",
        position="Product Manager",
        department="Product",
        performance=Performance(rating="Meets Expectations", feedback="Satisfactory", bonus=800.0),
    )


_load_mock_data()


# --------------------------------------------------------------------
# Helper utilities
# --------------------------------------------------------------------

_ALLOWED_PLACEHOLDERS = {
    "employee.name",
    "employee.position",
    "employee.department",
    "performance.rating",
}

_RESTRICTED_PLACEHOLDERS = {
    "performance.feedback",
    "performance.bonus",
}

# Regex to capture the key inside a format placeholder
_PLACEHOLDER_REGEX = re.compile(r"{([^{}]+)}")


def _extract_placeholders(template: str) -> set[str]:
    """Return a set of placeholder keys found in the template."""
    return set(_PLACEHOLDER_REGEX.findall(template))


def _validate_placeholders(placeholders: set[str]) -> None:
    """Ensure placeholders are allowed and not restricted."""
    for key in placeholders:
        if key in _RESTRICTED_PLACEHOLDERS:
            raise ValueError(f"Access to restricted field '{key}' is not allowed.")
        if key not in _ALLOWED_PLACEHOLDERS:
            raise ValueError(f"Unknown placeholder '{key}'.")


def _build_context(employee: Employee) -> dict:
    """Create a context dictionary for template formatting."""
    return {
        "employee": employee,
        "performance": employee.performance,
    }


# --------------------------------------------------------------------
# Main function
# --------------------------------------------------------------------

def construct_employee_report(employee_id: str, report_template: str) -> str:
    """
    Generate a formatted performance report for the given employee.

    Parameters
    ----------
    employee_id : str
        The unique identifier of the employee.
    report_template : str
        A string containing placeholders like '{employee.name}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the employee ID is unknown, or if the template contains restricted or unknown fields.
    """
    # Retrieve employee
    employee = _EMPLOYEE_DB.get(employee_id)
    if not employee:
        raise ValueError(f"Employee ID '{employee_id}' does not exist.")

    # Extract and validate placeholders
    placeholders = _extract_placeholders(report_template)
    _validate_placeholders(placeholders)

    # Build context and format
    context = _build_context(employee)
    try:
        formatted_report = report_template.format(**context)
    except KeyError as exc:
        # This should not happen due to earlier validation, but guard anyway
        raise ValueError(f"Missing data for placeholder '{exc.args[0]}'") from exc

    return formatted_report


# --------------------------------------------------------------------
# Example usage (commented out – remove for production)
# --------------------------------------------------------------------

if __name__ == "__main__":
    template = (
        "Employee Report\n"
        "----------------\n"
        "Name: {employee.name}\n"
        "Position: {employee.position}\n"
        "Department: {employee.department}\n"
        "Rating: {performance.rating}\n"
    )
    print(construct_employee_report("E001", template))