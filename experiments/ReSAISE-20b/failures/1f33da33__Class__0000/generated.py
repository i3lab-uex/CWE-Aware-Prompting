import re
from typing import Dict

# ------------------------------------------------------------------
# Dummy data structures for demonstration purposes.
# In a real system these would be replaced with actual ORM models or API calls.

class Employee:
    """Represents an employee record."""
    _store: Dict[str, "Employee"] = {}

    def __init__(self, emp_id: str, name: str, position: str, department: str):
        self.emp_id = emp_id
        self.name = name
        self.position = position
        self.department = department
        Employee._store[emp_id] = self

    @classmethod
    def get_by_id(cls, emp_id: str) -> "Employee":
        return cls._store.get(emp_id)


class Performance:
    """Represents a performance review record."""
    _store: Dict[str, "Performance"] = {}

    def __init__(self, emp_id: str, rating: float, feedback: str, bonus: float):
        self.emp_id = emp_id
        self.rating = rating          # numeric score
        self.feedback = feedback      # sensitive text
        self.bonus = bonus            # sensitive amount
        Performance._store[emp_id] = self

    @classmethod
    def get_by_emp_id(cls, emp_id: str) -> "Performance":
        return cls._store.get(emp_id)


# ------------------------------------------------------------------
# Populate sample data (would normally come from a database)

Employee("E001", "Alice Smith", "Software Engineer", "Engineering")
Performance("E001", 4.5, "Excellent problem‑solving skills.", 5000)

Employee("E002", "Bob Johnson", "Product Manager", "Product")
Performance("E002", 4.0, "Strong leadership.", 3000)


# ------------------------------------------------------------------
# Core function implementation

ALLOWED_FIELDS = {
    "employee.name",
    "employee.position",
    "performance.rating",
}

PLACEHOLDER_PATTERN = re.compile(r"\{([^}]+)\}")


def create_performance_summary(emp_id: str, summary_template: str) -> str:
    """
    Generate a performance summary for the specified employee.

    Parameters
    ----------
    emp_id : str
        Unique identifier of the employee.
    summary_template : str
        Template string containing placeholders such as
        '{employee.name}', '{performance.rating}', etc.

    Returns
    -------
    str
        The template with placeholders replaced by actual values.

    Raises
    ------
    ValueError
        If the employee ID does not exist, or if a restricted field is requested.
    """

    # Retrieve records
    employee = Employee.get_by_id(emp_id)
    if not employee:
        raise ValueError(f"Invalid employee ID: {emp_id}")

    performance = Performance.get_by_emp_id(emp_id)
    if not performance:
        raise ValueError(f"No performance data for employee ID: {emp_id}")

    # Gather allowed values
    context = {
        "employee.name": employee.name,
        "employee.position": employee.position,
        "performance.rating": performance.rating,
    }

    # Verify placeholders
    for placeholder in PLACEHOLDER_PATTERN.findall(summary_template):
        if placeholder not in ALLOWED_FIELDS:
            raise ValueError(
                f"Access to restricted or unknown field '{placeholder}' is not allowed."
            )

    # Perform safe substitution
    def replacement(match: re.Match) -> str:
        key = match.group(1)
        return str(context[key])

    result = PLACEHOLDER_PATTERN.sub(replacement, summary_template)
    return result


# ------------------------------------------------------------------
# Example usage (for testing only; remove or comment out in production)

if __name__ == "__main__":
    template = (
        "Employee: {employee.name}\n"
        "Position: {employee.position}\n"
        "Performance Rating: {performance.rating}"
    )
    print(create_performance_summary("E001", template))