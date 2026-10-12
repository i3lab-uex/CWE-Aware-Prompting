import re
from typing import Dict

# --------------------------------------------------------------------
# Mock data layer (replace with real implementations in production)
# --------------------------------------------------------------------

class Employee:
    """
    Represents an employee. In a real system this would be loaded from
    a database or external service.
    """
    _employees: Dict[str, "Employee"] = {}

    def __init__(self,
                 employee_id: str,
                 name: str,
                 position: str,
                 department: str):
        self.employee_id = employee_id
        self.name = name
        self.position = position
        self.department = department

    @classmethod
    def register(cls, employee: "Employee") -> None:
        cls._employees[employee.employee_id] = employee

    @classmethod
    def get_by_id(cls, employee_id: str) -> "Employee":
        try:
            return cls._employees[employee_id]
        except KeyError as exc:
            raise ValueError(f"Employee ID '{employee_id}' not found") from exc


class Performance:
    """
    Represents performance data for an employee. In a real system this
    would be loaded from a database or external service.
    """
    _performances: Dict[str, "Performance"] = {}

    def __init__(self,
                 employee_id: str,
                 rating: float,
                 feedback: str,
                 bonus: float):
        self.employee_id = employee_id
        self.rating = rating
        self.feedback = feedback
        self.bonus = bonus

    @classmethod
    def register(cls, performance: "Performance") -> None:
        cls._performances[performance.employee_id] = performance

    @classmethod
    def get_by_employee_id(cls, employee_id: str) -> "Performance":
        try:
            return cls._performances[employee_id]
        except KeyError as exc:
            raise ValueError(f"Performance data for employee ID '{employee_id}' not found") from exc


# --------------------------------------------------------------------
# Core function
# --------------------------------------------------------------------

_RE_PLACEHOLDER = re.compile(r"\{([a-zA-Z_][a-zA-Z0-9_.]*)\}")

# Fields that are explicitly forbidden from being exposed in the report
_FORBIDDEN_FIELDS = {"feedback", "bonus"}

def construct_employee_report(employee_id: str, report_template: str) -> str:
    """
    Construct a performance summary for the given employee.

    Parameters
    ----------
    employee_id : str
        The unique identifier of the employee.
    report_template : str
        Template containing placeholders like '{employee.name}' or
        '{performance.rating}'.  Placeholders may reference any attribute of
        the Employee or Performance objects, except those in
        :data:`_FORBIDDEN_FIELDS`.

    Returns
    -------
    str
        The fully formatted performance summary.

    Raises
    ------
    ValueError
        If the employee ID does not exist, if a placeholder refers to a
        forbidden field, or if a placeholder references an unknown attribute.
    """
    # --------------------------------------------------------------------
    # Retrieve data objects (resource acquisition)
    # --------------------------------------------------------------------
    employee = Employee.get_by_id(employee_id)
    performance = Performance.get_by_employee_id(employee_id)

    # --------------------------------------------------------------------
    # Build a namespace for safe formatting
    # --------------------------------------------------------------------
    namespace = {
        "employee": employee,
        "performance": performance
    }

    # --------------------------------------------------------------------
    # Validate and replace placeholders
    # --------------------------------------------------------------------
    def _replacement(match: re.Match) -> str:
        full_path = match.group(1).split(".")
        if not full_path:
            raise ValueError("Empty placeholder detected")

        # Detect forbidden fields early
        if full_path[0] == "performance" and full_path[1] in _FORBIDDEN_FIELDS:
            raise ValueError(f"Access to restricted field '{full_path[1]}' is prohibited")

        # Resolve the attribute chain
        obj = namespace.get(full_path[0])
        if obj is None:
            raise ValueError(f"Unknown placeholder prefix '{full_path[0]}'")

        for attr in full_path[1:]:
            try:
                obj = getattr(obj, attr)
            except AttributeError as exc:
                raise ValueError(
                    f"Attribute '{attr}' not found on object of type "
                    f"'{type(obj).__name__}'"
                ) from exc

        # Convert the final value to string
        return str(obj)

    try:
        formatted_report = _RE_PLACEHOLDER.sub(_replacement, report_template)
    except re.error as exc:
        raise ValueError("Invalid template syntax") from exc

    # --------------------------------------------------------------------
    # Return the final report (resource release is implicit in Python)
    # --------------------------------------------------------------------
    return formatted_report


# --------------------------------------------------------------------
# Example usage (for testing; remove or comment out in production)
# --------------------------------------------------------------------

if __name__ == "__main__":
    # Register some mock data
    emp = Employee("E123", "Alice Smith", "Senior Engineer", "R&D")
    perf = Performance("E123", 4.7, "Excellent teamwork and leadership.", 12000)

    Employee.register(emp)
    Performance.register(perf)

    template = (
        "Employee Report for {employee.name} ({employee.position})\n"
        "Department: {employee.department}\n"
        "Performance Rating: {performance.rating}/5.0\n"
    )

    print(construct_employee_report("E123", template))