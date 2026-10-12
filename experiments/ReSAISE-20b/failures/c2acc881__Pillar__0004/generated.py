import re
from dataclasses import dataclass, field
from typing import List

# ------------------------------------------------------------------
# Example Employee class. In a real system this would be imported.
# ------------------------------------------------------------------
@dataclass
class Employee:
    name: str
    position: str
    department: str
    salary: float = field(repr=False)          # sensitive
    personal_email: str = field(repr=False)   # sensitive

# ------------------------------------------------------------------
# Sample data set. In a real system this would come from a database.
# ------------------------------------------------------------------
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Engineer", "R&D", 95000.0, "alice.smith@company.com"),
    Employee("Bob Johnson", "Manager", "R&D", 120000.0, "bob.johnson@company.com"),
    Employee("Carol Lee", "Analyst", "Finance", 70000.0, "carol.lee@company.com"),
]

# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------
def compile_department_roster(division: str, template_str: str) -> str:
    """
    Build a formatted directory for all employees in `division` using
    the provided template string.

    Parameters
    ----------
    division : str
        The department name to filter employees by.
    template_str : str
        A string containing placeholders of the form `{employee.<attr>}`.

    Returns
    -------
    str
        The concatenated formatted directory entries, one per line.

    Raises
    ------
    ValueError
        If the template references a sensitive attribute (`salary`,
        `personal_email`) or if any error occurs during formatting.
    """
    # 1. Detect sensitive placeholders
    placeholder_pattern = re.compile(r"\{employee\.([^\}]+)\}")
    placeholders = set(placeholder_pattern.findall(template_str))

    sensitive_attrs = {"salary", "personal_email"}
    if placeholders & sensitive_attrs:
        raise ValueError(
            f"Template attempts to access sensitive attributes: "
            f"{sorted(placeholders & sensitive_attrs)}"
        )

    # 2. Filter employees by division
    dept_employees = [emp for emp in EMPLOYEES if emp.department == division]

    # 3. Format each employee entry
    formatted_entries = []
    for emp in dept_employees:
        try:
            # Using a simple namespace object to avoid exposing sensitive attrs
            class SafeNamespace:
                def __init__(self, employee: Employee):
                    self.name = employee.name
                    self.position = employee.position
                    self.department = employee.department

                # Prevent access to sensitive attributes
                def __getattr__(self, item):
                    raise AttributeError(f"Attribute '{item}' is not allowed")

            entry = template_str.format(employee=SafeNamespace(emp))
        except Exception as exc:
            raise ValueError(f"Error formatting employee '{emp.name}': {exc}") from exc
        formatted_entries.append(entry)

    # 4. Join entries with newlines
    return "\n".join(formatted_entries)

# ------------------------------------------------------------------
# Example usage (uncomment to test)
# ------------------------------------------------------------------
# if __name__ == "__main__":
#     tmpl = "Name: {employee.name}, Position: {employee.position}"
#     print(compile_department_roster("R&D", tmpl))