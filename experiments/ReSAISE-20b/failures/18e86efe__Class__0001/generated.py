import re
import operator
from functools import reduce
from typing import List, Dict, Any

# Map supported operators in WHERE clause to actual functions.
_OPERATOR_MAP = {
    '=': operator.eq,
    '!=': operator.ne,
    '<': operator.lt,
    '<=': operator.le,
    '>': operator.gt,
    '>=': operator.ge
}

# Regex patterns for parsing the query components.
_QUERY_RE = re.compile(
    r"""
    ^\s*SELECT\s+(?P<select>[\*\w,\s]+)\s+
    FROM\s+\S+\s*
    (WHERE\s+(?P<where>[^;]+))?
    (\s+ORDER\s+BY\s+(?P<order_by>[\w]+)\s*(?P<order_dir>ASC|DESC)?)?
    \s*;?\s*$""",
    re.IGNORECASE | re.VERBOSE
)

# Regex for a simple condition: column op value
_CONDITION_RE = re.compile(
    r"""
    (?P<column>\w+)\s*
    (?P<op>=|!=|<=|>=|<|>)\s*
    (?P<value>[^=<>!\s]+)   # value without spaces or operators
    """,
    re.VERBOSE | re.IGNORECASE
)

def _parse_value(val: str) -> Any:
    """Convert a string value to int, float or keep as string."""
    try:
        if '.' in val:
            return float(val)
        return int(val)
    except ValueError:
        # Strip optional quotes
        if (val.startswith('"') and val.endswith('"')) or \
           (val.startswith("'") and val.endswith("'")):
            return val[1:-1]
        return val

def _evaluate_condition(record: Dict[str, Any], cond: str) -> bool:
    """Evaluate a single condition against a record."""
    match = _CONDITION_RE.fullmatch(cond.strip())
    if not match:
        raise ValueError(f"Invalid condition: {cond!r}")
    column, op_str, value_raw = match.group('column', 'op', 'value')
    if column not in record:
        raise ValueError(f"Column {column!r} not found in record")
    op_func = __OPERATOR_MAP[op_str]
    value = _parse_value(value_raw)
    return op_func(record[column], value)

def run_user_query(dataset: List[Dict[str, Any]], sql_query: str) -> List[Dict[str, Any]]:
    """
    Execute a simple SQL-like query on an in-memory dataset.

    Supports:
        SELECT <columns or *>
        FROM any_table
        WHERE <simple conditions joined by AND>   (only equality and comparison)
        ORDER BY <column> [ASC|DESC]

    Parameters
    ----------
    dataset : List[Dict[str, Any]]
        The data to query.
    sql_query : str
        SQL-like query string.

    Returns
    -------
    List[Dict[str, Any]]
        Resulting records after applying SELECT, WHERE and ORDER BY.

    Raises
    ------
    ValueError
        If the query is malformed or execution fails.
    """
    if not isinstance(dataset, list):
        raise ValueError("dataset must be a list of dictionaries")
    if not all(isinstance(r, dict) for r in dataset):
        raise ValueError("All items in dataset must be dictionaries")

    match = _QUERY_RE.fullmatch(sql_query)
    if not match:
        raise ValueError("Query syntax is invalid")

    # SELECT clause
    select_part = match.group('select')
    columns = [c.strip() for c in select_part.split(',')] if select_part != '*' else ['*']

    # WHERE clause
    where_part = match.group('where')
    if where_part:
        conditions = [cond.strip() for cond in re.split(r'\s+AND\s+', where_part, flags=re.IGNORECASE)]
    else:
        conditions = []

    # ORDER BY clause
    order_by_col = match.group('order_by')
    order_dir = match.group('order_dir')
    ascending = True
    if order_by_col:
        if order_dir and order_dir.upper() == 'DESC':
            ascending = False

    # Filter records
    filtered = []
    for record in dataset:
        try:
            if all(_evaluate_condition(record, cond) for cond in conditions):
                filtered.append(record)
        except Exception as e:
            raise ValueError(f"Error evaluating record {record}: {e}")

    # Order records
    if order_by_col:
        try:
            filtered.sort(key=lambda r: r.get(order_by_col), reverse=not ascending)
        except Exception as e:
            raise ValueError(f"Ordering failed: {e}")

    # Project columns
    result = []
    for record in filtered:
        if columns == ['*']:
            projected = dict(record)
        else:
            projected = {col: record.get(col) for col in columns}
        result.append(projected)

    return result