import re
from dataclasses import dataclass

# ----------------------------------------------------------------------
# Data model
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Employee:
    name: str
    position: str
    department: str


@dataclass(frozen=True)
class Performance:
    rating: float  # e.g. 4.5 out of 5


# ----------------------------------------------------------------------
# In‑memory data store (for demonstration purposes)
# ----------------------------------------------------------------------
EMPLOYEES = {
    "E001": Employee(name="Alice Smith", position="Software Engineer", department="Engineering"),
    "E002": Employee(name="Bob Johnson", position="Product Manager", department="Product"),
}

PERFORMANCES = {
    "E001": Performance(rating=4.7),
    "E002": Performance(rating=3.9),
}


# ----------------------------------------------------------------------
# Utility functions
# ----------------------------------------------------------------------
def _get_employee(emp_code: str) -> Employee:
    try:
        return EMPLOYEES[emp_code]
    except KeyError as exc:
        raise ValueError(f"Unknown employee code: {emp_code}") from exc


def _get_performance(emp_code: str) -> Performance:
    try:
        return PERFORMANCES[emp_code]
    except KeyError as exc:
        raise ValueError(f"No performance data for employee code: {emp_code}") from exc


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def create_performance_report(emp_code: str, summary_template: str) -> str:
    """
    Generate a formatted performance report for an employee.

    Parameters
    ----------
    emp_code : str
        Identifier of the employee.
    summary_template : str
        Template string containing placeholders such as
        '{employee.name}', '{employee.position}',
        '{performance.rating}'. Restricted fields (e.g. feedback,
        bonus) will raise a ValueError.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the employee code is unknown, or if the template contains
        restricted or invalid placeholders.
    """
    # Retrieve data
    employee = _get_employee(emp_code)
    performance = _get_performance(emp_code)

    # Allowed attributes
    allowed_attrs = {
        "employee": {"name", "position", "department"},
        "performance": {"rating"},
    }

    # Find all placeholders in the template
    pattern = re.compile(r"\{([^{}]+)\}")
    placeholders = pattern.findall(summary_template)

    # Build a mapping from placeholder to actual value
    replacements = {}
    for key in placeholders:
        parts = key.split(".")
        if len(parts) != 2:
            raise ValueError(f"Invalid placeholder format: '{{{key}}}'")
        obj_name, attr = parts
        if obj_name not in allowed_attrs:
            raise ValueError(f"Unknown object '{obj_name}' in placeholder '{{{key}}}'")
        if attr not in allowed_attrs[obj_name]:
            raise ValueError(f"Access to restricted or unknown attribute '{attr}' "
                             f"in placeholder '{{{key}}}'")

        # Retrieve the value
        if obj_name == "employee":
            replacements[key] = getattr(employee, attr)
        elif obj_name == "performance":
            replacements[key] = getattr(performance, attr)

    # Perform the replacement
    def _replace(match: re.Match) -> str:
        placeholder = match.group(1)
        return str(replacements[placeholder])

    formatted_report = pattern.sub(_replace, summary_template)

    return formatted_report


# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Employee Report\n"
        "Name: {employee.name}\n"
        "Position: {employee.position}\n"
        "Department: {employee.department}\n"
        "Performance Rating: {performance.rating}"
    )
    print(create_performance_report("E001", template))