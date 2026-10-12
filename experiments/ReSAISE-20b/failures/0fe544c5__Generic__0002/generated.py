import re
import operator
from functools import reduce

# Supported comparison operators mapped to functions
CMP_OPS = {
    "=": operator.eq,
    "!=": operator.ne,
    "<": operator.lt,
    "<=": operator.le,
    ">": operator.gt,
    ">=": operator.ge
}

# Supported logical operators mapped to functions
LOG_OPS = {
    "AND": lambda a, b: a and b,
    "OR": lambda a, b: a or b
}

def _parse_select_clause(sql):
    """Return list of fields to select."""
    match = re.search(r"SELECT\s+(.*?)\s+WHERE", sql, re.IGNORECASE | re.DOTALL)
    if not match:
        # maybe no WHERE
        match = re.search(r"SELECT\s+(.*?)\s+ORDER BY", sql, re.IGNORECASE | re.DOTALL)
    if not match:
        match = re.search(r"SELECT\s+(.*?)(\s+FROM|\s*$)", sql, re.IGNORECASE | re.DOTALL)
    if not match:
        raise ValueError("SELECT clause malformed.")
    fields = [f.strip() for f in match.group(1).split(",")]
    return fields

def _parse_where_clause(sql):
    """Return a function that evaluates the WHERE condition for a record."""
    where_match = re.search(r"WHERE\s+(.*?)\s*(ORDER BY|$)", sql, re.IGNORECASE | re.DOTALL)
    if not where_match:
        return lambda record: True  # no condition
    expr = where_match.group(1).strip()

    # Tokenize the expression (field, operator, value) separated by logical ops
    tokens = re.split(r"\s+(AND|OR)\s+", expr, flags=re.IGNORECASE)
    if len(tokens) == 1:
        # single condition
        cond = tokens[0]
        return _build_cond_func(cond)
    else:
        # multiple conditions with logical operators
        cond_funcs = []
        ops = []
        for i, token in enumerate(tokens):
            if i % 2 == 0:
                cond_funcs.append(_build_cond_func(token))
            else:
                ops.append(token.upper())
        def combined(record):
            result = cond_funcs[0](record)
            for op, func in zip(ops, cond_funcs[1:]):
                result = LOG_OPS[op](result, func(record))
            return result
        return combined

def _build_cond_func(cond_str):
    """Build a single condition function."""
    pattern = r"(?P<field>\w+)\s*(?P<op>=|!=|<=|<|>=|>)\s*'?(?P<value>[^']+)'\s*$"
    m = re.match(pattern, cond_str.strip())
    if not m:
        raise ValueError(f"Invalid condition: {cond_str}")
    field = m.group("field")
    op = m.group("op")
    val_raw = m.group("value")

    cmp_func = CMP_OPS[op]
    # Try to interpret value as int or float, else keep string
    try:
        if '.' in val_raw:
            value = float(val_raw)
        else:
            value = int(val_raw)
    except ValueError:
        value = val_raw

    def func(record):
        record_val = record.get(field)
        if isinstance(record_val, str) and isinstance(value, (int, float)):
            try:
                record_val = int(record_val)
            except ValueError:
                pass
        return cmp_func(record_val, value)

    return func

def _parse_order_by_clause(sql):
    """Return a list of (field, ascending) tuples."""
    order_match = re.search(r"ORDER BY\s+(.*?)(\s+WHERE|\s*$)", sql, re.IGNORECASE | re.DOTALL)
    if not order_match:
        return []
    order_str = order_match.group(1).strip()
    fields = [f.strip() for f in order_str.split(",")]
    result = []
    for field in fields:
        parts = field.split()
        if len(parts) == 2 and parts[1].upper() in ("ASC", "DESC"):
            ascending = parts[1].upper() == "ASC"
        else:
            ascending = True
        result.append((parts[0], ascending))
    return result

def handle_sql_query(records, sql_command):
    """
    Execute a simple SQL-like query on a list of record dictionaries.

    Parameters
    ----------
    records : List[Dict[str, Any]]
        Input dataset.
    sql_command : str
        SQL-like query string.

    Returns
    -------
    List[Dict[str, Any]]
        Resulting records after SELECT, WHERE and ORDER BY.

    Raises
    ------
    ValueError
        If the query cannot be parsed or executed.
    """
    if not isinstance(records, list) or not all(isinstance(r, dict) for r in records):
        raise ValueError("Records must be a list of dictionaries.")
    if not isinstance(sql_command, str):
        raise ValueError("SQL command must be a string.")

    try:
        fields = _parse_select_clause(sql_command)
        where_func = _parse_where_clause(sql_command)
        order_by = _parse_order_by_clause(sql_command)

        # Filter
        filtered = [rec for rec in records if where_func(rec)]

        # Select fields
        selected = []
        for rec in filtered:
            if fields == ["*"]:
                selected.append(rec.copy())
            else:
                new_rec = {f: rec.get(f) for f in fields}
                selected.append(new_rec)

        # Order by
        if order_by:
            def sort_key(rec):
                key = []
                for field, asc in order_by:
                    val = rec.get(field)
                    # None values are considered smallest
                    key.append((val is not None, val) if asc else (val is None, -float('inf') if isinstance(val, (int, float)) else val))
                return key
            selected.sort(key=sort_key)

        return selected

    except Exception as e:
        raise ValueError(f"Failed to execute query: {e}") from e