import re
import operator
from functools import cmp_to_key

# Mapping of supported comparison operators to functions
OP_MAP = {
    '=': operator.eq,
    '!=': operator.ne,
    '<': operator.lt,
    '<=': operator.le,
    '>': operator.gt,
    '>=': operator.ge,
}

# Regex patterns for parsing the SQL-like statement
SELECT_RE = re.compile(r"^\s*SELECT\s+(?P<fields>[\w\*,\s]+)\s+FROM\s+\w+", re.IGNORECASE)
WHERE_RE = re.compile(
    r"WHERE\s+(?P<field>\w+)\s*(?P<op>=|!=|<=|>=|<|>)\s*(?P<value>.+)", re.IGNORECASE)
ORDER_RE = re.compile(
    r"ORDER\s+BY\s+(?P<field>\w+)(?:\s+(?P<direction>ASC|DESC))?", re.IGNORECASE)


def _parse_value(val: str):
    """Parse a value literal into int, float or string."""
    val = val.strip()
    # String literals may be quoted
    if (val.startswith("'") and val.endswith("'")) or (
        val.startswith('"') and val.endswith('"')
    ):
        return val[1:-1]
    # Try int
    try:
        return int(val)
    except ValueError:
        pass
    # Try float
    try:
        return float(val)
    except ValueError:
        pass
    # As is (unquoted string)
    return val


def submit_user_query(records, sql_statement):
    """
    Execute a simple SQL-like query on the provided list of record dictionaries.

    Supported clauses:
        SELECT <fields> FROM <table>
        WHERE <field> <op> <value>
        ORDER BY <field> [ASC|DESC]

    Parameters
    ----------
    records : list[dict]
        List of record dictionaries to query.
    sql_statement : str
        SQL-like statement string.

    Returns
    -------
    list[dict]
        Query result as a list of dictionaries.

    Raises
    ------
    ValueError
        If the query format is invalid or execution fails.
    """
    if not isinstance(records, list) or any(
        not isinstance(r, dict) for r in records
    ):
        raise ValueError("Records must be a list of dictionaries.")

    # 1. Parse SELECT clause
    m = SELECT_RE.search(sql_statement)
    if not m:
        raise ValueError("Invalid or missing SELECT clause.")
    fields_str = m.group('fields').strip()
    if fields_str == '*':
        selected_fields = None  # all fields
    else:
        selected_fields = [f.strip() for f in fields_str.split(',')]
        if not all(selected_fields):
            raise ValueError("Empty field names in SELECT clause.")

    # 2. Parse WHERE clause (optional)
    where_func = None
    m_where = WHERE_RE.search(sql_statement)
    if m_where:
        field = m_where.group('field')
        op_str = m_where.group('op')
        value_raw = m_where.group('value')

        if op_str not in OP_MAP:
            raise ValueError(f"Unsupported operator '{op_str}' in WHERE clause.")
        op_func = OP_MAP[op_str]
        value = _parse_value(value_raw)

        def where_func(rec):
            try:
                return op_func(rec.get(field), value)
            except Exception as e:
                raise ValueError(f"Error evaluating WHERE clause: {e}")

    # 3. Parse ORDER BY clause (optional)
    order_field = None
    reverse = False
    m_order = ORDER_RE.search(sql_statement)
    if m_order:
        order_field = m_order.group('field')
        direction = m_order.group('direction')
        if direction and direction.upper() == 'DESC':
            reverse = True

    # 4. Apply filtering
    filtered = []
    for rec in records:
        try:
            if where_func is None or where_func(rec):
                filtered.append(rec)
        except Exception as e:
            raise ValueError(f"Error applying WHERE clause: {e}")

    # 5. Apply ordering
    if order_field:
        try:
            filtered.sort(key=lambda r: r.get(order_field), reverse=reverse)
        except Exception as e:
            raise ValueError(f"Error applying ORDER BY: {e}")

    # 6. Project selected fields
    result = []
    for rec in filtered:
        if selected_fields is None:
            result.append(rec.copy())
        else:
            projected = {}
            for f in selected_fields:
                if f not in rec:
                    raise ValueError(f"Field '{f}' does not exist in record.")
                projected[f] = rec[f]
            result.append(projected)

    return result