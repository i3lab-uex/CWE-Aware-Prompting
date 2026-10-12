import re
import operator
from functools import cmp_to_key
from typing import List, Dict, Any

# Mapping of supported comparison operators
_COMP_OPS = {
    '=': operator.eq,
    '==': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le,
}

# Regular expressions for parsing
_RE_SELECT = re.compile(r'\s*SELECT\s+(?P<fields>[\*\w,\s]+)', re.IGNORECASE)
_RE_WHERE = re.compile(r'\s*WHERE\s+(?P<cond>.+)', re.IGNORECASE)
_RE_ORDER_BY = re.compile(r'\s*ORDER\s+BY\s+(?P<field>\w+)\s*(?P<dir>ASC|DESC)?', re.IGNORECASE)

# Regex for a simple comparison: field op value
_RE_COND = re.compile(
    r'(?P<field>\w+)\s*'
    r'(?P<op>=|==|!=|<>|>|<|>=|<=)\s*'
    r'(?P<value>.+)'
)

def _parse_value(raw: str) -> Any:
    """Parse a literal value (number or quoted string)."""
    raw = raw.strip()
    if raw.startswith(("'", '"')) and raw.endswith(("'", '"')):
        return raw[1:-1]
    # Try integer
    if re.fullmatch(r'-?\d+', raw):
        return int(raw)
    # Try float
    if re.fullmatch(r'-?\d+\.\d+', raw):
        return float(raw)
    # Otherwise treat as string
    return raw

def _evaluate_condition(record: Dict[str, Any], cond_str: str) -> bool:
    """Evaluate a simple condition against a record."""
    m = _RE_COND.fullmatch(cond_str)
    if not m:
        raise ValueError(f"Unsupported condition: {cond_str}")
    field = m.group('field')
    op_sym = m.group('op')
    value_raw = m.group('value')

    if field not in record:
        raise ValueError(f"Field '{field}' not found in records")

    op_func = _COMP_OPS.get(op_sym)
    if not op_func:
        raise ValueError(f"Unsupported operator: {op_sym}")

    record_value = record[field]
    cond_value = _parse_value(value_raw)

    try:
        return op_func(record_value, cond_value)
    except Exception as exc:
        raise ValueError(f"Failed to evaluate condition '{cond_str}': {exc}")

def _parse_order_by(order_clause: str) -> (str, bool):
    """Parse ORDER BY clause into field and direction."""
    m = _RE_ORDER_BY.fullmatch(order_clause)
    if not m:
        raise ValueError(f"Malformed ORDER BY clause: {order_clause}")
    field = m.group('field')
    dir_str = m.group('dir') or 'ASC'
    desc = dir_str.upper() == 'DESC'
    return field, desc

def run_sql_query(records: List[Dict[str, Any]], command: str) -> List[Dict[str, Any]]:
    """
    Execute a simple SQL-like query on an in-memory list of dictionaries.

    Supported syntax:
        SELECT <fields> [WHERE <condition>] [ORDER BY <field> [ASC|DESC]]

    * fields: comma-separated list of keys or '*' for all
    * condition: single comparison like "age > 20" (no logical operators)
    * ORDER BY: specify a single field and optional direction

    Parameters
    ----------
    records : list of dict
        The dataset to query.
    command : str
        The SQL-like command string.

    Returns
    -------
    list of dict
        Query result set.
    """
    if not isinstance(records, list):
        raise ValueError("records must be a list of dictionaries")
    if not all(isinstance(r, dict) for r in records):
        raise ValueError("each record must be a dictionary")

    # 1. Parse SELECT
    m = _RE_SELECT.match(command)
    if not m:
        raise ValueError("SELECT clause is required")
    fields_part = m.group('fields').strip()
    select_fields = [f.strip() for f in fields_part.split(',')] if fields_part != '*' else ['*']

    remaining = command[m.end():]

    # 2. Parse optional WHERE
    where_cond = None
    m_where = _RE_WHERE.search(remaining)
    if m_where:
        where_cond = m_where.group('cond').strip()
        remaining = remaining[:m_where.start()] + remaining[m_where.end():]

    # 3. Parse optional ORDER BY
    order_field = None
    desc_order = False
    m_order = _RE_ORDER_BY.search(remaining)
    if m_order:
        order_field, desc_order = _parse_order_by(m_order.group(0))

    # 4. Filter records
    result = []
    for rec in records:
        try:
            if where_cond and not _evaluate_condition(rec, where_cond):
                continue
        except Exception as exc:
            raise ValueError(f"Error evaluating WHERE clause: {exc}")
        # Project fields
        if select_fields == ['*']:
            projected = dict(rec)
        else:
            try:
                projected = {field: rec[field] for field in select_fields}
            except KeyError as exc:
                raise ValueError(f"Field not found during SELECT projection: {exc}")
        result.append(projected)

    # 5. Sort if needed
    if order_field:
        if not all(order_field in r for r in result):
            raise ValueError(f"ORDER BY field '{order_field}' not present in all records")
        result.sort(key=lambda r: r[order_field], reverse=desc_order)

    return result