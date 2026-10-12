import re
from typing import List

# --------------------------------------------------------------------
# Example Employee class (in real usage this would be provided elsewhere)
# --------------------------------------------------------------------
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# --------------------------------------------------------------------
# Global list of employees – in a real system this would come from a DB
# --------------------------------------------------------------------
EMPLOYEES: List[Employee] = []

# --------------------------------------------------------------------
# Main function
# --------------------------------------------------------------------
def build_team_directory(team: str, template_text: str) -> str:
    """
    Build a formatted employee directory for the given department.

    Parameters
    ----------
    team : str
        The name of the department to filter employees by.
    template_text : str
        A string containing placeholders such as `{employee.name}` or
        `{employee.position}` to be replaced with employee data.

    Returns
    -------
    str
        The formatted directory string containing one line per employee in the
        selected department.

    Raises
    ------
    ValueError
        If a sensitive field (salary or personal_email) is referenced in the
        template, or if any other error occurs during processing.
    """
    try:
        # 1. Detect usage of sensitive fields early
        if re.search(r'\{employee\.(salary|personal_email)\}', template_text):
            raise ValueError("Template references a sensitive employee attribute")

        # 2. Compile regex to find all placeholders of the form {employee.<attr>}
        placeholder_pattern = re.compile(r'\{employee\.([^\}]+)\}')

        lines: List[str] = []

        for emp in EMPLOYEES:
            if emp.department != team:
                continue

            # Replace placeholders with actual employee attribute values
            def replace_placeholder(match: re.Match) -> str:
                attr_name = match.group(1)
                if not hasattr(emp, attr_name):
                    raise ValueError(f"Unknown attribute '{attr_name}' for employee")
                value = getattr(emp, attr_name)
                return str(value)

            formatted_line = placeholder_pattern.sub(replace_placeholder, template_text)
            lines.append(formatted_line)

        return "\n".join(lines)

    except Exception as exc:
        # Wrap any exception in ValueError to conform with the contract
        raise ValueError(f"Failed to build directory: {exc}") from exc

# --------------------------------------------------------------------
# Example usage (this section would normally be omitted or moved to tests)
# --------------------------------------------------------------------
if __name__ == "__main__":
    # Populate some sample data
    EMPLOYEES.extend([
        Employee("Alice Smith", "Engineer", "R&D", 95000, "alice@company.com"),
        Employee("Bob Johnson", "Manager", "R&D", 120000, "bob@company.com"),
        Employee("Carol Lee", "Designer", "Marketing", 70000, "carol@company.com"),
    ])

    tmpl = "{employee.name} - {employee.position}"
    print(build_team_directory("R&D", tmpl))