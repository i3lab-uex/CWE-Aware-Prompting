import re
import operator
from functools import reduce
from typing import List, Dict, Any

# Map string operators to actual functions
OPERATORS = {
    "=": operator.eq,
    "!=": operator.ne,
    "<": operator.lt,
    ">": operator.gt,
    "<=": operator.le,
    ">=": operator.ge
}

# Supported comparison operators in WHERE clauses
COMPARISON_RE = re.compile(r"(?P<field>\w+)\s*(?P<op>=|!=|<=|>=|<|>)\s*(?P<value>.+)")


def _parse_select_clause(query: str) -> List[str]:
    """Extract the list of fields to select."""
    match = re.search(r"SELECT\s+(?P<fields>[\w\*,\s]+)\s+WHERE", query, re.IGNORECASE)
    if not match:
        raise ValueError("Missing or malformed SELECT clause")
    fields_str = match.group("fields").strip()
    if fields_str == "*":
        return []  # empty list denotes all fields
    return [f.strip() for f in fields_str.split(",") if f.strip()]


def _parse_where_clause(query: str) -> List[Dict[str, Any]]:
    """Parse the WHERE clause into a list of conditions."""
    match = re.search(r"WHERE\s+(?P<conditions>.+?)\s+ORDER", query, re.IGNORECASE | re.DOTALL)
    if not match:
        # Try without ORDER BY
        match = re.search(r"WHERE\s+(?P<conditions>.+)$", query, re.IGNORECASE | re.DOTALL)
        if not match:
            raise ValueError("Missing or malformed WHERE clause")
    conditions_str = match.group("conditions").strip()
    # Split on AND (case-insensitive)
    raw_conditions = re.split(r"\s+AND\s+", conditions_str, flags=re.IGNORECASE)
    conditions = []
    for cond in raw_conditions:
        m = COMPARISON_RE.fullmatch(cond.strip())
        if not m:
            raise ValueError(f"Invalid condition: {cond}")
        field, op_str, value_raw = m.group("field"), m.group("op"), m.group("value")
        # Attempt to interpret value as int, float or keep string
        try:
            if "." in value_raw:
                value = float(value_raw)
            else:
                value = int(value_raw)
        except ValueError:
            # Strip quotes if present
            value = value_raw.strip().strip('"').strip("'")
        conditions.append({"field": field, "op": OPERATORS[op_str], "value": value})
    return conditions


def _parse_order_by_clause(query: str) -> List[Dict[str, Any]]:
    """Parse the ORDER BY clause into a list of (field, direction)."""
    match = re.search(r"ORDER\s+BY\s+(?P<order>.+)$", query, re.IGNORECASE | re.DOTALL)
    if not match:
        return []  # No ordering requested
    order_str = match.group("order").strip()
    parts = [p.strip() for p in order_str.split(",") if p.strip()]
    ordering = []
    for part in parts:
        tokens = part.split()
        field = tokens[0]
        direction = "ASC"
        if len(tokens) > 1 and tokens[1].upper() in ("ASC", "DESC"):
            direction = tokens[1].upper()
        ordering.append({"field": field, "direction": direction})
    return ordering


def _apply_where(data: List[Dict[str, Any]], conditions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Filter data according to all conditions."""
    def matches(record):
        return all(cond["op"](record.get(cond["field"]), cond["value"]) for cond in conditions)
    return list(filter(matches, data))


def _apply_order_by(data: List[Dict[str, Any]], ordering: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Sort data according to ordering specifications."""
    if not ordering:
        return data
    # Build a composite key function
    def sort_key(record):
        keys = []
        for ord_item in ordering:
            val = record.get(ord_item["field"])
            # None values should sort last
            keys.append((val is None, val))
        return tuple(keys)

    reverse = any(ord_item["direction"] == "DESC" for ord_item in ordering)
    return sorted(data, key=sort_key, reverse=reverse)


def _project_fields(record: Dict[str, Any], fields: List[str]) -> Dict[str, Any]:
    """Return a new record containing only the requested fields."""
    if not fields:
        return record.copy()
    return {f: record.get(f) for f in fields}


def execute_custom_query(data: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
    """
    Execute a simple SQL-like query on an in-memory list of dictionaries.

    Supported syntax:
        SELECT <field1, field2, ... | *>
        WHERE <condition> [AND <condition>...]
        ORDER BY <field1> [ASC|DESC], <field2> [ASC|DESC]...

    Example:
        query = "SELECT name, age WHERE age >= 30 AND status = 'active' ORDER BY age DESC"
    """
    if not isinstance(data, list) or not all(isinstance(r, dict) for r in data):
        raise ValueError("Data must be a list of dictionaries")
    if not isinstance(query, str):
        raise ValueError("Query must be a string")

    # Normalize whitespace
    query = " ".join(query.strip().split())

    try:
        fields = _parse_select_clause(query)
        conditions = _parse_where_clause(query)
        ordering = _parse_order_by_clause(query)

        # Filter
        filtered = _apply_where(data, conditions)
        # Order
        ordered = _apply_order_by(filtered, ordering)
        # Project fields
        result = [_project_fields(r, fields) for r in ordered]
    except Exception as e:
        raise ValueError(f"Failed to execute query: {e}") from e

    return result