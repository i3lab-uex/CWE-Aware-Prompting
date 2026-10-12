import re
import operator
from functools import reduce
from typing import List, Dict, Any

# Mapping of supported comparison operators to functions
_OP_MAP = {
    "=": operator.eq,
    "!=": operator.ne,
    "<": operator.lt,
    ">": operator.gt,
    "<=": operator.le,
    ">=": operator.ge,
}

# Regex patterns
_SELECT_RE = re.compile(r"SELECT\s+(?P<fields>[\*\w,\s]+)\s+WHERE\s+(?P<condition>.+?)\s*(ORDER BY\s+(?P<orderby>.+))?$",
                        re.IGNORECASE | re.DOTALL)
_CONDITION_RE = re.compile(r"(?P<field>\w+)\s*(?P<op>=|!=|<=|>=|<|>)\s*(?P<value>.+)", re.IGNORECASE)
_ORDERBY_RE = re.compile(r"(?P<field>\w+)(?:\s+(?P<direction>ASC|DESC))?", re.IGNORECASE)

def _parse_value(val: str) -> Any:
    """Parse a value literal (number, quoted string)."""
    val = val.strip()
    if re.match(r"^'([^']*)'$", val) or re.match(r'^\"([^\"]*)\"$', val):
        return re.sub(r"^['\"]|['\"]$", "", val)
    # Try numeric
    try:
        if "." in val:
            return float(val)
        return int(val)
    except ValueError:
        pass
    # Fallback to string without quotes
    return val

def _build_condition(cond_str: str):
    """Return a function that evaluates the condition on a record."""
    m = _CONDITION_RE.fullmatch(cond_str.strip())
    if not m:
        raise ValueError(f"Invalid WHERE condition: {cond_str}")
    field, op_symbol, value = m.group('field'), m.group('op'), m.group('value')
    op_func = _OP_MAP[op_symbol]
    cmp_value = _parse_value(value)

    def condition(record: Dict[str, Any]) -> bool:
        try:
            return op_func(record.get(field), cmp_value)
        except Exception:
            # If types are incompatible, treat as False
            return False

    return condition

def _parse_orderby(orderby_str: str):
    """Return a list of (field, reverse) tuples."""
    orderings = []
    for part in orderby_str.split(","):
        m = _ORDERBY_RE.fullmatch(part.strip())
        if not m:
            raise ValueError(f"Invalid ORDER BY clause: {part}")
        field = m.group('field')
        direction = m.group('direction')
        reverse = direction.lower() == 'desc' if direction else False
        orderings.append((field, reverse))
    return orderings

def run_custom_query(dataset: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
    """
    Execute a simple SQL-like SELECT query on an in-memory dataset.

    Supported syntax:
        SELECT <fields> WHERE <condition> [ORDER BY <field> [ASC|DESC], ...]
    - <fields>: comma-separated list of field names or * for all fields
    - <condition>: a single comparison like `age >= 30` or `name = 'Alice'`
    - ORDER BY: optional, supports multiple fields and ASC/DESC ordering

    Parameters
    ----------
    dataset : list of dict
        The data to query.
    query : str
        SQL-like query string.

    Returns
    -------
    list of dict
        The filtered, projected and sorted result set.

    Raises
    ------
    ValueError
        If the query is malformed or cannot be processed.
    """
    if not isinstance(dataset, list) or not all(isinstance(r, dict) for r in dataset):
        raise ValueError("Dataset must be a list of dictionaries.")

    m = _SELECT_RE.fullmatch(query.strip())
    if not m:
        raise ValueError("Query must match the pattern: SELECT ... WHERE ... [ORDER BY ...]")

    fields_str = m.group('fields').strip()
    condition_str = m.group('condition')
    orderby_str = m.group('orderby')

    # Projection
    if fields_str == '*':
        projected_fields = None  # keep all
    else:
        projected_fields = [f.strip() for f in fields_str.split(",")]
        if not all(projected_fields):
            raise ValueError("Field names cannot be empty.")

    # Condition
    condition_func = _build_condition(condition_str)

    # Filter dataset
    filtered = [rec for rec in dataset if condition_func(rec)]

    # Projection step
    if projected_fields is not None:
        result = [{k: rec.get(k) for k in projected_fields} for rec in filtered]
    else:
        result = [rec.copy() for rec in filtered]

    # Ordering
    if orderby_str:
        orderings = _parse_orderby(orderby_str)
        # Build a composite key function
        def sort_key(rec):
            return tuple(
                rec.get(field) if not reverse else _reverse_sort_value(rec.get(field))
                for field, reverse in orderings
            )

        def _reverse_sort_value(val):
            # For numeric types, negate; for others, use tuple with reverse flag
            if isinstance(val, (int, float)):
                return -val
            return val  # strings and others are sorted as is; reverse handled by key tuple

        result.sort(key=sort_key)

    return result