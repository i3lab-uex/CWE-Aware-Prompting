import re
import operator
from functools import cmp_to_key
from typing import List, Dict, Any

# Mapping of supported operators to functions
_OPERATOR_MAP = {
    '==': operator.eq,
    '=': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,
    '>=': operator.ge,
    '<=': operator.le,
    '>': operator.gt,
    '<': operator.lt,
}

# Regular expression to parse the simple SQL‑like statement
_QUERY_RE = re.compile(
    r'''
    ^\s*SELECT\s+(?P<select>[\*\w,\s]+)\s*
    (?:FROM\s+\w+\s*)?                      # optional table name, ignored
    (?:WHERE\s+(?P<where>.+?)\s*)?
    (?:ORDER\s+BY\s+(?P<order>\w+)\s*(?P<dir>ASC|DESC)?)?
    \s*;?\s*$                                 # optional trailing semicolon
    ''',
    re.IGNORECASE | re.VERBOSE,
)

# Regular expression to parse a simple condition (field op value)
_COND_RE = re.compile(
    r'''
    (?P<field>\w+)\s*
    (?P<op>==|=|!=|<>|>=|<=|>|<)\s*
    (?P<value>.+)
    ''',
    re.VERBOSE,
)

def _parse_literal(literal: str) -> Any:
    """Convert a literal string into an int, float or stripped string."""
    literal = literal.strip()
    # Strip surrounding quotes if present
    if (literal.startswith('"') and literal.endswith('"')) or \
       (literal.startswith("'") and literal.endswith("'")):
        return literal[1:-1]
    # Try int
    try:
        return int(literal)
    except ValueError:
        pass
    # Try float
    try:
        return float(literal)
    except ValueError:
        pass
    # Fallback to string
    return literal

def _evaluate_condition(record: Dict[str, Any], cond_str: str) -> bool:
    """Evaluate a single condition against a record."""
    m = _COND_RE.fullmatch(cond_str.strip())
    if not m:
        raise ValueError(f"Invalid WHERE condition: '{cond_str}'")
    field, op_sym, value_raw = m.group('field', 'op', 'value')
    if field not in record:
        raise ValueError(f"Field '{field}' not found in record")
    op_func = __OPERATOR_MAP.get(op_sym)
    if not op_func:
        raise ValueError(f"Unsupported operator '{op_sym}'")
    value = _parse_literal(value_raw)
    return op_func(record[field], value)

def submit_user_query(records: List[Dict[str, Any]], sql_statement: str) -> List[Dict[str, Any]]:
    """
    Execute a simple SQL‑like query on the provided list of dictionaries.

    Parameters
    ----------
    records : List[Dict[str, Any]]
        The dataset to query.
    sql_statement : str
        A SQL‑like statement supporting SELECT, WHERE and ORDER BY clauses.

    Returns
    -------
    List[Dict[str, Any]]
        The query result as a list of dictionaries.

    Raises
    ------
    ValueError
        If the statement is malformed or execution fails.
    """
    if not isinstance(records, list):
        raise ValueError("records must be a list of dictionaries")
    for rec in records:
        if not isinstance(rec, dict):
            raise ValueError("All items in records must be dictionaries")

    m = _QUERY_RE.fullmatch(sql_statement)
    if not m:
        raise ValueError("Invalid query format")

    # SELECT clause
    select_part = m.group('select')
    fields = [f.strip() for f in select_part.split(',')]
    if fields == ['*']:
        selected_fields = None  # means all fields
    else:
        for f in fields:
            if not re.match(r'^\w+$', f):
                raise ValueError(f"Invalid field name in SELECT: '{f}'")
        selected_fields = fields

    # WHERE clause
    where_part = m.group('where')
    if where_part:
        def record_matches(rec):
            try:
                return _evaluate_condition(rec, where_part)
            except ValueError as e:
                raise ValueError(f"WHERE evaluation error: {e}") from None
    else:
        def record_matches(rec):
            return True

    # ORDER BY clause
    order_field = m.group('order')
    order_dir = (m.group('dir') or 'ASC').upper()
    reverse_order = order_dir == 'DESC'
    if order_field and not re.match(r'^\w+$', order_field):
        raise ValueError(f"Invalid ORDER BY field: '{order_field}'")

    # Filter records
    filtered = [rec for rec in records if record_matches(rec)]

    # Order records
    if order_field:
        try:
            filtered.sort(key=lambda r: r[order_field], reverse=reverse_order)
        except KeyError:
            raise ValueError(f"ORDER BY field '{order_field}' not found in records")

    # Project fields
    if selected_fields is not None:
        result = [{k: rec[k] for k in selected_fields if k in rec} for rec in filtered]
    else:
        result = [rec.copy() for rec in filtered]

    return result