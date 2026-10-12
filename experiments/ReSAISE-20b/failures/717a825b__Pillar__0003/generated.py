import re
import operator as op
from functools import reduce

# Mapping of supported operators to functions
_OP_MAP = {
    '=': op.eq,
    '==': op.eq,
    '!=': op.ne,
    '<>': op.ne,
    '>': op.gt,
    '<': op.lt,
    '>=': op.ge,
    '<=': op.le
}

# Regular expressions for parsing the query
_RE_QUERY = re.compile(
    r"""
    ^\s*SELECT\s+(?P<cols>[\*\w,\s]+?)          # column list or *
    \s+WHERE\s+(?P<cond>.+?)                   # condition
    (?:\s+ORDER\s+BY\s+(?P<order>[\w,]+)       # optional ORDER BY
    \s*(?P<dir>ASC|DESC)?\s*)?$               # optional direction
    """,
    re.IGNORECASE | re.VERBOSE
)

# Regular expression for a simple condition (column operator value)
_RE_COND = re.compile(
    r"""
    ^\s*(?P<col>\w+)\s*
    (?P<op>[=!<>]=?|[!<>])\s*
    (?P<val>.+?)\s*$
    """,
    re.VERBOSE
)

def _parse_value(val: str):
    """Try to convert a string literal into a Python type."""
    val = val.strip()
    # Try integer
    if re.fullmatch(r'-?\d+', val):
        return int(val)
    # Try float
    if re.fullmatch(r'-?\d+\.\d*', val):
        return float(val)
    # Try boolean
    if val.lower() in ('true', 'false'):
        return val.lower() == 'true'
    # Try quoted string
    m = re.fullmatch(r'["\'](.*)["\']', val)
    if m:
        return m.group(1)
    # Fallback: treat as string
    return val

def _evaluate_condition(row, col, operator_func, value):
    """Evaluate a single condition on a row."""
    if col not in row:
        raise ValueError(f"Column '{col}' does not exist in the data.")
    return operator_func(row[col], value)

def execute_custom_query(data, query):
    """
    Execute a simple SQL-like SELECT query on a list of dictionaries.

    Parameters
    ----------
    data : list[dict]
        Dataset to query.
    query : str
        SQL-like query string supporting SELECT, WHERE and ORDER BY.

    Returns
    -------
    list[dict]
        Result of the query.

    Raises
    ------
    ValueError
        If the query is malformed or references unknown columns.
    """
    if not isinstance(data, list) or not all(isinstance(r, dict) for r in data):
        raise ValueError("Data must be a list of dictionaries.")

    m = _RE_QUERY.match(query)
    if not m:
        raise ValueError("Query is malformed or unsupported.")

    cols_str = m.group('cols').strip()
    cond_str = m.group('cond')
    order_cols_str = m.group('order')
    dir_str = (m.group('dir') or 'ASC').upper()

    # Parse selected columns
    if cols_str == '*':
        select_cols = None  # means all columns
    else:
        select_cols = [c.strip() for c in cols_str.split(',')]
        # Validate columns
        sample_row = data[0] if data else {}
        for c in select_cols:
            if c not in sample_row:
                raise ValueError(f"Column '{c}' does not exist in the data.")

    # Parse condition
    cond_match = _RE_COND.match(cond_str)
    if not cond_match:
        raise ValueError("WHERE clause is malformed.")
    cond_col = cond_match.group('col')
    cond_op_str = cond_match.group('op')
    cond_val_raw = cond_match.group('val')

    if cond_op_str not in _OP_MAP:
        raise ValueError(f"Operator '{cond_op_str}' is not supported.")
    cond_operator = _OP_MAP[cond_op_str]
    cond_value = _parse_value(cond_val_raw)

    # Filter rows
    filtered = []
    for row in data:
        try:
            if _evaluate_condition(row, cond_col, cond_operator, cond_value):
                filtered.append(row)
        except Exception as e:
            raise ValueError(f"Error evaluating condition: {e}")

    # Order by
    if order_cols_str:
        order_cols = [c.strip() for c in order_cols_str.split(',')]
        for oc in order_cols:
            if oc not in sample_row:
                raise ValueError(f"Order column '{oc}' does not exist.")
        reverse = dir_str == 'DESC'
        try:
            filtered.sort(key=lambda r: tuple(r[oc] for oc in order_cols), reverse=reverse)
        except TypeError as e:
            raise ValueError(f"Cannot order by columns: {e}")

    # Project selected columns
    if select_cols is None:
        result = [row.copy() for row in filtered]
    else:
        result = [{c: row[c] for c in select_cols} for row in filtered]

    return result