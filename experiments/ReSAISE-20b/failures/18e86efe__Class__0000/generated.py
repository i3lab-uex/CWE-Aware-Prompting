import re
import operator
from functools import cmp_to_key
from typing import List, Dict, Any

# Mapping of supported comparison operators to the corresponding operator functions
_COMPARISONS = {
    '=': operator.eq,
    '!=': operator.ne,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le
}

# Regular expressions for parsing the query
_QUERY_RE = re.compile(
    r'''
    ^\s*SELECT\s+(?P<columns>[\w\*,\s]+?)      # SELECT clause
    \s+WHERE\s+(?P<condition>[^;]+?)          # WHERE clause
    (?:\s+ORDER\s+BY\s+(?P<orderby>[^;]+))?   # optional ORDER BY
    \s*$''',
    re.IGNORECASE | re.VERBOSE
)

_CONDITION_RE = re.compile(
    r'''
    ^\s*(?P<col>\w+)\s*
    (?P<op>=|!=|>|<|>=|<=)\s*
    (?P<val>.+?)\s*$
    ''',
    re.VERBOSE
)

_ORDERBY_RE = re.compile(
    r'''
    ^\s*(?P<col>\w+)\s*
    (?P<dir>ASC|DESC)?\s*$
    ''',
    re.IGNORECASE | re.VERBOSE
)

def _parse_value(val: str) -> Any:
    """Parse a value literal into an int, float or stripped string."""
    val = val.strip()
    if (val.startswith("'") and val.endswith("'")) or (val.startswith('"') and val.endswith('"')):
        return val[1:-1]
    # Try integer
    try:
        return int(val)
    except ValueError:
        pass
    # Try float
    try:
        return float(val)
    except ValueError:
        pass
    # Fallback: string without quotes
    return val

def _build_condition(cond_str: str):
    """Build a callable that evaluates the condition on a record."""
    m = _CONDITION_RE.match(cond_str)
    if not m:
        raise ValueError(f"Invalid WHERE condition: '{cond_str}'")
    col, op_sym, val_raw = m.group('col'), m.group('op'), m.group('val')
    if op_sym not in _COMPARISONS:
        raise ValueError(f"Unsupported operator '{op_sym}' in WHERE clause")
    op_func = _COMPARISONS[op_sym]
    val = _parse_value(val_raw)

    def predicate(record: Dict[str, Any]) -> bool:
        if col not in record:
            return False
        try:
            return op_func(record[col], val)
        except Exception as e:
            raise ValueError(f"Error evaluating condition on record {record}: {e}") from e

    return predicate

def _build_orderby(orderby_str: str):
    """Return a key function for sorting and reverse flag."""
    m = _ORDERBY_RE.match(orderby_str)
    if not m:
        raise ValueError(f"Invalid ORDER BY clause: '{orderby_str}'")
    col, dir_ = m.group('col'), m.group('dir')
    reverse = (dir_.upper() == 'DESC') if dir_ else False

    def key_func(record: Dict[str, Any]) -> Any:
        return record.get(col)

    return key_func, reverse

def run_user_query(dataset: List[Dict[str, Any]], sql_query: str) -> List[Dict[str, Any]]:
    """
    Execute a simple SQL-like query on the provided dataset.

    Supported syntax:
        SELECT <columns> WHERE <condition> [ORDER BY <column> [ASC|DESC]]

    Columns can be '*' to select all.
    Condition must be a single comparison (col op value).
    ORDER BY supports one column and optional ASC/DESC.

    Parameters
    ----------
    dataset : List[Dict[str, Any]]
        The data to query.
    sql_query : str
        Query string.

    Returns
    -------
    List[Dict[str, Any]]
        The filtered and sorted result set.

    Raises
    ------
    ValueError
        If the query is malformed or execution fails.
    """
    if not isinstance(dataset, list):
        raise ValueError("dataset must be a list of dictionaries")
    if not all(isinstance(r, dict) for r in dataset):
        raise ValueError("All items in dataset must be dictionaries")

    m = _QUERY_RE.match(sql_query)
    if not m:
        raise ValueError("Query does not match supported pattern")

    # SELECT columns
    cols_part = m.group('columns')
    selected_cols = [c.strip() for c in cols_part.split(',')]
    if len(selected_cols) == 1 and selected_cols[0] == '*':
        selected_cols = None  # means all columns

    # WHERE condition
    condition_str = m.group('condition')
    predicate = _build_condition(condition_str)

    # ORDER BY
    orderby_part = m.group('orderby')
    if orderby_part:
        key_func, reverse_flag = _build_orderby(orderby_part)
    else:
        key_func, reverse_flag = None, False

    # Apply filtering
    try:
        filtered = [rec for rec in dataset if predicate(rec)]
    except Exception as e:
        raise ValueError(f"Error during filtering: {e}") from e

    # Apply sorting
    if key_func:
        try:
            filtered.sort(key=key_func, reverse=reverse_flag)
        except Exception as e:
            raise ValueError(f"Error during sorting: {e}") from e

    # Apply projection
    if selected_cols is not None:
        result = []
        for rec in filtered:
            projected = {col: rec.get(col) for col in selected_cols}
            result.append(projected)
    else:
        result = filtered

    return result