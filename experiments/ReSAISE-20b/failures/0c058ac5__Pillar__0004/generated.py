import re
import operator
from functools import partial
from typing import List, Dict, Any

# Mapping of supported operators to the operator module functions
_OP_MAP = {
    '=': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,  # alternative not equal
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le
}

# Regular expression to parse a very small subset of SQL.
# The grammar is intentionally strict:
#   SELECT <cols> [WHERE <condition>] [ORDER BY <col> [ASC|DESC]]
_QUERY_RE = re.compile(
    r"""
    ^\s*SELECT\s+
    (?P<select>[\*\w,\s]+)          # columns or *
    (?:\s+WHERE\s+(?P<where>[^;]+?))?
    (?:\s+ORDER\s+BY\s+(?P<order>\w+)(?:\s+(?P<dir>ASC|DESC))?)?
    \s*;?\s*$                       # optional trailing semicolon
    """,
    re.IGNORECASE | re.VERBOSE,
)

# Regular expression to parse a simple condition:
#   <column> <operator> <value>
_COND_RE = re.compile(
    r"""
    ^\s*
    (?P<col>\w+)\s*
    (?P<op>=|!=|<>|>|<|>=|<=)\s*
    (?P<val>
        '(?:\\'|[^'])*' |   # single quoted string, supports escaped quote
        "(?:\\"|[^"])*" |   # double quoted string, supports escaped quote
        \d+(?:\.\d+)?       # integer or float
    )
    \s*$
    """,
    re.VERBOSE,
)

def _parse_value(val_str: str) -> Any:
    """Convert a literal string into an appropriate Python type."""
    if val_str.startswith(("'", '"')) and val_str.endswith(("'", '"')):
        # Remove surrounding quotes and unescape
        quote = val_str[0]
        inner = val_str[1:-1].replace(f"\\{quote}", quote)
        return inner
    # Try to parse number (int or float)
    try:
        if '.' in val_str:
            return float(val_str)
        return int(val_str)
    except ValueError as exc:
        raise ValueError(f"Invalid literal value: {val_str}") from exc

def _build_where_func(where_clause: str):
    """Return a function that evaluates the where condition for a record."""
    match = _COND_RE.match(where_clause)
    if not match:
        raise ValueError(f"Unsupported or malformed WHERE clause: {where_clause}")
    col = match.group('col')
    op_sym = match.group('op')
    val_raw = match.group('val')

    if op_sym not in _OP_MAP:
        raise ValueError(f"Unsupported operator '{op_sym}' in WHERE clause")
    op_func = _OP_MAP[op_sym]
    val = _parse_value(val_raw)

    def where_func(record: Dict[str, Any]) -> bool:
        if col not in record:
            raise ValueError(f"Column '{col}' does not exist in records")
        return op_func(record[col], val)

    return where_func

def _select_columns(select_clause: str, record: Dict[str, Any]) -> Dict[str, Any]:
    """Return a new dictionary with only the requested columns."""
    if select_clause.strip() == '*':
        return record.copy()
    cols = [c.strip() for c in select_clause.split(',')]
    missing = [c for c in cols if c not in record]
    if missing:
        raise ValueError(f"Columns {missing} not found in record")
    return {c: record[c] for c in cols}

def submit_user_query(records: List[Dict[str, Any]], sql_statement: str) -> List[Dict[str, Any]]:
    """
    Execute a very small subset of SQL against an in‑memory list of dictionaries.

    Parameters
    ----------
    records : List[Dict[str, Any]]
        The dataset to query.
    sql_statement : str
        A SQL‑like statement limited to SELECT, optional WHERE and ORDER BY.

    Returns
    -------
    List[Dict[str, Any]]
        The query result as a list of dictionaries.

    Raises
    ------
    ValueError
        If the query is malformed, references unknown columns, or cannot be executed.
    """
    if not isinstance(records, list) or any(not isinstance(r, dict) for r in records):
        raise ValueError("records must be a list of dictionaries")

    match = _QUERY_RE.match(sql_statement)
    if not match:
        raise ValueError("Query format is invalid or unsupported")

    select_clause = match.group('select')
    where_clause = match.group('where')
    order_col = match.group('order')
    dir_flag = match.group('dir')

    # Build where function if present
    where_func = None
    if where_clause:
        where_func = _build_where_func(where_clause)

    # Filter records
    filtered = []
    for rec in records:
        try:
            if where_func is None or where_func(rec):
                filtered.append(_select_columns(select_clause, rec))
        except Exception as exc:
            raise ValueError(f"Error evaluating record {rec}: {exc}") from exc

    # Order if requested
    if order_col:
        try:
            reverse = (dir_flag or 'ASC').upper() == 'DESC'
            filtered.sort(key=lambda r: r[order_col], reverse=reverse)
        except KeyError as exc:
            raise ValueError(f"ORDER BY column '{order_col}' does not exist") from exc

    return filtered