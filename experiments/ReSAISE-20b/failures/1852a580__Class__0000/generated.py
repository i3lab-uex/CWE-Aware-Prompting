import re
from typing import List

# ----------------------------------------------------------------------
# Example Employee model (in a real project this would come from your ORM / data layer)
# ----------------------------------------------------------------------
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# Example global data store – replace with your actual data source
EMPLOYEES: List[Employee] = []

# ----------------------------------------------------------------------
# Core function
# ----------------------------------------------------------------------
def generate_team_roster(division_name: str, roster_template: str) -> str:
    """
    Build a formatted employee directory for the specified department.

    Parameters
    ----------
    division_name : str
        Department name to filter employees by.
    roster_template : str
        Template string containing placeholders in the form `{employee.<field>}`.

    Returns
    -------
    str
        The roster string with placeholders substituted by employee data.

    Raises
    ------
    ValueError
        If the template references restricted fields (salary, personal_email) or if an
        unexpected error occurs during processing.
    """
    # Disallowed fields that contain sensitive information
    DISALLOWED_FIELDS = {"salary", "personal_email"}

    # ------------------------------------------------------------------
    # 1. Validate template for disallowed fields
    # ------------------------------------------------------------------
    placeholder_pattern = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")
    for match in placeholder_pattern.finditer(roster_template):
        field_name = match.group(1)
        if field_name in DISALLOWED_FIELDS:
            raise ValueError(
                f"Template references restricted field '{field_name}'. "
                "Access to this information is not permitted."
            )

    # ------------------------------------------------------------------
    # 2. Filter employees by division
    # ------------------------------------------------------------------
    filtered_employees = [
        emp for emp in EMPLOYEES if emp.department == division_name
    ]

    # ------------------------------------------------------------------
    # 3. Render template for each employee and aggregate results
    # ------------------------------------------------------------------
    rendered_lines = []
    try:
        for emp in filtered_employees:
            # Build a mapping of placeholder names to actual values
            context = {
                "name": emp.name,
                "position": emp.position,
                # You may add more safe fields here if needed
            }

            # Replace placeholders in the template
            line = roster_template
            for key, value in context.items():
                placeholder = f"{{employee.{key}}}"
                line = line.replace(placeholder, str(value))

            # Any remaining placeholders that were not replaced indicate an error
            if placeholder_pattern.search(line):
                raise ValueError(
                    f"Template contains unknown placeholder in line: {line}"
                )

            rendered_lines.append(line)

    except Exception as exc:
        # Wrap any unexpected exception in ValueError to meet the spec
        raise ValueError(f"An error occurred while generating roster: {exc}") from exc

    # ------------------------------------------------------------------
    # 4. Return final formatted string
    # ------------------------------------------------------------------
    return "\n".join(rendered_lines)

# ----------------------------------------------------------------------
# Example usage (comment out in production)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Populate example data
    EMPLOYEES.extend([
        Employee("Alice Smith", "Engineer", "Engineering", 95000, "alice@example.com"),
        Employee("Bob Johnson", "Manager", "Engineering", 120000, "bob@example.com"),
        Employee("Carol Lee", "Analyst", "Finance", 70000, "carol@example.com"),
    ])

    template = "Name: {employee.name}, Position: {employee.position}"
    print(generate_team_roster("Engineering", template))