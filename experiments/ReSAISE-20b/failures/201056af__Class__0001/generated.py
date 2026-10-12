import re
from dataclasses import dataclass
from typing import List

# --------------------------------------------------------------------------- #
#   Employee model (simplified for this example)                              #
# --------------------------------------------------------------------------- #
@dataclass
class Employee:
    name: str
    position: str
    department: str
    salary: float          # Sensitive field – must not be exposed
    personal_email: str   # Sensitive field – must not be exposed

# --------------------------------------------------------------------------- #
#   Sample data (in a real application this would come from a database)      #
# --------------------------------------------------------------------------- #
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Engineer", "Engineering", 95000, "alice@company.com"),
    Employee("Bob Johnson", "Manager", "Engineering", 120000, "bob@company.com"),
    Employee("Carol Lee", "HR Specialist", "Human Resources", 70000, "carol@company.com"),
]

# --------------------------------------------------------------------------- #
#   Core function                                                             #
# --------------------------------------------------------------------------- #
def build_worker_list(team_name: str, list_template: str) -> str:
    """
    Build a formatted employee directory for the given department.

    Parameters
    ----------
    team_name : str
        The department name to filter employees by.
    list_template : str
        A string containing placeholders of the form {employee.<field>}.

    Returns
    -------
    str
        The directory formatted according to the template, one employee per line.

    Raises
    ------
    ValueError
        If a placeholder references a restricted field (salary or personal_email),
        or if any unexpected error occurs during processing.
    """
    # Define the set of disallowed fields
    DISALLOWED_FIELDS = {"salary", "personal_email"}

    # Regex to find placeholders of the form {employee.field}
    placeholder_pattern = re.compile(r"\{employee\.([^\}]+)\}")

    # Filter employees by department (case‑insensitive match)
    filtered = [emp for emp in EMPLOYEES if emp.department.lower() == team_name.lower()]
    if not filtered:
        return ""

    # Build the output lines
    result_lines = []
    for emp in filtered:
        try:
            # Find all placeholders in the template
            fields_in_template = placeholder_pattern.findall(list_template)

            # Check for disallowed fields
            if any(field in DISALLOWED_FIELDS for field in fields_in_template):
                raise ValueError(
                    f"Attempted to expose restricted field(s) in template: {fields_in_template}"
                )

            # Replace placeholders with actual attribute values
            line = list_template
            for field in fields_in_template:
                if not hasattr(emp, field):
                    raise ValueError(f"Unknown field '{field}' in template.")
                value = getattr(emp, field)
                line = line.replace(f"{{employee.{field}}}", str(value))

            result_lines.append(line)

        except Exception as exc:
            # Wrap any exception into ValueError to signal misuse
            raise ValueError(f"Failed to build worker list: {exc}") from exc

    return "\n".join(result_lines)

# --------------------------------------------------------------------------- #
#   Example usage (commented out – remove comments to run)                    #
# --------------------------------------------------------------------------- #
# if __name__ == "__main__":
#     template = "- {employee.name} ({employee.position})"
#     print(build_worker_list("Engineering", template))