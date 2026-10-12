import re
from typing import List

# ------------------------------------------------------------------
# Example Employee class – in a real system this would be defined elsewhere
# ------------------------------------------------------------------
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# ------------------------------------------------------------------
# Global list of employees – in a real system this would be replaced by
# a database query or other data source.
# ------------------------------------------------------------------
ALL_EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Engineer", "Engineering", 95000.0, "alice@example.com"),
    Employee("Bob Jones", "Manager", "Engineering", 120000.0, "bob@example.com"),
    Employee("Carol Lee", "Analyst", "Finance", 70000.0, "carol@example.com"),
]

# ------------------------------------------------------------------
# Assemble employee list for a given department using the supplied template
# ------------------------------------------------------------------
def assemble_employee_list(dept_name: str, template: str) -> str:
    """
    Build a formatted employee directory for the specified department.

    Parameters
    ----------
    dept_name : str
        The department name to filter employees by.
    template : str
        A string containing placeholders of the form {employee.<field>}.

    Returns
    -------
    str
        The formatted employee directory, one entry per line.

    Raises
    ------
    ValueError
        If the template references a restricted field (salary or personal_email)
        or if an unexpected error occurs during processing.
    """
    # Allowed fields that can be exposed
    allowed_fields = {"name", "position", "department"}

    # Regular expression to find placeholders like {employee.name}
    placeholder_pattern = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

    # Find all unique fields referenced in the template
    referenced_fields = set(placeholder_pattern.findall(template))

    # Check for restricted fields
    restricted_fields = referenced_fields - allowed_fields
    if restricted_fields:
        raise ValueError(
            f"Template references restricted fields: {', '.join(sorted(restricted_fields))}"
        )

    # Filter employees by department
    filtered_employees = [
        emp for emp in ALL_EMPLOYEES if emp.department == dept_name
    ]

    # If no employees found, return an informative message
    if not filtered_employees:
        return f"No employees found in department '{dept_name}'."

    # Build the output lines
    output_lines = []
    for emp in filtered_employees:
        try:
            # Use re.sub with a function to replace each placeholder
            def repl(match):
                field_name = match.group(1)
                value = getattr(emp, field_name)
                return str(value)

            formatted_line = placeholder_pattern.sub(repl, template)
            output_lines.append(formatted_line)
        except Exception as exc:
            # Wrap any unexpected exception in a ValueError with context
            raise ValueError(
                f"Failed to format employee '{emp.name}': {exc}"
            ) from exc

    return "\n".join(output_lines)


# ------------------------------------------------------------------
# Example usage (uncomment to test)
# ------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = "Name: {employee.name}, Position: {employee.position}"
    print(assemble_employee_list("Engineering", tmpl))