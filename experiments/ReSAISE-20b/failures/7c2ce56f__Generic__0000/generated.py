import re
from typing import List

# Assume the Employee class is defined elsewhere and imported here.
# from employee_module import Employee

class Employee:
    """
    Dummy Employee class for demonstration purposes.
    Replace this with the actual implementation from your project.
    """
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email


def _is_sensitive_placeholder(placeholder: str) -> bool:
    """
    Detect if the placeholder references a sensitive attribute.
    """
    return placeholder in {"salary", "personal_email"}


def build_team_directory(team: str, template_text: str) -> str:
    """
    Generate a formatted directory string for employees belonging to the
    specified department.

    Parameters:
        team (str): The department name used for filtering employees.
        template_text (str): A format string containing placeholders
            such as '{employee.name}', '{employee.position}', etc.

    Returns:
        str: The directory string with placeholders replaced by actual
            employee data.

    Raises:
        ValueError: If the template attempts to access sensitive fields,
                    or if any other error occurs during formatting.
    """
    # Gather all employees. In a real implementation this would query a
    # database or data source; here we simply use a placeholder list.
    all_employees: List[Employee] = []  # Replace with actual data retrieval

    # Filter employees by department
    filtered_employees = [emp for emp in all_employees if emp.department == team]

    # Prepare the final directory lines
    directory_lines = []

    # Compile a regex to find placeholders like {employee.attr}
    placeholder_pattern = re.compile(r"\{([^{}]+)\}")

    for emp in filtered_employees:
        # Detect any sensitive placeholders before formatting
        placeholders = placeholder_pattern.findall(template_text)
        for ph in placeholders:
            # Only consider attributes of the employee object
            if ph.startswith("employee."):
                attr = ph.split(".", 1)[1]
                if _is_sensitive_placeholder(attr):
                    raise ValueError(
                        f"Access to sensitive attribute '{attr}' is prohibited."
                    )

        # Construct a safe mapping for formatting
        safe_attrs = {
            "name": getattr(emp, "name", ""),
            "position": getattr(emp, "position", ""),
            "department": getattr(emp, "department", ""),
        }
        # Use a simple namespace object to allow attribute access
        class Namespace:
            def __init__(self, attrs):
                self.__dict__.update(attrs)

        ns = Namespace(safe_attrs)

        try:
            formatted_line = template_text.format(employee=ns)
        except Exception as exc:
            raise ValueError(f"Error formatting template: {exc}") from exc

        directory_lines.append(formatted_line)

    return "\n".join(directory_lines)