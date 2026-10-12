import re
from typing import List

# --------------------------------------------------------------------
# Dummy data model – in a real application this would come from your
# database or another data source.
# --------------------------------------------------------------------
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# Example employee list – replace with real data in production.
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Software Engineer", "Engineering",
             95000.0, "alice.smith@example.com"),
    Employee("Bob Johnson", "Product Manager", "Engineering",
             105000.0, "bob.johnson@example.com"),
    Employee("Carol Lee", "HR Specialist", "Human Resources",
             75000.0, "carol.lee@example.com"),
]


# --------------------------------------------------------------------
# Core function
# --------------------------------------------------------------------
def build_worker_list(team_name: str, list_template: str) -> str:
    """
    Build a formatted employee directory for the specified department.

    Parameters
    ----------
    team_name : str
        The name of the department to filter employees by.
    list_template : str
        A string containing placeholders in the form '{employee.<field>}'.

    Returns
    -------
    str
        The formatted directory string. Each employee occupies one line,
        with placeholders replaced by actual values.

    Raises
    ------
    ValueError
        If the template contains disallowed fields (salary or personal_email)
        or if any unexpected error occurs during processing.
    """
    # ----------------------------------------------------------------
    # 1. Find all placeholders in the template.
    # ----------------------------------------------------------------
    placeholder_pattern = re.compile(r"\{([^}]+)\}")
    placeholders = set(placeholder_pattern.findall(list_template))

    # ----------------------------------------------------------------
    # 2. Validate that only allowed fields are referenced.
    # ----------------------------------------------------------------
    disallowed_fields = {"employee.salary", "employee.personal_email"}
    if placeholders & disallowed_fields:
        raise ValueError(
            f"Template contains restricted fields: {', '.join(placeholders & disallowed_fields)}"
        )

    # ----------------------------------------------------------------
    # 3. Filter employees by department.
    # ----------------------------------------------------------------
    filtered_employees = [
        emp for emp in EMPLOYEES if emp.department.lower() == team_name.lower()
    ]

    # ----------------------------------------------------------------
    # 4. Replace placeholders for each employee.
    # ----------------------------------------------------------------
    output_lines = []
    for emp in filtered_employees:
        line = list_template

        # Replace each placeholder with the corresponding attribute.
        for ph in placeholders:
            if not ph.startswith("employee."):
                raise ValueError(f"Unsupported placeholder format: {{{ph}}}")

            attr_name = ph.split(".", 1)[1]
            if not hasattr(emp, attr_name):
                raise ValueError(f"Unknown attribute '{attr_name}' in placeholder {{{ph}}}")

            # Convert the value to string; ensure no sensitive data leaks.
            try:
                replacement = str(getattr(emp, attr_name))
            except Exception as exc:  # pragma: no cover
                raise ValueError(f"Failed to retrieve value for {{{ph}}}") from exc

            line = line.replace("{" + ph + "}", replacement)

        output_lines.append(line)

    # ----------------------------------------------------------------
    # 5. Join lines into the final string.
    # ----------------------------------------------------------------
    return "\n".join(output_lines)


# --------------------------------------------------------------------
# Example usage (for manual testing only – remove or guard in production).
# --------------------------------------------------------------------
if __name__ == "__main__":
    template = "{employee.name} - {employee.position}"
    try:
        print(build_worker_list("Engineering", template))
    except ValueError as e:
        print(f"Error: {e}")