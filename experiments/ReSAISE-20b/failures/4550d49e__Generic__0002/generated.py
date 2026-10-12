import re
from dataclasses import dataclass
from typing import Dict

# --------------------------------------------------------------------------- #
# Dummy data structures – in a real system these would be replaced by ORM models
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class Performance:
    rating: str
    feedback: str
    bonus: float


@dataclass(frozen=True)
class Employee:
    employee_id: str
    name: str
    position: str
    department: str
    performance: Performance


# Example in‑memory store of employees (replace with a DB query in production)
EMPLOYEE_STORE: Dict[str, Employee] = {
    "E001": Employee(
        employee_id="E001",
        name="Alice Smith",
        position="Software Engineer",
        department="Engineering",
        performance=Performance(
            rating="Excellent",
            feedback="Outstanding contribution to the project.",
            bonus=1500.00,
        ),
    ),
    "E002": Employee(
        employee_id="E002",
        name="Bob Johnson",
        position="Product Manager",
        department="Product",
        performance=Performance(
            rating="Good",
            feedback="Delivered product on time.",
            bonus=1200.00,
        ),
    ),
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def _get_employee(employee_id: str) -> Employee:
    """Retrieve an employee from the store, raising ValueError if not found."""
    try:
        return EMPLOYEE_STORE[employee_id]
    except KeyError as exc:
        raise ValueError(f"Employee ID '{employee_id}' not found.") from exc


def _extract_placeholders(template: str):
    """Return a set of unique placeholders found in the template."""
    # Matches {something} including nested attributes like {employee.name}
    return set(re.findall(r"{([^{}]+)}", template))


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #
def construct_employee_report(employee_id: str, report_template: str) -> str:
    """
    Construct a performance report for the given employee ID using the provided template.

    Parameters
    ----------
    employee_id : str
        The unique identifier of the employee.
    report_template : str
        A template string containing placeholders such as {employee.name},
        {performance.rating}, etc.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the employee ID does not exist, or if the template attempts to
        access restricted fields like 'feedback' or 'bonus'.
    """
    # Restricted attributes that must not be exposed
    RESTRICTED = {"feedback", "bonus"}

    employee = _get_employee(employee_id)

    placeholders = _extract_placeholders(report_template)
    values: Dict[str, str] = {}

    for placeholder in placeholders:
        # Split into object and attribute parts: e.g. employee.name -> ["employee", "name"]
        parts = placeholder.split(".")
        if len(parts) != 2:
            raise ValueError(f"Invalid placeholder format: '{{{placeholder}}}'")

        obj_name, attr_name = parts

        # Validate restricted fields
        if attr_name in RESTRICTED:
            raise ValueError(
                f"Access to restricted field '{attr_name}' is not allowed in the report."
            )

        # Resolve the value from the employee object
        try:
            if obj_name == "employee":
                val = getattr(employee, attr_name)
            elif obj_name == "performance":
                val = getattr(employee.performance, attr_name)
            else:
                raise ValueError(f"Unknown placeholder object '{obj_name}'.")
        except AttributeError as exc:
            raise ValueError(
                f"Attribute '{attr_name}' not found on '{obj_name}'."
            ) from exc

        values[placeholder] = str(val)

    # Perform safe formatting
    try:
        report = report_template.format(**values)
    except KeyError as exc:
        raise ValueError(f"Missing value for placeholder: {exc}") from exc

    return report


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
# if __name__ == "__main__":
#     tmpl = (
#         "Employee Report for {employee.name} ({employee.position})\n"
#         "Department: {employee.department}\n"
#         "Performance Rating: {performance.rating}"
#     )
#     print(construct_employee_report("E001", tmpl))