import re
from dataclasses import dataclass, fields
from typing import List

# Minimal Employee definition for demonstration purposes.
@dataclass
class Employee:
    name: str
    position: str
    department: str
    salary: float
    personal_email: str


def generate_department_directory(dept_name: str, dir_template: str) -> str:
    """
    Generate a formatted employee directory for the given department.

    Parameters
    ----------
    dept_name : str
        The name of the department to filter employees.
    dir_template : str
        A template string containing placeholders like '{employee.name}'.

    Returns
    -------
    str
        The formatted directory string for all employees in the specified department.

    Raises
    ------
    ValueError
        If a placeholder refers to a sensitive attribute (salary or personal_email)
        or if any error occurs during processing.
    """
    # Regular expression to find placeholders of the form {employee.attribute}
    placeholder_pattern = re.compile(r'\{employee\.([^\}]+)\}')

    # Collect all placeholders used in the template
    placeholders = placeholder_pattern.findall(dir_template)

    # Disallow sensitive fields
    sensitive_fields = {'salary', 'personal_email'}
    for ph in placeholders:
        if ph.lower() in sensitive_fields:
            raise ValueError(f"Access to sensitive field '{ph}' is not allowed.")

    # Fetch all Employee instances (in a real system this might come from a DB or API)
    try:
        all_employees: List[Employee] = _get_all_employees()
    except Exception as exc:
        raise ValueError(f"Failed to retrieve employee data: {exc}") from exc

    # Filter employees by department
    dept_employees = [emp for emp in all_employees if emp.department == dept_name]

    # Prepare the formatted output
    formatted_entries = []
    for emp in dept_employees:
        try:
            # Build a mapping from placeholder names to attribute values
            emp_dict = {field.name: getattr(emp, field.name) for field in fields(Employee)}
            entry = dir_template.format(employee=emp_dict)
            formatted_entries.append(entry)
        except KeyError as exc:
            raise ValueError(f"Template references unknown attribute: {exc}") from exc
        except Exception as exc:
            raise ValueError(f"Error formatting entry for employee '{emp.name}': {exc}") from exc

    return "\n".join(formatted_entries)


# ----------------------------------------------------------------------
# Helper functions (mocked for this example)
# ----------------------------------------------------------------------
def _get_all_employees() -> List[Employee]:
    """
    Mock function to return a list of Employee objects.
    Replace this with actual data retrieval logic in production.
    """
    return [
        Employee("Alice Smith", "Engineer", "Engineering", 95000.0, "alice.smith@example.com"),
        Employee("Bob Johnson", "Manager", "Engineering", 120000.0, "bob.johnson@example.com"),
        Employee("Carol Lee", "Analyst", "Marketing", 70000.0, "carol.lee@example.com"),
    ]


# ----------------------------------------------------------------------
# Example usage (commented out; remove comments to test)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     template = "Name: {employee.name}, Position: {employee.position}"
#     print(generate_department_directory("Engineering", template))