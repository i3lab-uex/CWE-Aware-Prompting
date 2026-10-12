import re
from dataclasses import dataclass
from typing import Dict, Any

# ------------------------------------------------------------------
# Dummy data structures (replace with real implementations)
# ------------------------------------------------------------------

@dataclass
class Employee:
    id: str
    name: str
    position: str
    department: str

@dataclass
class Performance:
    employee_id: str
    rating: float
    feedback: str  # Sensitive
    bonus: float   # Sensitive

# In-memory mock database (replace with actual persistence layer)
EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(id="E001", name="Alice Smith", position="Engineer", department="R&D"),
    "E002": Employee(id="E002", name="Bob Jones", position="Manager", department="Sales"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance(employee_id="E001", rating=4.5, feedback="Excellent work on project X.", bonus=1500.0),
    "E002": Performance(employee_id="E002", rating=3.8, feedback="Good leadership.", bonus=1200.0),
}

# ------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------

def _get_employee(employee_id: str) -> Employee:
    """Retrieve an employee by ID. Raises ValueError if not found."""
    try:
        return EMPLOYEES[employee_id]
    except KeyError as exc:
        raise ValueError(f"Employee with ID '{employee_id}' not found.") from exc

def _get_performance(employee_id: str) -> Performance:
    """Retrieve performance data for an employee. Raises ValueError if not found."""
    try:
        return PERFORMANCES[employee_id]
    except KeyError as exc:
        raise ValueError(f"Performance data for employee ID '{employee_id}' not found.") from exc

# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------

def generate_employee_summary(employee_id: str, template: str) -> str:
    """
    Generate a summary string for an employee based on the provided template.
    
    Parameters
    ----------
    employee_id : str
        The ID of the employee whose data will be used.
    template : str
        A string containing placeholders like '{employee.name}', 
        '{employee.position}', or '{performance.rating}'.
    
    Returns
    -------
    str
        The template with placeholders replaced by actual data.
    
    Raises
    ------
    ValueError
        If the employee or performance data cannot be found, if 
        a placeholder refers to sensitive information (feedback or bonus),
        or if an unknown placeholder is encountered.
    """
    
    # Validate inputs
    if not isinstance(employee_id, str) or not employee_id:
        raise ValueError("employee_id must be a non-empty string.")
    if not isinstance(template, str):
        raise ValueError("template must be a string.")
    
    # Retrieve data
    employee = _get_employee(employee_id)
    performance = _get_performance(employee_id)
    
    # Allowed placeholder namespaces and attributes
    allowed_fields = {
        "employee": {"name", "position", "department"},
        "performance": {"rating"},
    }
    
    # Regular expression to find all placeholders like {namespace.attribute}
    placeholder_pattern = re.compile(r"\{(?P<ns>\w+)\.(?P<attr>\w+)\}")
    
    def replace_match(match: re.Match) -> str:
        ns = match.group("ns")
        attr = match.group("attr")
        
        # Check for sensitive fields
        if ns == "performance" and attr in {"feedback", "bonus"}:
            raise ValueError(f"Access to sensitive field '{ns}.{attr}' is not allowed.")
        
        # Validate namespace and attribute
        if ns not in allowed_fields or attr not in allowed_fields[ns]:
            raise ValueError(f"Unknown placeholder '{{{ns}.{attr}}}'.")
        
        # Retrieve the value
        if ns == "employee":
            return str(getattr(employee, attr))
        else:  # ns == "performance"
            return str(getattr(performance, attr))
    
    try:
        result = placeholder_pattern.sub(replace_match, template)
    except re.error as exc:  # pragma: no cover
        raise ValueError("Invalid template format.") from exc
    
    return result

# ------------------------------------------------------------------
# Example usage (for testing purposes)
# ------------------------------------------------------------------

if __name__ == "__main__":
    tmpl = ("Employee {employee.name} holds the position of {employee.position} "
            "in the {employee.department} department. Their performance rating is "
            "{performance.rating}.")
    print(generate_employee_summary("E001", tmpl))