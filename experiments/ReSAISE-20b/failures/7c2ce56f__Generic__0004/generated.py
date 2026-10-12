import re
from typing import List

# Minimal Employee class for demonstration purposes.
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# Example employee data (in a real scenario this would come from a database or API)
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Software Engineer", "Engineering", 95000.0, "alice.smith@example.com"),
    Employee("Bob Johnson", "Product Manager", "Engineering", 105000.0, "bob.johnson@example.com"),
    Employee("Carol Lee", "HR Specialist", "Human Resources", 70000.0, "carol.lee@example.com"),
    # Add more employees as needed
]

# Set of attributes that are considered sensitive and must not be exposed in the template.
SENSITIVE_ATTRIBUTES = {"salary", "personal_email"}


def _extract_placeholders(template: str) -> List[str]:
    """
    Extract all placeholders of the form {employee.<attribute>} from a template string.
    Returns a list of attribute names.
    """
    pattern = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")
    return pattern.findall(template)


def _replace_placeholders(employee: Employee, template: str) -> str:
    """
    Replace placeholders in the template with actual employee attribute values.
    Raises ValueError if a sensitive attribute is requested or if any other error occurs.
    """
    def replacement(match):
        attr = match.group(1)
        if attr in SENSITIVE_ATTRIBUTES:
            raise ValueError(f"Access to sensitive attribute '{attr}' is prohibited.")
        try:
            return str(getattr(employee, attr))
        except AttributeError as exc:
            raise ValueError(f"Employee has no attribute '{attr}'.") from exc
        except Exception as exc:
            raise ValueError(f"Error accessing attribute '{attr}': {exc}") from exc

    pattern = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")
    try:
        return pattern.sub(replacement, template)
    except Exception as exc:
        raise ValueError(f"Failed to replace placeholders: {exc}") from exc


def build_team_directory(team: str, template_text: str) -> str:
    """
    Build a formatted employee directory for the specified team (department).
    
    Parameters
    ----------
    team : str
        The department name used to filter employees.
    template_text : str
        A string containing placeholders like '{employee.name}' or '{employee.position}'.
    
    Returns
    -------
    str
        A directory string with each employee's information formatted according to the template.
    
    Raises
    ------
    ValueError
        If a sensitive attribute is requested, if an unknown attribute is referenced,
        or if any other error occurs during processing.
    """
    # Validate that the template contains only allowed placeholders
    placeholders = set(_extract_placeholders(template_text))
    if not placeholders:
        raise ValueError("Template does not contain any valid employee placeholders.")
    
    # Filter employees by department
    selected_employees = [emp for emp in EMPLOYEES if emp.department.lower() == team.lower()]
    if not selected_employees:
        raise ValueError(f"No employees found in department '{team}'.")
    
    # Build the directory
    formatted_entries = []
    for emp in selected_employees:
        try:
            entry = _replace_placeholders(emp, template_text)
            formatted_entries.append(entry)
        except ValueError as exc:
            # Wrap the error with context
            raise ValueError(f"Error processing employee '{emp.name}': {exc}") from exc
    
    return "\n".join(formatted_entries)


# Example usage (uncomment to test):
# if __name__ == "__main__":
#     template = "Name: {employee.name}\nPosition: {employee.position}\n"
#     print(build_team_directory("Engineering", template))