import re
import operator
from functools import reduce

# Mapping of string operators to functions from the `operator` module.
OPERATORS = {
    '=': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le,
}

# Regular expressions for parsing the SQL‑like query.
SELECT_RE = re.compile(r'\s*SELECT\s+(?P<columns>[\*\w,\s]+)\s+FROM\s+\w+', re.IGNORECASE)
WHERE_RE = re.compile(r'\s*WHERE\s+(?P<clause>.+)', re.IGNORECASE)
ORDER_RE = re.compile(r'\s*ORDER\s+BY\s+(?P<col>\w+)(?:\s+(?P<dir>ASC|DESC))?', re.IGNORECASE)

# Regex for a simple condition: column operator value
COND_RE = re.compile(
    r'(?P<col>\w+)\s*(?P<op>=|!=|<>|<=?|>=?)\s*'
    r'(?P<val>.+)', re.IGNORECASE
)

# Allowed characters in a value (digits, quotes, etc.) – basic validation to mitigate injection.
VAL_RE = re.compile(r'^[\w\'"\.\-]+$')


def _parse_select(query):
    m = SELECT_RE.search(query)
    if not m:
        raise ValueError("SELECT clause missing or malformed.")
    cols = [c.strip() for c in m.group('columns').split(',')]
    if len(cols) == 1 and cols[0] == '*':
        return None  # None will mean all columns
    for col in cols:
        if not re.match(r'^\w+$', col):
            raise ValueError(f"Invalid column name in SELECT: {col}")
    return cols


def _parse_where(query):
    m = WHERE_RE.search(query)
    if not m:
        return None  # No filtering
    clause = m.group('clause').strip()
    # Split by AND/OR (case-insensitive). For simplicity, only support AND.
    parts = re.split(r'\s+AND\s+', clause, flags=re.IGNORECASE)
    conditions = []
    for part in parts:
        m2 = COND_RE.match(part.strip())
        if not m2:
            raise ValueError(f"Malformed WHERE condition: {part}")
        col = m2.group('col')
        op_str = m2.group('op')
        val_raw = m2.group('val').strip()
        if not VAL_RE.match(val_raw):
            raise ValueError(f"Invalid value in WHERE condition: {val_raw}")
        # Convert to appropriate Python type
        if val_raw.startswith(("'", '"')) and val_raw.endswith(("'", '"')):
            value = val_raw[1:-1]
        else:
            try:
                if '.' in val_raw:
                    value = float(val_raw)
                else:
                    value = int(val_raw)
            except ValueError:
                # Treat as string if not numeric
                value = val_raw
        op_func = OPERATORS.get(op_str)
        if not op_func:
            raise ValueError(f"Unsupported operator in WHERE: {op_str}")
        conditions.append((col, op_func, value))
    return conditions


def _parse_order(query):
    m = ORDER_RE.search(query)
    if not m:
        return None
    col = m.group('col')
    direction = m.group('dir')
    reverse = direction and direction.upper() == 'DESC'
    return col, reverse


def _row_matches(row, conditions):
    for col, op_func, val in conditions:
        if col not in row:
            return False
        try:
            if not op_func(row[col], val):
                return False
        except Exception:
            return False
    return True


def run_user_query(dataset, sql_query):
    """
    Execute a very small subset of SQL on an in‑memory list of dictionaries.

    Parameters
    ----------
    dataset : list[dict]
        The data to query.
    sql_query : str
        SQL‑like query string.

    Returns
    -------
    list[dict]
        Query result as a list of dictionaries with selected columns.

    Raises
    ------
    ValueError
        If the query is malformed or execution fails.
    """
    if not isinstance(dataset, list) or not all(isinstance(r, dict) for r in dataset):
        raise ValueError("Dataset must be a list of dictionaries.")
    if not isinstance(sql_query, str):
        raise ValueError("Query must be a string.")

    # Parse clauses
    try:
        select_cols = _parse_select(sql_query)
        where_conditions = _parse_where(sql_query)
        order_clause = _parse_order(sql_query)
    except ValueError as exc:
        raise ValueError(f"Query parsing error: {exc}") from None

    # Filter rows
    if where_conditions:
        filtered = [row for row in dataset if _row_matches(row, where_conditions)]
    else:
        filtered = list(dataset)

    # Order rows
    if order_clause:
        col, reverse = order_clause
        try:
            filtered.sort(key=lambda r: r.get(col), reverse=reverse)
        except Exception as exc:
            raise ValueError(f"Ordering failed: {exc}") from None

    # Project columns
    if select_cols is None:
        result = [dict(row) for row in filtered]
    else:
        result = [{c: row.get(c) for c in select_cols} for row in filtered]

    return result