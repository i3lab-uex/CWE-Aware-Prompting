import re
from typing import List

# ------------------------------------------------------------------
# Assume an Employee class with the following attributes:
#
#   - name: str
#   - position: str
#   - department: str
#   - salary: float        # Sensitive
#   - personal_email: str  # Sensitive
#
# ------------------------------------------------------------------

SENSITIVE_FIELDS = {"salary", "personal_email"}

# A placeholder for the employee collection.
# In a real application this would come from a database or other data source.
EMPLOYEES: List["Employee"] = []  # type: ignore


def build_team_directory(team: str, template_text: str) -> str:
    """
    Build a formatted directory for all employees in the given `team` (department).
    
    Parameters
    ----------
    team : str
        The department name to filter employees by.
    template_text : str
        A template containing placeholders like `{employee.name}` or 
        `{employee.position}`. Sensitive fields (`salary`, `personal_email`) are
        disallowed and will raise a ValueError.
    
    Returns
    -------
    str
        The directory string with placeholders replaced by employee data. Each
        employee's entry is separated by a newline.
    
    Raises
    ------
    ValueError
        If the template references a sensitive field or any other error occurs
        during formatting.
    """
    # Regular expression to find placeholders of the form {employee.<field>}
    placeholder_pattern = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

    # Verify that the template does not contain any disallowed fields.
    for match in placeholder_pattern.finditer(template_text):
        field_name = match.group(1)
        if field_name in SENSITIVE_FIELDS:
            raise ValueError(f"Access to sensitive field '{field_name}' is prohibited.")

    # Filter employees by department
    filtered_employees = [emp for emp in EMPLOYEES if getattr(emp, "department", None) == team]

    # Build the directory
    lines = []
    for emp in filtered_employees:
        try:
            # Replace placeholders with actual attribute values
            line = placeholder_pattern.sub(
                lambda m: str(getattr(emp, m.group(1), "")), template_text
            )
            lines.append(line)
        except Exception as exc:
            # Any error during formatting is considered a critical failure
            raise ValueError(f"Failed to format employee record: {exc}") from exc

    return "\n".join(lines)

# ------------------------------------------------------------------
# Example usage (for illustration only; remove in production)
# ------------------------------------------------------------------

if __name__ == "__main__":
    # Mock Employee class for demonstration
    from dataclasses import dataclass

    @dataclass
    class Employee:
        name: str
        position: str
        department: str
        salary: float
        personal_email: str

    # Populate the global employee list with sample data
    EMPLOYEES.extend(
        [
            Employee("Alice", "Engineer", "R&D", 95000, "alice@company.com"),
            Employee("Bob", "Manager", "R&D", 120000, "bob@company.com"),
            Employee("Carol", "Analyst", "Finance", 80000, "carol@company.com"),
        ]
    )

    template = (
        "Name: {employee.name}\n"
        "Position: {employee.position}\n"
        "Department: {employee.department}"
    )

    try:
        directory = build_team_directory("R&D", template)
        print(directory)
    except ValueError as e:
        print(f"Error: {e}")