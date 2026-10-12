import re
from functools import reduce
import operator

# ------------------------------------------------------------
# Helper functions for parsing and evaluating WHERE clauses
# ------------------------------------------------------------

def _safe_eval(expr: str, record: dict):
    """
    Evaluate a simple boolean expression using the fields from `record`.
    Only the following operators are allowed: ==, !=, <, <=, >, >=
    Logical operators AND, OR, and parentheses are also supported.
    """
    # Replace logical operators with python equivalents
    expr = re.sub(r'\bAND\b', 'and', expr, flags=re.IGNORECASE)
    expr = re.sub(r'\bOR\b', 'or', expr, flags=re.IGNORECASE)

    # Build a namespace with record values
    safe_globals = {"__builtins__": None}
    # Convert all keys to valid identifiers (replace spaces with underscores)
    safe_locals = {}
    for k, v in record.items():
        safe_locals[k] = v

    try:
        return eval(expr, safe_globals, safe_locals)
    except Exception as e:
        raise ValueError(f"Invalid WHERE expression '{expr}': {e}") from None

# ------------------------------------------------------------
# Main function
# ------------------------------------------------------------

def run_sql_query(records, command):
    """
    Execute a simple SQL-like query on a list of dictionaries.

    Supported syntax:
        SELECT <fields> [WHERE <condition>] [ORDER BY <field> [ASC|DESC]]

    *   selects all fields
    WHERE allows ==, !=, <, <=, >, >= and logical AND/OR.
    ORDER BY sorts the result by a single field.

    Parameters
    ----------
    records : list[dict]
        The dataset to query.
    command : str
        The SQL-like statement.

    Returns
    -------
    list[dict]
        The query result.

    Raises
    ------
    ValueError
        If the command is malformed or cannot be processed.
    """
    if not isinstance(records, list) or any(not isinstance(r, dict) for r in records):
        raise ValueError("records must be a list of dictionaries")

    # Basic pattern
    pattern = re.compile(
        r"""
        ^\s*SELECT\s+(?P<select>[\*\w,\s]+)          # SELECT clause
        (?:\s+WHERE\s+(?P<where>[^;]+?))?           # optional WHERE
        (?:\s+ORDER\s+BY\s+(?P<order>\w+)(?:\s+(?P<dir>ASC|DESC))?)?
        \s*$
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    match = pattern.match(command)
    if not match:
        raise ValueError("Invalid command syntax")

    select_part = match.group('select')
    where_part = match.group('where')
    order_field = match.group('order')
    order_dir = match.group('dir') or 'ASC'

    # Parse SELECT fields
    if select_part.strip() == '*':
        selected_fields = None  # indicates all fields
    else:
        selected_fields = [f.strip() for f in select_part.split(',')]
        if not all(selected_fields):
            raise ValueError("Invalid SELECT fields")

    # Apply WHERE filter
    if where_part:
        filtered = [r for r in records if _safe_eval(where_part, r)]
    else:
        filtered = list(records)

    # Apply ORDER BY
    if order_field:
        try:
            reverse = order_dir.upper() == 'DESC'
            filtered.sort(key=lambda r: r.get(order_field), reverse=reverse)
        except Exception as e:
            raise ValueError(f"ORDER BY failed: {e}") from None

    # Build result with selected fields
    if selected_fields is None:
        result = [dict(r) for r in filtered]
    else:
        missing = set()
        result = []
        for r in filtered:
            row = {}
            for f in selected_fields:
                if f not in r:
                    missing.add(f)
                else:
                    row[f] = r[f]
            result.append(row)

    if missing:
        raise ValueError(f"Fields not found in records: {', '.join(sorted(missing))}")

    return result