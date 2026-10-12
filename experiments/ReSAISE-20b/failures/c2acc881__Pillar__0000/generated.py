import re
from typing import List

# --------------------------------------------------------------------
# Sample Employee class – in a real system this would be imported
# from the application's domain model.
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# --------------------------------------------------------------------
# Global list of employees – in a real system this would come from
# a database or an external data source.
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Senior Engineer", "Engineering",
             120000.0, "alice.smith@company.com"),
    Employee("Bob Johnson", "HR Manager", "Human Resources",
             90000.0, "bob.johnson@company.com"),
    Employee("Carol Williams", "CTO", "Engineering",
             250000.0, "carol.williams@company.com"),
]

# --------------------------------------------------------------------
class _RestrictedEmployee:
    """
    Wraps an Employee instance and exposes only non‑sensitive attributes.
    Attempting to access a sensitive attribute raises ValueError.
    """
    _SENSITIVE = {"salary", "personal_email"}

    def __init__(self, employee: Employee):
        self._employee = employee

    def __getattr__(self, name: str):
        if name in self._SENSITIVE:
            raise ValueError(f"Access to sensitive attribute '{name}' is forbidden.")
        if hasattr(self._employee, name):
            return getattr(self._employee, name)
        raise AttributeError(f"'Employee' object has no attribute '{name}'")

    def __repr__(self):
        return f"<RestrictedEmployee name={self._employee.name}>"

# --------------------------------------------------------------------
def compile_department_roster(division: str, template_str: str) -> str:
    """
    Build a formatted employee directory for the given department.

    Parameters
    ----------
    division : str
        Department name used to filter employees.
    template_str : str
        A string containing placeholders like '{employee.name}' or
        '{employee.position}'.  The function substitutes these with the
        corresponding attributes of each employee in the department.

    Returns
    -------
    str
        A newline‑separated string of formatted employee records.

    Raises
    ------
    ValueError
        If the template tries to access a sensitive attribute (salary or
        personal_email) or if any other exception occurs during formatting.
    """
    try:
        # Filter employees by department
        dept_employees = [
            _RestrictedEmployee(emp) for emp in EMPLOYEES if emp.department == division
        ]

        # No employees – return empty string (no error)
        if not dept_employees:
            return ""

        # Compile the result
        formatted_lines = []
        for emp_ctx in dept_employees:
            # We want placeholders like {employee.name}.  The
            # format string may contain arbitrary braces; we replace
            # 'employee' with the context object for formatting.
            mapping = {"employee": emp_ctx}
            formatted_lines.append(template_str.format_map(mapping))

        return "\n".join(formatted_lines)

    except KeyError as exc:
        # Raised when a placeholder refers to an unknown key
        raise ValueError(f"Unknown placeholder in template: {exc}") from exc

    except AttributeError as exc:
        # Raised when the employee object lacks an attribute
        raise ValueError(f"Invalid placeholder in template: {exc}") from exc

    except Exception as exc:
        # Catch-all for unexpected errors
        raise ValueError(f"An error occurred while compiling the roster: {exc}") from exc

# --------------------------------------------------------------------
# Example usage (commented out – remove comments to test)
#
# if __name__ == "__main__":
#     tmpl = "Name: {employee.name}, Position: {employee.position}"
#     print(compile_department_roster("Engineering", tmpl))