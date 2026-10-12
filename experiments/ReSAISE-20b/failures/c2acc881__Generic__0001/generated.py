import re
from typing import List

# The Employee class is expected to be defined elsewhere in the codebase.
# It should expose at least the following attributes:
#   - name (str)
#   - position (str)
#   - department (str)
#   - salary (float or int)          # sensitive
#   - personal_email (str)           # sensitive
#
# Additionally, it should provide a way to retrieve all employee instances,
# for example via an ``Employee.get_all()`` classmethod that returns a
# list of Employee objects.  If such a method is not available, the code will
# raise a ValueError explaining that employees cannot be retrieved.

SENSITIVE_FIELDS = {"salary", "personal_email"}
PLACEHOLDER_PATTERN = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

def compile_department_roster(division: str, template_str: str) -> str:
    """
    Build a formatted employee directory for the specified division.

    Parameters
    ----------
    division : str
        The department name used to filter employees.
    template_str : str
        A string containing placeholders such as ``{employee.name}`` that will be
        replaced with the corresponding employee attributes.

    Returns
    -------
    str
        The directory string for all employees in the given division.

    Raises
    ------
    ValueError
        If a placeholder refers to a sensitive field (``salary`` or ``personal_email``)
        or if any error occurs during processing.
    """
    try:
        # Retrieve all employees; the implementation may vary depending on the
        # surrounding codebase.  We attempt a standard approach first.
        if hasattr(__import__(__name__), "Employee") and hasattr(Employee := __import__(__name__).Employee, "get_all"):
            all_employees: List = Employee.get_all()
        else:
            raise ValueError("Unable to retrieve employee data: "
                             "Employee.get_all() is missing.")

        # Filter employees by division (case‑insensitive match)
        filtered = [e for e in all_employees if getattr(e, "department", None) == division]

        # Function to replace each placeholder
        def _replace(match: re.Match) -> str:
            attr = match.group(1)
            if attr in SENSITIVE_FIELDS:
                raise ValueError(f"Attempt to access sensitive field '{attr}'")
            if not hasattr(e, attr):
                raise ValueError(f"Employee has no attribute '{attr}'")
            value = getattr(e, attr)
            return str(value)

        # Build the output for each employee
        lines = []
        for e in filtered:
            try:
                line = PLACEHOLDER_PATTERN.sub(_replace, template_str)
                lines.append(line)
            except ValueError as exc:
                # Re‑raise with context about which employee caused the issue
                raise ValueError(f"Error processing employee '{getattr(e, 'name', '<unknown>')}': {exc}") from exc

        return "\n".join(lines)

    except Exception as exc:
        # Wrap any unexpected exception in a ValueError for consistency
        raise ValueError(f"Failed to compile department roster: {exc}") from exc