import re
from typing import List, Dict, Any

def run_sql_query(records: List[Dict[str, Any]], command: str) -> List[Dict[str, Any]]:
    """
    Execute a very small subset of SQL-like queries on an in-memory list of dictionaries.

    Supported syntax (case‑insensitive):
        SELECT <columns> [WHERE <condition>] [ORDER BY <column> [ASC|DESC]]

    Examples:
        SELECT name, age WHERE age > 20 ORDER BY age DESC
        SELECT * WHERE score >= 90
    """
    if not isinstance(records, list) or any(not isinstance(r, dict) for r in records):
        raise ValueError("records must be a list of dictionaries")

    # Normalize whitespace and case
    cmd = command.strip()
    if not cmd:
        raise ValueError("empty command")

    # Regex to capture SELECT part, optional WHERE and ORDER BY
    pattern = re.compile(
        r"SELECT\s+(?P<cols>[\*\w,\s]+)"
        r"(?:\s+WHERE\s+(?P<where>[^O]+))?"
        r"(?:\s+ORDER\s+BY\s+(?P<order>\w+)(?:\s+(?P<dir>ASC|DESC))?)?",
        re.IGNORECASE
    )
    match = pattern.fullmatch(cmd)
    if not match:
        raise ValueError("Invalid query format")

    # Parse columns
    cols_raw = match.group('cols').strip()
    if cols_raw == '*':
        selected_cols = None  # means all columns
    else:
        selected_cols = [c.strip() for c in cols_raw.split(',')]
        if not all(selected_cols):
            raise ValueError("Empty column name detected")

    # Parse WHERE clause
    where_clause = match.group('where')
    if where_clause:
        where_clause = where_clause.strip()
        # Replace field names with dictionary lookups
        def replace_field(match_obj):
            name = match_obj.group(0)
            if name in ('AND', 'OR', 'NOT'):
                return name.lower()
            return f"record.get('{name}')"
        # Simple tokenization to avoid replacing operators
        expr = re.sub(r'\b\w+\b', replace_field, where_clause)
    else:
        expr = None

    # Parse ORDER BY
    order_col = match.group('order')
    order_dir = match.group('dir')
    if order_col:
        order_col = order_col.strip()
        reverse = (order_dir or '').upper() == 'DESC'
    else:
        reverse = False

    # Helper to evaluate the where expression
    def matches(record: Dict[str, Any]) -> bool:
        if expr is None:
            return True
        try:
            # Evaluate with a very limited environment
            return bool(eval(expr, {"__builtins__": None}, {"record": record}))
        except Exception as exc:
            raise ValueError(f"Failed to evaluate WHERE clause: {exc}") from exc

    # Filter records
    filtered = [rec for rec in records if matches(rec)]

    # Sort records if needed
    if order_col:
        try:
            filtered.sort(key=lambda r: r.get(order_col), reverse=reverse)
        except TypeError as exc:
            raise ValueError(f"Cannot sort by column '{order_col}': {exc}") from exc

    # Project selected columns
    if selected_cols is None:
        result = [dict(rec) for rec in filtered]
    else:
        result = []
        for rec in filtered:
            proj = {}
            for col in selected_cols:
                if col not in rec:
                    raise ValueError(f"Column '{col}' does not exist in records")
                proj[col] = rec[col]
            result.append(proj)

    return result