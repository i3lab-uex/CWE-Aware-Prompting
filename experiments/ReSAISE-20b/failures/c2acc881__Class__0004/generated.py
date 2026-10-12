import sys
from typing import List

# The real Employee class is assumed to be defined elsewhere.
# For the sake of completeness, we provide a minimal stub here
# that can be replaced by the actual implementation.
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float = 0.0, personal_email: str = ""):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# Mock data store – replace with real data source in production
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Engineer", "Engineering", 90000, "alice@example.com"),
    Employee("Bob Johnson", "Manager", "Engineering", 120000, "bob@example.com"),
    Employee("Carol Williams", "Analyst", "Finance", 70000, "carol@example.com"),
]


class _SafeEmployeeProxy:
    """
    A proxy that exposes only non‑sensitive attributes of an Employee.
    Attempts to access sensitive data raise a ValueError.
    """
    _sensitive_attrs = {"salary", "personal_email"}

    def __init__(self, employee: Employee):
        self._employee = employee

    def __getattr__(self, item):
        if item in self._sensitive_attrs:
            raise ValueError(f"Access to sensitive attribute '{item}' is forbidden.")
        try:
            return getattr(self._employee, item)
        except AttributeError as exc:
            raise ValueError(f"Attribute '{item}' does not exist.") from exc


def compile_department_roster(division: str, template_str: str) -> str:
    """
    Generate a formatted employee directory for the specified department.

    Parameters
    ----------
    division : str
        The name of the department to filter employees by.
    template_str : str
        A format string containing placeholders such as '{employee.name}'.

    Returns
    -------
    str
        The concatenated formatted strings for all employees in the department.

    Raises
    ------
    ValueError
        If a template attempts to access sensitive attributes or any other error occurs.
    """
    try:
        # Filter employees belonging to the requested division
        relevant = [emp for emp in EMPLOYEES if emp.department == division]
        if not relevant:
            return ""

        rendered_lines = []
        for employee in relevant:
            proxy = _SafeEmployeeProxy(employee)
            # Using format with keyword argument 'employee'
            rendered_lines.append(template_str.format(employee=proxy))

        return "\n".join(rendered_lines)

    except Exception as exc:
        # Wrap any exception into a ValueError to signal failure
        raise ValueError("Failed to compile department roster.") from exc


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    tmpl = "Name: {employee.name}, Position: {employee.position}"
    try:
        print(compile_department_roster("Engineering", tmpl))
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)