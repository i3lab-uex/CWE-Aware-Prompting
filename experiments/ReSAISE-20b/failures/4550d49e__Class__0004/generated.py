import re
from typing import Dict

# ------------------------------------------------------------------
# Mock data structures – in a real system these would be imported
# from the company's domain model.
# ------------------------------------------------------------------
class Employee:
    def __init__(self, emp_id: str, name: str, position: str,
                 department: str, performance):
        self.id = emp_id
        self.name = name
        self.position = position
        self.department = department
        self.performance = performance


class Performance:
    def __init__(self, rating: str, feedback: str, bonus: float):
        self.rating = rating
        self.feedback = feedback
        self.bonus = bonus


# ------------------------------------------------------------------
# In‑memory “database” of employees – replace with real persistence
# ------------------------------------------------------------------
EMPLOYEES_DB: Dict[str, Employee] = {}


def get_employee(emp_id: str) -> Employee:
    """Retrieve an employee by ID, or raise KeyError if not found."""
    try:
        return EMPLOYEES_DB[emp_id]
    except KeyError as exc:
        raise ValueError(f"Employee ID '{emp_id}' not found.") from exc


# ------------------------------------------------------------------
# The function required by the task
# ------------------------------------------------------------------
PLACEHOLDER_PATTERN = re.compile(r"\{(?P<scope>\w+)\.(?P<field>\w+)\}")

# Allowed fields per scope
ALLOWED_FIELDS = {
    "employee": {"name", "position", "department"},
    "performance": {"rating"}
}


def construct_employee_report(employee_id: str, report_template: str) -> str:
    """
    Construct a performance summary for the given employee.

    Args:
        employee_id: The unique identifier of an employee.
        report_template: A template string containing placeholders such
                         as `{employee.name}` or `{performance.rating}`.

    Returns:
        A formatted string with all placeholders replaced by actual data.

    Raises:
        ValueError: If the employee ID is invalid or if the template
                    references restricted fields.
    """
    # 1. Retrieve employee data
    employee = get_employee(employee_id)

    # 2. Validate placeholders and build a mapping of values
    def replace_match(match: re.Match) -> str:
        scope = match.group("scope")
        field = match.group("field")

        # Check that the placeholder is allowed
        if scope not in ALLOWED_FIELDS:
            raise ValueError(f"Invalid placeholder scope '{scope}'.")
        if field not in ALLOWED_FIELDS[scope]:
            raise ValueError(
                f"Access to restricted field '{field}' in scope '{scope}'."
            )

        # Retrieve the value
        if scope == "employee":
            return str(getattr(employee, field))
        else:  # performance
            return str(getattr(employee.performance, field))

    # 3. Perform substitution
    try:
        result = PLACEHOLDER_PATTERN.sub(replace_match, report_template)
    except ValueError as exc:
        # Re‑raise to expose the specific validation error
        raise

    return result


# ------------------------------------------------------------------
# Example usage (would normally be omitted from the module)
# ------------------------------------------------------------------
if __name__ == "__main__":
    # Populate mock database
    perf = Performance(rating="Excellent", feedback="Great work!", bonus=5000)
    EMPLOYEES_DB["E123"] = Employee(
        emp_id="E123",
        name="Jane Doe",
        position="Software Engineer",
        department="Engineering",
        performance=perf,
    )

    template = (
        "Employee Report:\n"
        "Name: {employee.name}\n"
        "Position: {employee.position}\n"
        "Department: {employee.department}\n"
        "Rating: {performance.rating}"
    )

    print(construct_employee_report("E123", template))