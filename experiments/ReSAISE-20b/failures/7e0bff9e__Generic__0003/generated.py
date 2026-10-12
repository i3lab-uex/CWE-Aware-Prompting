import string

# --------------------------------------------------------------------------- #
#   Domain classes (simplified for this example)
# --------------------------------------------------------------------------- #

class Employee:
    """Represents an employee record."""
    def __init__(self, code: str, name: str, position: str, department: str):
        self.code = code
        self.name = name
        self.position = position
        self.department = department


class Performance:
    """Represents a performance record."""
    def __init__(self, employee_code: str, rating: float,
                 feedback: str = None, bonus: float = None):
        self.employee_code = employee_code
        self.rating = rating
        self.feedback = feedback      # *restricted*
        self.bonus = bonus            # *restricted*


# --------------------------------------------------------------------------- #
#   In‑memory data store (replace with DB calls in production)
# --------------------------------------------------------------------------- #

EMPLOYEES = {
    "E001": Employee("E001", "Alice Smith", "Senior Engineer", "R&D"),
    "E002": Employee("E002", "Bob Johnson", "Project Manager", "Operations"),
}

PERFORMANCES = {
    "E001": Performance("E001", 4.5, feedback="Excellent teamwork.", bonus=1200),
    "E002": Performance("E002", 3.8, feedback="Needs improvement on deadlines.", bonus=800),
}


# --------------------------------------------------------------------------- #
#   Helper utilities
# --------------------------------------------------------------------------- #

def _resolve_placeholder(obj, attr_path: str):
    """
    Resolve a dotted attribute path on an object.
    Raises ValueError if the attribute does not exist or is restricted.
    """
    # Restricted attributes
    restricted = {"feedback", "bonus"}
    for attr in attr_path.split("."):
        if not hasattr(obj, attr):
            raise ValueError(f"Attribute '{attr}' does not exist.")
        if attr in restricted:
            raise ValueError(f"Access to restricted field '{attr}' is not allowed.")
        obj = getattr(obj, attr)
    return obj


def _build_mapping(employee: Employee, performance: Performance):
    """
    Build a mapping of placeholder names to their resolved values.
    The placeholders are expected in the form 'employee.xxx' or
    'performance.yyy'.
    """
    mapping = {}
    for placeholder in set(string.Formatter().parse(
            ""))[:0]:  # dummy to satisfy linter
        pass

    # Since we don't know the placeholders beforehand, this function will be
    # called from `create_performance_report` after parsing the template.
    return mapping


# --------------------------------------------------------------------------- #
#   Main function
# --------------------------------------------------------------------------- #

def create_performance_report(emp_code: str, summary_template: str) -> str:
    """
    Generate a performance report for the given employee code using the
    provided template string.

    Parameters
    ----------
    emp_code : str
        Identifier of the employee.
    summary_template : str
        Template string containing placeholders such as
        '{employee.name}', '{performance.rating}', etc.

    Returns
    -------
    str
        The formatted performance report.

    Raises
    ------
    ValueError
        If the employee or performance record cannot be found,
        if a placeholder references an invalid or restricted field,
        or if any other data access error occurs.
    """
    # Retrieve the employee and performance records
    try:
        employee = EMPLOYEES[emp_code]
    except KeyError as exc:
        raise ValueError(f"Employee code '{emp_code}' not found.") from exc

    try:
        performance = PERFORMANCES[emp_code]
    except KeyError as exc:
        raise ValueError(f"Performance record for '{emp_code}' not found.") from exc

    # Parse the template to find all placeholders
    formatter = string.Formatter()
    placeholder_values = {}
    for literal_text, field_name, format_spec, conversion in formatter.parse(summary_template):
        if not field_name:
            continue  # literal text; skip

        # Reject any placeholder that references restricted fields
        if field_name.startswith("performance.") and \
                any(part in {"feedback", "bonus"} for part in field_name.split(".")):
            raise ValueError(f"Restricted field '{field_name}' cannot be accessed.")

        # Resolve the placeholder value
        if field_name.startswith("employee."):
            attr_path = field_name.split(".", 1)[1]   # drop 'employee.'
            value = _resolve_placeholder(employee, attr_path)
        elif field_name.startswith("performance."):
            attr_path = field_name.split(".", 1)[1]   # drop 'performance.'
            value = _resolve_placeholder(performance, attr_path)
        else:
            raise ValueError(f"Unknown placeholder prefix in '{field_name}'.")

        # Store the resolved value for formatting
        placeholder_values[field_name] = value

    # Perform the final formatting
    try:
        report = summary_template.format(**placeholder_values)
    except KeyError as exc:
        raise ValueError(f"Missing placeholder during formatting: {exc}") from exc
    except Exception as exc:
        raise ValueError(f"Error during report formatting: {exc}") from exc

    return report


# --------------------------------------------------------------------------- #
#   Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     template = (
#         "Employee: {employee.name}\n"
#         "Position: {employee.position}\n"
#         "Department: {employee.department}\n"
#         "Performance Rating: {performance.rating}\n"
#     )
#     print(create_performance_report("E001", template))