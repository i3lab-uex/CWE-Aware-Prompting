import re
import operator
from functools import reduce

# Allowed comparison operators
_COMPARISONS = {
    "==": operator.eq,
    "=": operator.eq,
    "!=": operator.ne,
    "<>": operator.ne,
    "<=": operator.le,
    ">=": operator.ge,
    "<": operator.lt,
    ">": operator.gt,
}

# Regex to parse a very small subset of SQL-like syntax
_QUERY_RE = re.compile(
    r"""
    ^\s*SELECT\s+(?P<fields>[\*\w,\s]+?)          # SELECT fields
    (?:\s+WHERE\s+(?P<where>.+?))?               # optional WHERE
    (?:\s+ORDER\s+BY\s+(?P<orderby>\w+)(?:\s+(?P<orderdir>ASC|DESC))?)?
    \s*$
    """,
    re.IGNORECASE | re.VERBOSE,
)

def _parse_condition(cond_str):
    """
    Parse a simple condition string into a callable that accepts a record.
    Supports only comparisons of the form <field> <op> <value>.
    """
    parts = cond_str.strip().split()
    if len(parts) != 3:
        raise ValueError(f"Unsupported WHERE clause: {cond_str!r}")

    field, op_token, value_raw = parts

    if op_token not in _COMPARISONS:
        raise ValueError(f"Unsupported operator {op_token!r} in WHERE clause")

    # Try to interpret the value as int/float or keep as string
    try:
        if '.' in value_raw:
            value = float(value_raw)
        else:
            value = int(value_raw)
    except ValueError:
        # strip surrounding quotes if present
        if (value_raw.startswith("'") and value_raw.endswith("'")) or \
           (value_raw.startswith('"') and value_raw.endswith('"')):
            value = value_raw[1:-1]
        else:
            value = value_raw

    comp_func = _COMPARISONS[op_token]

    def condition(record):
        if field not in record:
            raise ValueError(f"Field {field!r} does not exist in the record")
        return comp_func(record[field], value)

    return condition

def run_sql_query(records, command):
    """
    Execute a very small subset of SQL-like commands on an in-memory list
    of dictionaries.

    Parameters
    ----------
    records : list[dict]
        The data set.
    command : str
        The SQL-like query string.

    Returns
    -------
    list[dict]
        Resulting records after applying SELECT, WHERE and ORDER BY.

    Raises
    ------
    ValueError
        If the query is malformed or contains unsupported features.
    """
    if not isinstance(records, list):
        raise ValueError("records must be a list of dictionaries")
    if not all(isinstance(r, dict) for r in records):
        raise ValueError("each record must be a dictionary")

    match = _QUERY_RE.match(command)
    if not match:
        raise ValueError("Query syntax is invalid or unsupported")

    fields_str = match.group('fields').strip()
    where_clause = match.group('where')
    orderby_field = match.group('orderby')
    orderdir = match.group('orderdir')

    # SELECT fields
    if fields_str == '*':
        selected_fields = None  # means all
    else:
        selected_fields = [f.strip() for f in fields_str.split(',')]
        # validate that all fields exist in at least one record
        if records:
            for f in selected_fields:
                if not any(f in r for r in records):
                    raise ValueError(f"Field {f!r} not found in any record")

    # WHERE
    if where_clause:
        condition = _parse_condition(where_clause)
        filtered_records = [r for r in records if condition(r)]
    else:
        filtered_records = list(records)

    # ORDER BY
    if orderby_field:
        reverse = (orderdir or 'ASC').upper() == 'DESC'
        try:
            filtered_records.sort(key=lambda r: r[orderby_field], reverse=reverse)
        except KeyError:
            raise ValueError(f"ORDER BY field {orderby_field!r} not found in records")

    # Projection
    if selected_fields is None:
        result = [dict(r) for r in filtered_records]
    else:
        result = [{k: v for k, v in r.items() if k in selected_fields} for r in filtered_records]

    return result