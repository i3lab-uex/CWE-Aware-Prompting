import re
from typing import List

# ------------------------------------------------------------------
# Minimal Employee model for demonstration purposes.
# In a real application this would be replaced by the actual ORM/model class.
# ------------------------------------------------------------------
class Employee:
    _registry: List["Employee"] = []

    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email
        Employee._registry.append(self)

    @classmethod
    def get_all(cls) -> List["Employee"]:
        """Return all registered employees."""
        return cls._registry


# ------------------------------------------------------------------
# build_worker_list implementation
# ------------------------------------------------------------------
def build_worker_list(team_name: str, list_template: str) -> str:
    """
    Build a formatted employee directory for the specified department.

    Parameters
    ----------
    team_name : str
        The department name to filter employees by.
    list_template : str
        A string template containing placeholders like '{employee.name}'.

    Returns
    -------
    str
        The formatted directory string for the department.

    Raises
    ------
    ValueError
        If a restricted field is accessed or any unexpected error occurs.
    """
    # Fields that are not allowed to be exposed
    restricted_fields = {"salary", "personal_email"}

    # Regex to find placeholders of the form {employee.field}
    placeholder_pattern = re.compile(r"\{employee\.([^\}]+)\}")

    rendered_lines: List[str] = []

    for emp in Employee.get_all():
        if emp.department != team_name:
            continue

        def _replace_placeholder(match: re.Match) -> str:
            field = match.group(1)
            if field in restricted_fields:
                raise ValueError(
                    f"Access to restricted field '{field}' is not allowed."
                )
            if not hasattr(emp, field):
                raise ValueError(
                    f"Employee '{emp.name}' has no attribute '{field}'."
                )
            return str(getattr(emp, field))

        try:
            rendered = placeholder_pattern.sub(_replace_placeholder, list_template)
            rendered_lines.append(rendered)
        except Exception as exc:
            raise ValueError(
                f"Error processing employee '{emp.name}': {exc}"
            ) from exc

    return "\n".join(rendered_lines)


# ------------------------------------------------------------------
# Example usage (for testing purposes)
# ------------------------------------------------------------------
if __name__ == "__main__":
    # Create some sample employees
    Employee("Alice Smith", "Engineer", "Engineering", 90000, "alice@company.com")
    Employee("Bob Johnson", "Manager", "Engineering", 120000, "bob@company.com")
    Employee("Carol Lee", "Designer", "Design", 75000, "carol@company.com")

    template = (
        "Name: {employee.name}\n"
        "Position: {employee.position}\n"
        "Department: {employee.department}\n"
    )

    print(build_worker_list("Engineering", template))