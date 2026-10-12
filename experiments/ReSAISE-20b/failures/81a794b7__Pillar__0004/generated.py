import re
from dataclasses import dataclass
from typing import Dict, Any

# ----------------------------------------------------------------------
# Mock data structures (in a real system these would be imported)
# ----------------------------------------------------------------------
@dataclass
class Performance:
    rating: str  # e.g. "Excellent", "Needs Improvement"
    feedback: str  # confidential
    bonus: float   # confidential


@dataclass
class Employee:
    employee_id: str
    name: str
    position: str
    department: str
    performance: Performance


# ----------------------------------------------------------------------
# In‑memory store of employees (replace with real persistence in prod)
# ----------------------------------------------------------------------
_EMPLOYEE_DB: Dict[str, Employee] = {
    "E001": Employee(
        employee_id="E001",
        name="Alice Johnson",
        position="Senior Engineer",
        department="R&D",
        performance=Performance(
            rating="Excellent",
            feedback="Outstanding contributions to the AI project.",
            bonus=5000.00,
        ),
    ),
    "E002": Employee(
        employee_id="E002",
        name="Bob Smith",
        position="Project Manager",
        department="Operations",
        performance=Performance(
            rating="Meets Expectations",
            feedback="Delivered the project on time.",
            bonus=3000.00,
        ),
    ),
}


# ----------------------------------------------------------------------
# Helper: Safe mapping that rejects unauthorized keys
# ----------------------------------------------------------------------
class _SafeMapping(dict):
    """A dictionary wrapper that only allows a predefined set of keys."""

    def __init__(self, allowed_keys: Dict[str, Any], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._allowed_keys = set(allowed_keys)

    def __getitem__(self, key: str) -> Any:
        if key not in self._allowed_keys:
            raise ValueError(f"Unauthorized placeholder '{key}' accessed.")
        return super().__getitem__(key)


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def compile_employee_evaluation(employee_id: str, template: str) -> str:
    """
    Generate a formatted employee evaluation string by replacing placeholders
    in *template* with data from the employee record identified by
    *employee_id*. Only a limited set of placeholders are allowed:
        {personnel.name}
        {personnel.position}
        {review.rating}

    Raises
    ------
    ValueError
        If the employee_id does not exist or an unauthorized placeholder is used.
    """
    # ------------------------------------------------------------------
    # 1. Retrieve employee record
    # ------------------------------------------------------------------
    employee = _EMPLOYEE_DB.get(employee_id)
    if not employee:
        raise ValueError(f"Invalid employee ID: {employee_id}")

    # ------------------------------------------------------------------
    # 2. Prepare allowed data mapping
    # ------------------------------------------------------------------
    data_map = {
        "personnel.name": employee.name,
        "personnel.position": employee.position,
        "review.rating": employee.performance.rating,
    }

    # ------------------------------------------------------------------
    # 3. Validate placeholders in the template
    # ------------------------------------------------------------------
    placeholder_pattern = re.compile(r"\{([^{}]+)\}")
    placeholders_in_template = set(placeholder_pattern.findall(template))

    # If any placeholder is not in the allowed list, raise an error
    for ph in placeholders_in_template:
        if ph not in data_map:
            raise ValueError(
                f"Unauthorized placeholder '{ph}' in template. "
                "Only personnel.name, personnel.position, and review.rating are allowed."
            )

    # ------------------------------------------------------------------
    # 4. Perform the substitution safely
    # ------------------------------------------------------------------
    safe_map = _SafeMapping(data_map)
    try:
        formatted_output = template.format_map(safe_map)
    except KeyError as exc:
        # This should not happen due to prior validation, but guard anyway
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    # ------------------------------------------------------------------
    # 5. Return the formatted string
    # ------------------------------------------------------------------
    return formatted_output


# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = (
        "Employee: {personnel.name}\n"
        "Position: {personnel.position}\n"
        "Rating: {review.rating}\n"
    )
    print(compile_employee_evaluation("E001", tmpl))