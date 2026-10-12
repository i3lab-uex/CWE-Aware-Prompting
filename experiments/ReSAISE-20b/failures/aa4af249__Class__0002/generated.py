import re
from operator import eq, ne, lt, le, gt, ge
from functools import reduce

# Mapping of supported comparison operators to functions
COMPARISON_OPS = {
    '=': eq,
    '!=': ne,
    '<>': ne,
    '>': gt,
    '<': lt,
    '>=': ge,
    '<=': le
}

# Regex patterns for parsing the SQL‑like statement
SELECT_RE = re.compile(
    r'^\s*SELECT\s+(?P<columns>[\w\s,]+)\s*(?:WHERE\s+(?P<where>[^ORDER]*))?(?:\s+ORDER\s+BY\s+(?P<orderby>.+))?\s*$', re.IGNORECASE)
COND_RE = re.compile(
    r'(?P<field>\w+)\s*(?P<op>=|!=|<>|>|<|>=|<=)\s*(?P<value>.+?)\s*(?:AND|$)', re.IGNORECASE)
ORDER_RE = re.compile(r'(?P<field>\w+)\s*(?P<dir>ASC|DESC)?', re.IGNORECASE)


def _parse_value(val: str):
    """Parse a literal value from the query."""
    val = val.strip()
    # Try integer
    if re.match(r'^\d+$', val):
        return int(val)
    # Try float
    if re.match(r'^\d+\.\d*$', val):
        return float(val)
    # Try quoted string
    m = re.match(r"^(['\"])(.*)\1$", val)
    if m:
        return m.group(2)
    # Fallback: treat as string
    return val


def _evaluate_condition(record, field, op_func, value):
    if field not in record:
        return False
    try:
        return op_func(record[field], value)
    except Exception:
        return False


def process_sql_request(dataset_records, sql_statement):
    """
    Execute a simple SQL‑like query on an in‑memory list of dictionaries.

    Parameters
    ----------
    dataset_records : list[dict]
        The dataset to query.
    sql_statement : str
        The SQL‑like statement.

    Returns
    -------
    list[dict]
        Query results as a list of dictionaries.

    Raises
    ------
    ValueError
        If the statement is malformed or cannot be executed.
    """
    if not isinstance(dataset_records, list):
        raise ValueError("dataset_records must be a list of dictionaries")
    if not isinstance(sql_statement, str):
        raise ValueError("sql_statement must be a string")

    match = SELECT_RE.match(sql_statement)
    if not match:
        raise ValueError("Invalid or unsupported SQL statement")

    # Parse SELECT columns
    cols_raw = match.group('columns')
    selected_cols = [c.strip() for c in cols_raw.split(',')]
    if not all(col for col in selected_cols):
        raise ValueError("Empty column name detected")

    # Parse WHERE clause
    where_raw = match.group('where')
    conditions = []
    if where_raw:
        for cond_match in COND_RE.finditer(where_raw):
            field = cond_match.group('field')
            op_symbol = cond_match.group('op')
            val_raw = cond_match.group('value')
            if op_symbol not in COMPARISON_OPS:
                raise ValueError(f"Unsupported operator '{op_symbol}'")
            conditions.append((field, COMPARISON_OPS[op_symbol], _parse_value(val_raw)))

    # Parse ORDER BY clause
    orderby_raw = match.group('orderby')
    order_keys = []
    if orderby_raw:
        for ord_match in ORDER_RE.finditer(orderby_raw):
            field = ord_match.group('field')
            direction = ord_match.group('dir') or 'ASC'
            reverse = direction.upper() == 'DESC'
            order_keys.append((field, reverse))

    # Filter records
    def record_matches(rec):
        return all(_evaluate_condition(rec, f, op_func, v) for f, op_func, v in conditions)

    filtered = [rec for rec in dataset_records if record_matches(rec)]

    # Sort records
    def sort_key_func(rec):
        return tuple(
            rec.get(field) if not rev else _negate_value(rec.get(field))
            for field, rev in order_keys
        )

    def _negate_value(val):
        # For numeric values, negate; for others, return as is (order will be reversed by reverse flag)
        if isinstance(val, (int, float)):
            return -val
        return val

    if order_keys:
        filtered.sort(key=sort_key_func)

    # Project selected columns
    result = []
    for rec in filtered:
        projected = {}
        for col in selected_cols:
            if col not in rec:
                raise ValueError(f"Column '{col}' does not exist in record")
            projected[col] = rec[col]
        result.append(projected)

    return result