import re
from typing import Dict

# ----------------------------------------------------------------------
# Dummy data classes (replace with the real implementations)
# ----------------------------------------------------------------------
class Employee:
    def __init__(self, key: str, name: str, position: str, department: str):
        self.key = key
        self.name = name
        self.position = position
        self.department = department

    @staticmethod
    def get_by_id(emp_key: str) -> "Employee":
        # In a real system this would query a database
        fake_db = {
            "E001": Employee("E001", "Alice Smith", "Senior Engineer", "R&D"),
            "E002": Employee("E002", "Bob Johnson", "Product Manager", "Product"),
        }
        try:
            return fake_db[emp_key]
        except KeyError as exc:
            raise ValueError(f"Employee with key '{emp_key}' not found") from exc


class Performance:
    def __init__(self, employee: Employee, rating: str):
        self.employee = employee
        self.rating = rating

    @staticmethod
    def get_by_employee(employee: Employee) -> "Performance":
        # In a real system this would query a database
        fake_perf = {
            "E001": Performance(employee, "Excellent"),
            "E002": Performance(employee, "Meets Expectations"),
        }
        key = employee.key
        try:
            return fake_perf[key]
        except KeyError as exc:
            raise ValueError(f"Performance data for employee '{key}' not found") from exc


# ----------------------------------------------------------------------
# Utility classes
# ----------------------------------------------------------------------
class SafeDict(dict):
    """
    A dict that raises KeyError for missing keys.
    This prevents the use of default values during formatting,
    ensuring that all placeholders are explicitly provided.
    """
    def __missing__(self, key):
        raise KeyError(key)


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def build_employee_summary(emp_key: str, template_str: str) -> str:
    """
    Builds a formatted employee performance summary.

    Args:
        emp_key: Identifier of the employee.
        template_str: String containing placeholders such as
            '{employee.name}', '{performance.rating}'.

    Returns:
        A string with placeholders replaced by actual data.

    Raises:
        ValueError: If the employee or performance record is missing,
                    if a restricted field is requested, or
                    if an invalid placeholder is used.
    """
    # 1. Retrieve data objects
    employee = Employee.get_by_id(emp_key)
    performance = Performance.get_by_employee(employee)

    # 2. Define allowed placeholder patterns
    allowed_patterns = {
        "employee.name",
        "employee.position",
        "employee.department",
        "performance.rating",
    }
    restricted_patterns = {"feedback", "bonus"}

    # 3. Find all placeholders in the template
    placeholder_regex = re.compile(r"\{([^\}]+)\}")
    placeholders = placeholder_regex.findall(template_str)

    # 4. Validate each placeholder
    for ph in placeholders:
        if any(restricted in ph for restricted in restricted_patterns):
            raise ValueError(f"Access to restricted field '{ph}' is not allowed.")
        if ph not in allowed_patterns:
            raise ValueError(f"Invalid placeholder '{ph}' in template.")

    # 5. Build a mapping for formatting
    context: Dict[str, str] = {
        "employee.name": employee.name,
        "employee.position": employee.position,
        "employee.department": employee.department,
        "performance.rating": performance.rating,
    }

    # 6. Perform safe formatting
    try:
        formatted = placeholder_regex.sub(lambda m: context[m.group(1)], template_str)
    except KeyError as exc:
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return formatted