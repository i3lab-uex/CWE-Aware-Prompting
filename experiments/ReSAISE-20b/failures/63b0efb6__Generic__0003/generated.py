import re
import operator
from functools import reduce

# Supported binary operators for WHERE clause
OPERATORS = {
    '==': operator.eq,
    '=': operator.eq,
    '!=': operator.ne,
    '>=': operator.ge,
    '<=': operator.le,
    '>': operator.gt,
    '<': operator.lt
}

def _parse_where(condition: str):
    """Parse a simple condition of the form <field> <op> <value>."""
    pattern = r'^\s*(?P<field>\w+)\s*(?P<op>==|=|!=|>=|<=|>|<)\s*(?P<value>.+?)\s*$'
    m = re.match(pattern, condition)
    if not m:
        raise ValueError(f"Invalid WHERE clause: {condition!r}")

    field = m.group('field')
    op_str = m.group('op')
    value_raw = m.group('value').strip()

    # Try to interpret the literal value
    try:
        if re.match(r'^-?\d+$', value_raw):
            value = int(value_raw)
        elif re.match(r'^-?\d+\.\d*$', value_raw):
            value = float(value_raw)
        elif re.match(r"^'(.*)'$", value_raw) or re.match(r'^\"(.*)\"$', value_raw):
            # quoted string
            value = re.sub(r"^['\"]|['\"]$", "", value_raw)
        else:
            # treat as string
            value = value_raw
    except Exception:
        raise ValueError(f"Could not parse value in WHERE clause: {value_raw!r}")

    op_func = OPERATORS.get(op_str)
    if not op_func:
        raise ValueError(f"Unsupported operator in WHERE clause: {op_str!r}")

    return field, op_func, value

def _apply_where(records, condition):
    if not condition:
        return records
    field, op_func, value = _parse_where(condition)
    def matches(rec):
        if field not in rec:
            return False
        try:
            return op_func(rec[field], value)
        except Exception:
            return False
    return list(filter(matches, records))

def _apply_select(records, fields):
    if fields == ['*']:
        return records
    selected = []
    for rec in records:
        new_rec = {}
        for f in fields:
            if f not in rec:
                raise ValueError(f"Field {f!r} not found in record")
            new_rec[f] = rec[f]
        selected.append(new_rec)
    return selected

def _apply_order_by(records, order_clause):
    if not order_clause:
        return records
    # Support simple ORDER BY <field> [ASC|DESC]
    pattern = r'^\s*(?P<field>\w+)(?:\s+(?P<dir>ASC|DESC))?\s*$'
    m = re.match(pattern, order_clause, re.IGNORECASE)
    if not m:
        raise ValueError(f"Invalid ORDER BY clause: {order_clause!r}")
    field = m.group('field')
    direction = m.group('dir') or 'ASC'
    reverse = direction.upper() == 'DESC'
    try:
        return sorted(records, key=lambda r: r[field], reverse=reverse)
    except KeyError:
        raise ValueError(f"Field {field!r} not found for ORDER BY")
    except TypeError:
        # Uncomparable types
        raise ValueError(f"Field {field!r} contains unorderable values")

def run_sql_query(records, command):
    """
    Execute a basic SQL-like SELECT query on a list of dictionaries.

    Parameters
    ----------
    records : list[dict]
        The data to query.
    command : str
        A SQL-like statement supporting SELECT, WHERE, and ORDER BY.

    Returns
    -------
    list[dict]
        The query result.

    Raises
    ------
    ValueError
        If the command is malformed or cannot be executed.
    """
    if not isinstance(records, list):
        raise ValueError("records must be a list of dictionaries")
    if not all(isinstance(r, dict) for r in records):
        raise ValueError("All items in records must be dictionaries")

    # Basic regex to split SELECT, WHERE, ORDER BY
    select_pattern = r'^\s*SELECT\s+(?P<fields>.+?)\s*(?:WHERE|ORDER BY|$)'
    where_pattern = r'\bWHERE\s+(?P<cond>.+?)\s*(?:ORDER BY|$)'
    order_pattern = r'\bORDER\s+BY\s+(?P<order>.+?)\s*$'

    # Parse SELECT fields
    m_select = re.search(select_pattern, command, re.IGNORECASE)
    if not m_select:
        raise ValueError("SELECT clause missing or malformed")
    fields_str = m_select.group('fields')
    fields = [f.strip() for f in fields_str.split(',')]
    if not all(fields):
        raise ValueError("Empty field name detected")

    # Parse WHERE clause
    m_where = re.search(where_pattern, command, re.IGNORECASE)
    where_cond = m_where.group('cond') if m_where else None

    # Parse ORDER BY clause
    m_order = re.search(order_pattern, command, re.IGNORECASE)
    order_clause = m_order.group('order') if m_order else None

    # Apply query steps
    result = _apply_where(records, where_cond)
    result = _apply_select(result, fields)
    result = _apply_order_by(result, order_clause)

    return result