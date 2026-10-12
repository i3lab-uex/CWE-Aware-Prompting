import re
from typing import Dict, Any

# Assuming these classes exist in the surrounding codebase.
class Employee:
    def __init__(self, name: str, position: str, department: str):
        self.name = name
        self.position = position
        self.department = department

class Performance:
    def __init__(self, rating: str):
        self.rating = rating
        # The following fields are considered restricted and must not be exposed
        self.feedback = "Sensitive feedback"
        self.bonus = 5000

# Dummy data store for illustration purposes
EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee("Alice Smith", "Senior Analyst", "Finance"),
    "E002": Employee("Bob Johnson", "Developer", "Engineering")
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance("Excellent"),
    "E002": Performance("Good")
}

# Restricted fields that must not appear in the template
RESTRICTED_FIELDS = {"feedback", "bonus"}

# Regular expression to find placeholders like {employee.name} or {performance.rating}
PLACEHOLDER_RE = re.compile(r"\{(?P<obj>employee|performance)\.(?P<attr>\w+)\}")

def build_employee_summary(emp_key: str, template_str: str) -> str:
    """
    Build a summary string for the given employee using the provided template.

    Args:
        emp_key (str): Identifier of the employee.
        template_str (str): Template containing placeholders.

    Returns:
        str: Formatted summary string.

    Raises:
        ValueError: If the employee does not exist, a restricted field is requested,
                    or an unknown placeholder appears.
    """
    # Retrieve employee and performance objects
    emp = EMPLOYEES.get(emp_key)
    perf = PERFORMANCES.get(emp_key)

    if emp is None or perf is None:
        raise ValueError(f"Employee with key '{emp_key}' not found.")

    # Function to resolve a single placeholder
    def replace_match(match: re.Match) -> str:
        obj_name = match.group("obj")
        attr_name = match.group("attr")

        # Check for restricted fields
        if attr_name in RESTRICTED_FIELDS:
            raise ValueError(f"Access to restricted field '{attr_name}' is not allowed.")

        # Resolve attribute
        if obj_name == "employee":
            source = emp
        elif obj_name == "performance":
            source = perf
        else:
            raise ValueError(f"Unknown object '{obj_name}' in placeholder.")

        if not hasattr(source, attr_name):
            raise ValueError(f"Attribute '{attr_name}' does not exist on {obj_name}.")

        return str(getattr(source, attr_name))

    # Perform substitution
    try:
        result = PLACEHOLDER_RE.sub(replace_match, template_str)
    except ValueError as e:
        raise

    return result