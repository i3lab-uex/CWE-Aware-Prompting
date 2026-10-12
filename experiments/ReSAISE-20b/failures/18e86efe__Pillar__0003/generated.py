import re
import operator
from functools import reduce

# Mapping of supported operators to functions
_OP_MAP = {
    '=': operator.eq,
    '==': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le,
}

# Regex to parse a simple condition like "age >= 30" or "name = 'John'"
_COND_RE = re.compile(
    r"""(?P<col>\w+)\s*
        (?P<op>==|!=|<>|>=|<=|>|<)\s*
        (?P<val>
            (?:'[^']*')|
            (?:\d+(?:\.\d*)?)|
            (?P<null>NULL)
        )
    """,
    re.VERBOSE | re.IGNORECASE
)

# Regex to parse the overall query
_QUERY_RE = re.compile(
    r"""
        SELECT\s+(?P<cols>[\*\w,\s]+)\s*
        (?:WHERE\s+(?P<where>[^ORDER]*))?
        (?:\s+ORDER\s+BY\s+(?P<order_col>\w+)\s*(?P<order_dir>ASC|DESC)?)?
        \s*$
    """,
    re.IGNORECASE | re.VERBOSE
)

def _parse_value(val: str):
    """Convert a string value from the query into an appropriate Python type."""
    if val.upper() == "NULL":
        return None
    if val.startswith("'") and val.endswith("'"):
        return val[1:-1]
    try:
        if '.' in val:
            return float(val)
        return int(val)
    except ValueError:
        raise ValueError(f"Unsupported literal value: {val}")

def _evaluate_condition(record, col, op_func, val):
    """Evaluate a single condition against a record."""
    if col not in record:
        # Missing column considered as None
        rec_val = None
    else:
        rec_val = record[col]
    return op_func(rec_val, val)

def run_user_query(dataset, sql_query):
    """
    Execute a very small subset of SQL on an in‑memory dataset.

    Parameters
    ----------
    dataset : list[dict]
        List of records. Each record is a dictionary.
    sql_query : str
        Query string in the form:
            SELECT <columns> [WHERE <condition>] [ORDER BY <column> [ASC|DESC]]

    Returns
    -------
    list[dict]
        Resulting records after applying SELECT, WHERE and ORDER BY.

    Raises
    ------
    ValueError
        If the query is malformed or cannot be executed.
    """
    if not isinstance(dataset, list):
        raise ValueError("dataset must be a list of dictionaries")
    if not all(isinstance(r, dict) for r in dataset):
        raise ValueError("all items in dataset must be dictionaries")

    match = _QUERY_RE.match(sql_query.strip())
    if not match:
        raise ValueError("Invalid query syntax")

    # SELECT columns
    cols_str = match.group('cols').strip()
    if cols_str == '*':
        selected_cols = None  # keep all columns
    else:
        selected_cols = [c.strip() for c in cols_str.split(',')]
        if not all(selected_cols):
            raise ValueError("Empty column name in SELECT clause")

    # WHERE condition
    where_clause = match.group('where')
    if where_clause:
        cond_match = _COND_RE.fullmatch(where_clause.strip())
        if not cond_match:
            raise ValueError("Unsupported or malformed WHERE clause")
        col = cond_match.group('col')
        op_str = cond_match.group('op')
        val_raw = cond_match.group('val')
        try:
            val = _parse_value(val_raw)
        except ValueError as e:
            raise ValueError(f"Invalid literal in WHERE clause: {e}") from None
        op_func = _OP_MAP[op_str]
    else:
        col, op_func, val = None, None, None

    # ORDER BY
    order_col = match.group('order_col')
    order_dir = match.group('order_dir')
    if order_col:
        reverse_flag = (order_dir or 'ASC').upper() == 'DESC'
    else:
        reverse_flag = False

    # Filter records
    filtered = []
    for record in dataset:
        try:
            if col is None or _evaluate_condition(record, col, op_func, val):
                filtered.append(record)
        except Exception as exc:
            raise ValueError(f"Error evaluating record {record}: {exc}") from None

    # Sort records if needed
    if order_col:
        try:
            filtered.sort(key=lambda r: r.get(order_col, None), reverse=reverse_flag)
        except Exception as exc:
            raise ValueError(f"Error sorting by {order_col}: {exc}") from None

    # Project selected columns
    if selected_cols is not None:
        result = [{k: v for k, v in rec.items() if k in selected_cols} for rec in filtered]
    else:
        result = [dict(rec) for rec in filtered]  # shallow copy

    return result