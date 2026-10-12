import re
from dataclasses import dataclass, field
from typing import List

# --- Mock employee data ---------------------------------------------
@dataclass
class Employee:
    name: str
    position: str
    department: str
    salary: float = field(repr=False)          # sensitive
    personal_email: str = field(repr=False)   # sensitive

# Example employee list (in a real system this would come from a DB or API)
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Software Engineer", "Engineering", 95000, "alice.smith@example.com"),
    Employee("Bob Johnson", "DevOps Engineer", "Engineering", 88000, "bob.johnson@example.com"),
    Employee("Carol Williams", "HR Manager", "Human Resources", 72000, "carol.williams@example.com"),
    Employee("David Brown", "Accountant", "Finance", 68000, "david.brown@example.com"),
]

# --- Core function ---------------------------------------------
def generate_staff_listing(dep: str, format_template: str) -> str:
    """
    Generate a directory listing for all employees in the given department,
    formatted according to `format_template`.

    Parameters
    ----------
    dep : str
        The department name whose employees should be listed.
    format_template : str
        A template string containing placeholders like `{employee.name}`.

    Returns
    -------
    str
        The formatted directory listing, one employee per line.

    Raises
    ------
    ValueError
        If the template references a sensitive field (`salary` or `personal_email`)
        or if any other error occurs during formatting.
    """
    # Define the set of disallowed fields
    disallowed = {"salary", "personal_email"}

    # Find all placeholders in the template
    placeholder_pattern = re.compile(r"{\s*employee\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")
    placeholders = placeholder_pattern.findall(format_template)

    # Check for disallowed fields
    if any(field in disallowed for field in placeholders):
        raise ValueError("Template references a sensitive employee attribute.")

    # Filter employees by department
    filtered = [e for e in EMPLOYEES if e.department.lower() == dep.lower()]
    if not filtered:
        return f"No employees found in department '{dep}'."

    # Build the directory string
    lines = []
    for emp in filtered:
        try:
            line = format_template.format(employee=emp)
        except Exception as exc:
            # Wrap any formatting error in ValueError
            raise ValueError(f"Error while formatting employee data: {exc}") from exc
        lines.append(line)

    return "\n".join(lines)


# --- Example usage ---------------------------------------------
if __name__ == "__main__":
    try:
        template = "Name: {employee.name}, Position: {employee.position}"
        print(generate_staff_listing("Engineering", template))
    except ValueError as e:
        print(f"Error: {e}")