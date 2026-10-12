import re
import operator
from functools import reduce

# Mapping of supported comparison operators to functions
_OPERATOR_MAP = {
    '=': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,
    '<': operator.lt,
    '>': operator.gt,
    '<=': operator.le,
    '>=': operator.ge,
}

# Supported logical operators
_LOGICAL_OPS = {
    'AND': lambda a, b: a and b,
    'OR':  lambda a, b: a or b,
}

def _parse_select_clause(select_part):
    """Parse the SELECT clause and return a list of columns."""
    select_part = select_part.strip()
    if select_part == '*':
        return ['*']
    cols = [c.strip() for c in select_part.split(',')]
    if not all(cols):
        raise ValueError('Empty column name in SELECT clause')
    return cols

def _parse_where_clause(where_part):
    """
    Very simple parser that supports a single condition of the form:
        column operator value
    where value can be a number or a quoted string.
    """
    where_part = where_part.strip()
    # Regex to capture column, operator and value
    pattern = r'(?P<col>\w+)\s*(?P<op>=|!=|<>|<=|>=|<|>)\s*(?P<val>.+)'
    m = re.match(pattern, where_part)
    if not m:
        raise ValueError('Invalid WHERE clause')
    col = m.group('col')
    op_str = m.group('op')
    val_raw = m.group('val').strip()

    # Interpret value: int, float or string literal
    if (val_raw.startswith("'") and val_raw.endswith("'")) or \
       (val_raw.startswith('"') and val_raw.endswith('"')):
        val = val_raw[1:-1]
    else:
        try:
            if '.' in val_raw:
                val = float(val_raw)
            else:
                val = int(val_raw)
        except ValueError:
            # Treat as string if not a number
            val = val_raw

    comp_op = _OPERATOR_MAP.get(op_str)
    if not comp_op:
        raise ValueError(f'Unsupported operator {op_str}')

    def predicate(record):
        try:
            record_val = record[col]
        except KeyError:
            return False
        return comp_op(record_val, val)

    return predicate

def _parse_order_by_clause(order_part):
    """
    Parse ORDER BY clause: column [ASC|DESC]
    Returns a tuple (column, reverse_bool)
    """
    order_part = order_part.strip()
    parts = order_part.split()
    if not parts:
        raise ValueError('Empty ORDER BY clause')
    col = parts[0]
    reverse = False
    if len(parts) > 1:
        direction = parts[1].upper()
        if direction == 'DESC':
            reverse = True
        elif direction != 'ASC':
            raise ValueError('ORDER BY direction must be ASC or DESC')
    return col, reverse

def submit_user_query(records, sql_statement):
    """
    Execute a simple SQL-like query on a list of dictionaries.

    Supported syntax:
        SELECT <columns> [WHERE <condition>] [ORDER BY <column> [ASC|DESC]]
    """
    if not isinstance(records, list):
        raise ValueError('records must be a list')
    for rec in records:
        if not isinstance(rec, dict):
            raise ValueError('Each record must be a dictionary')

    sql_statement = sql_statement.strip()
    if not sql_statement:
        raise ValueError('Empty SQL statement')

    # Regex to capture SELECT, optional WHERE and ORDER BY
    pattern = r"""
        ^SELECT\s+(?P<select>.+?)
        (?:\s+WHERE\s+(?P<where>.+?))?
        (?:\s+ORDER\s+BY\s+(?P<order>.+?))?
        \s*$
    """
    m = re.match(pattern, sql_statement, re.IGNORECASE | re.VERBOSE)
    if not m:
        raise ValueError('Invalid SQL statement format')

    # SELECT
    select_part = m.group('select')
    selected_columns = _parse_select_clause(select_part)

    # WHERE
    where_part = m.group('where')
    if where_part:
        predicate = _parse_where_clause(where_part)
    else:
        predicate = lambda r: True

    # ORDER BY
    order_part = m.group('order')
    if order_part:
        order_col, reverse = _parse_order_by_clause(order_part)
    else:
        order_col, reverse = None, False

    # Filter records
    try:
        filtered = [rec for rec in records if predicate(rec)]
    except Exception as e:
        raise ValueError(f'Error evaluating WHERE clause: {e}')

    # Order records
    if order_col:
        try:
            filtered.sort(key=lambda r: r.get(order_col, None), reverse=reverse)
        except Exception as e:
            raise ValueError(f'Error ordering by column {order_col}: {e}')

    # Project selected columns
    result = []
    for rec in filtered:
        if selected_columns == ['*']:
            projected = dict(rec)
        else:
            projected = {col: rec.get(col, None) for col in selected_columns}
        result.append(projected)

    return result