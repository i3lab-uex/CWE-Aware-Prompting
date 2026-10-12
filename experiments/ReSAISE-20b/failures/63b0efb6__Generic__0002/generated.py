import re
import operator
from functools import reduce

def run_sql_query(records, command):
    """
    Execute a simple SQL‑like query on a list of dictionaries.

    Parameters
    ----------
    records : list[dict]
        The dataset to query.
    command : str
        SQL‑like statement supporting SELECT, WHERE and ORDER BY.

    Returns
    -------
    list[dict]
        Result set after applying the query.

    Raises
    ------
    ValueError
        If the command is malformed or cannot be executed.
    """
    if not isinstance(records, list) or any(not isinstance(r, dict) for r in records):
        raise ValueError("records must be a list of dictionaries")

    # Regular expression for the supported syntax
    sql_re = re.compile(
        r"""
        ^\s*SELECT\s+
        (?P<fields>[\w\*,\s]+)           # column list or *
        (?:\s+WHERE\s+(?P<where>[^ORDER]+))?
        (?:\s+ORDER\s+BY\s+(?P<order>\w+)(?:\s+(ASC|DESC))?)?
        \s*$
        """,
        re.IGNORECASE | re.VERBOSE
    )

    match = sql_re.match(command)
    if not match:
        raise ValueError("Invalid query syntax")

    fields_str = match.group('fields').strip()
    where_clause = match.group('where')
    order_by_field = match.group('order')
    order_dir = match.lastindex and (match.captures(3)[0] if match.group(3) else None)

    # Resolve fields
    if fields_str == '*':
        selected_fields = None  # means all fields
    else:
        selected_fields = [f.strip() for f in fields_str.split(',')]
        if not all(selected_fields):
            raise ValueError("Empty field name detected")

    # Filter records
    def _eval_where(rec):
        if not where_clause:
            return True
        # Very simple condition: field operator value (no AND/OR)
        cond_re = re.compile(r'(?P<field>\w+)\s*(?P<op>[<>]=?|==|!=)\s*(?P<value>.+)', re.IGNORECASE)
        cond_match = cond_re.match(where_clause.strip())
        if not cond_match:
            raise ValueError("Unsupported WHERE clause")

        field = cond_match.group('field')
        op_sym = cond_match.group('op')
        val_raw = cond_match.group('value').strip()

        # Parse value: int, float or string literal
        if (val_raw.startswith("'") and val_raw.endswith("'")) or \
           (val_raw.startswith('"') and val_raw.endswith('"')):
            value = val_raw[1:-1]
        else:
            try:
                if '.' in val_raw:
                    value = float(val_raw)
                else:
                    value = int(val_raw)
            except ValueError:
                raise ValueError(f"Unsupported literal: {val_raw}")

        # Retrieve record value
        rec_value = rec.get(field)
        if rec_value is None:
            return False

        ops_map = {
            '>': operator.gt,
            '<': operator.lt,
            '>=': operator.ge,
            '<=': operator.le,
            '==': operator.eq,
            '=': operator.eq,
            '!=': operator.ne
        }
        op_func = ops_map.get(op_sym)
        if not op_func:
            raise ValueError(f"Unsupported operator: {op_sym}")

        try:
            return op_func(rec_value, value)
        except TypeError:
            # Incomparable types
            return False

    filtered = list(filter(_eval_where, records))

    # Order by
    if order_by_field:
        reverse = (order_dir and order_dir.upper() == 'DESC')
        try:
            filtered.sort(key=lambda r: r.get(order_by_field), reverse=reverse)
        except TypeError as exc:
            raise ValueError(f"Cannot order by field '{order_by_field}': {exc}")

    # Project fields
    if selected_fields is None:
        result = [dict(r) for r in filtered]
    else:
        result = []
        for rec in filtered:
            proj = {}
            for f in selected_fields:
                if f not in rec:
                    raise ValueError(f"Field '{f}' not found in record")
                proj[f] = rec[f]
            result.append(proj)

    return result