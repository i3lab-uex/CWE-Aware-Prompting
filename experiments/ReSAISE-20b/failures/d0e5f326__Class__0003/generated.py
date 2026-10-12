import re
from dataclasses import dataclass

# ----------------------------------------------------------------------
# Mocked domain classes (in a real system these would be imported)
# ----------------------------------------------------------------------
@dataclass
class Performance:
    rating: str          # e.g. "Excellent"
    feedback: str        # sensitive
    bonus: float         # sensitive


@dataclass
class Employee:
    id: str
    name: str
    position: str
    performance: Performance


# ----------------------------------------------------------------------
# In-memory "database" for demonstration purposes
# ----------------------------------------------------------------------
_EMPLOYEE_DB = {
    "E001": Employee(
        id="E001",
        name="Alice Johnson",
        position="Software Engineer",
        performance=Performance(
            rating="Outstanding",
            feedback="Excellent teamwork and problem solving.",
            bonus=5000.00,
        ),
    ),
    "E002": Employee(
        id="E002",
        name="Bob Smith",
        position="Product Manager",
        performance=Performance(
            rating="Exceeds Expectations",
            feedback="Delivered project on time with high quality.",
            bonus=7500.00,
        ),
    ),
}


def _get_employee(employee_id: str) -> Employee:
    """
    Retrieve an employee from the mock database.
    Raises ValueError if the ID is not found.
    """
    try:
        return _EMPLOYEE_DB[employee_id]
    except KeyError as exc:
        raise ValueError(f"Employee ID '{employee_id}' is invalid.") from exc


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def build_employee_report(employee_id: str, template: str) -> str:
    """
    Build a performance report for an employee based on the supplied template.

    The template may contain placeholders in the form `{staff.name}`, `{staff.position}`,
    and `{evaluation.rating}`.  Any attempt to access sensitive fields such as
    `feedback` or `bonus` will raise a ValueError.

    Parameters:
        employee_id (str): The unique identifier of the employee.
        template (str):  The report template containing placeholders.

    Returns:
        str: A fully rendered performance summary.

    Raises:
        ValueError: If the employee ID is unknown or if the template attempts to
                    access sensitive data.
    """
    # Retrieve employee record (validation is performed in the helper)
    employee = _get_employee(employee_id)

    # Allowed placeholders mapping
    placeholder_map = {
        "staff.name": employee.name,
        "staff.position": employee.position,
        "evaluation.rating": employee.performance.rating,
    }

    # Find all placeholders in the template
    pattern = re.compile(r"\{([^}]+)\}")
    tokens = pattern.findall(template)

    # Validate and replace placeholders
    for token in tokens:
        if token in {"feedback", "bonus"} or re.search(r"\b(feedback|bonus)\b", token):
            raise ValueError(
                f"Unauthorized access to sensitive information: '{token}'."
            )

        if token not in placeholder_map:
            raise ValueError(f"Unknown placeholder '{token}' in template.")

    # Perform the substitution
    def replacer(match: re.Match) -> str:
        key = match.group(1)
        return placeholder_map[key]

    rendered_report = pattern.sub(replacer, template)

    return rendered_report


# ----------------------------------------------------------------------
# Example usage (would normally be in a separate test module)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = (
        "Employee Report for {staff.name} ({staff.position}):\n"
        "Performance Rating: {evaluation.rating}\n"
    )
    print(build_employee_report("E001", tmpl))