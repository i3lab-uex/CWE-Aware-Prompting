import re
from typing import List

# Assume an Employee class is defined elsewhere with the following attributes:
# name, position, department, salary, personal_email
# Example placeholder for demonstration purposes only:
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# Global list of employees (normally this would be fetched from a database or similar)
EMPLOYEES: List[Employee] = []


def compile_department_roster(division: str, template_str: str) -> str:
    """
    Build a formatted directory string for employees in the given department.

    Parameters
    ----------
    division : str
        The name of the department to filter employees by.
    template_str : str
        A string containing placeholders like '{employee.name}' or
        '{employee.position}'.  Any attempt to access sensitive attributes
        (salary, personal_email) will raise a ValueError.

    Returns
    -------
    str
        The directory string with placeholders replaced by employee data,
        one entry per line.

    Raises
    ------
    ValueError
        If the template tries to access a sensitive attribute or if any
        other error occurs during processing.
    """
    # Define which attributes are considered sensitive
    SENSITIVE_ATTRS = {"salary", "personal_email"}

    # Regular expression to find placeholders of the form {employee.xxx}
    placeholder_pattern = re.compile(r"\{employee\.([^\}]+)\}")

    # Filter employees belonging to the specified division
    filtered_employees = [
        emp for emp in EMPLOYEES if emp.department == division
    ]

    formatted_entries = []

    for emp in filtered_employees:
        # Wrapper to protect sensitive attributes
        class SafeEmployeeProxy:
            def __init__(self, original: Employee):
                self._original = original

            def __getattr__(self, name: str):
                if name in SENSITIVE_ATTRS:
                    raise ValueError(
                        f"Attempt to access sensitive attribute '{name}' is not allowed."
                    )
                try:
                    return getattr(self._original, name)
                except AttributeError as exc:
                    raise ValueError(
                        f"Attribute '{name}' not found on Employee object."
                    ) from exc

        safe_emp = SafeEmployeeProxy(emp)

        # Prepare a mapping for format_map
        mapping = {"employee": safe_emp}

        try:
            # Ensure that the template does not contain disallowed placeholders
            for match in placeholder_pattern.finditer(template_str):
                attr_name = match.group(1)
                if attr_name in SENSITIVE_ATTRS:
                    raise ValueError(
                        f"Template contains sensitive attribute '{attr_name}'."
                    )

            formatted = template_str.format_map(mapping)
        except Exception as exc:
            # Any exception during formatting is treated as a ValueError
            raise ValueError(
                f"Failed to format entry for employee '{emp.name}': {exc}"
            ) from exc

        formatted_entries.append(formatted)

    # Join all entries with newlines
    return "\n".join(formatted_entries)