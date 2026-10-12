import re
from typing import Any

# Assume these classes exist in the system.  We only need to reference them here.
class Employee:
    """Placeholder for the real Employee class."""
    def __init__(self, emp_id: str, name: str, position: str, department: str):
        self.emp_id = emp_id
        self.name = name
        self.position = position
        self.department = department
    @staticmethod
    def get_by_id(emp_id: str) -> 'Employee':
        """Retrieve an Employee instance by ID.  Replace with actual lookup."""
        # Example stub – replace with real data access logic.
        if emp_id == "E001":
            return Employee(emp_id, "Alice Smith", "Software Engineer", "Engineering")
        raise KeyError(f"Employee {emp_id} not found")

class Performance:
    """Placeholder for the real Performance class."""
    def __init__(self, rating: str):
        self.rating = rating
    @staticmethod
    def get_by_employee(emp: Employee) -> 'Performance':
        """Retrieve a Performance instance for an employee.  Replace with actual lookup."""
        # Example stub – replace with real data access logic.
        return Performance("Excellent")

# Proxy objects that expose only allowed attributes
class RestrictedAttrProxy:
    def __init__(self, obj: Any, allowed_attrs: set[str], context_name: str):
        self._obj = obj
        self._allowed_attrs = allowed_attrs
        self._context_name = context_name

    def __getattr__(self, name: str) -> Any:
        if name in self._allowed_attrs:
            return getattr(self._obj, name)
        raise ValueError(
            f"Access to restricted field '{self._context_name}.{name}' is not allowed"
        )

# Main function
def create_performance_summary(emp_id: str, summary_template: str) -> str:
    """
    Generate a performance summary for the given employee ID using the provided template.

    Parameters
    ----------
    emp_id : str
        The unique identifier of the employee.
    summary_template : str
        A template string containing placeholders like '{employee.name}', 
        '{performance.rating}', etc.

    Returns
    -------
    str
        The formatted performance summary string.

    Raises
    ------
    ValueError
        If the employee ID is invalid, if restricted fields are accessed,
        or if placeholders reference undefined attributes.
    """
    # 1. Retrieve employee and performance data
    try:
        emp = Employee.get_by_id(emp_id)
    except KeyError as exc:
        raise ValueError(f"Invalid employee ID: {emp_id}") from exc

    perf = Performance.get_by_employee(emp)

    # 2. Define allowed attributes for each context
    employee_allowed = {"name", "position", "department"}
    performance_allowed = {"rating"}

    # 3. Wrap objects in proxies that enforce attribute restrictions
    emp_proxy = RestrictedAttrProxy(emp, employee_allowed, "employee")
    perf_proxy = RestrictedAttrProxy(perf, performance_allowed, "performance")

    # 4. Validate template placeholders to catch accidental use of disallowed fields
    placeholder_pattern = re.compile(r"\{([^}]+)\}")
    for match in placeholder_pattern.finditer(summary_template):
        full_path = match.group(1).strip()
        # Split into context and attribute
        if "." not in full_path:
            raise ValueError(f"Invalid placeholder '{full_path}': missing context")
        ctx, attr = full_path.split(".", 1)
        if ctx == "employee" and attr not in employee_allowed:
            raise ValueError(f"Access to restricted field 'employee.{attr}' is not allowed")
        if ctx == "performance" and attr not in performance_allowed:
            raise ValueError(f"Access to restricted field 'performance.{attr}' is not allowed")
        if ctx not in {"employee", "performance"}:
            raise ValueError(f"Unknown context '{ctx}' in placeholder")

    # 5. Perform formatting
    try:
        formatted = summary_template.format(employee=emp_proxy, performance=perf_proxy)
    except KeyError as exc:
        raise ValueError(f"Template references unknown attribute: {exc}") from exc
    except AttributeError as exc:
        # This can happen if a proxy raises an AttributeError for disallowed access
        raise ValueError(f"Template references restricted or missing attribute: {exc}") from exc

    return formatted