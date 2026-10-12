import re
import operator
from functools import reduce

# Map supported operators to the corresponding functions in the operator module.
OPERATORS = {
    "==": operator.eq,
    "!=": operator.ne,
    "<=": operator.le,
    ">=": operator.ge,
    "<": operator.lt,
    ">": operator.gt,
}

# Regular expression patterns for parsing the query components.
SELECT_RE = re.compile(r"^\s*SELECT\s+(?P<cols>[\*\w,\s]+)\s+WHERE\s+(?P<where>.+?)\s*(ORDER BY\s+(?P<order>\w+)(?:\s+(ASC|DESC))?)?\s*$",
                       re.IGNORECASE | re.DOTALL)

# Simple tokenizer for the WHERE clause.
WHERE_TOKEN_RE = re.compile(r"(?P<field>\w+)\s*(?P<op>==|!=|<=|>=|<|>)\s*(?P<value>'[^']*'|\"[^\"]*\"|\d+(\.\d+)?)\s*(?P<logic>AND)?", re.IGNORECASE)

def _parse_value(val: str):
    """Convert a string literal or numeric value into its Python representation."""
    if val.startswith(("'", '"')) and val.endswith(("'", '"')):
        return val[1:-1]
    try:
        if '.' in val:
            return float(val)
        return int(val)
    except ValueError:
        raise ValueError(f"Unable to parse value: {val}")

def _build_where_func(where_clause: str):
    """Create a function that evaluates whether a record satisfies the WHERE clause."""
    tokens = []
    pos = 0
    while pos < len(where_clause):
        match = WHERE_TOKEN_RE.match(where_clause, pos)
        if not match:
            raise ValueError(f"Invalid WHERE clause near: {where_clause[pos:]}")
        field = match.group("field")
        op_token = match.group("op")
        value_str = match.group("value")
        logic = match.group("logic")

        op_func = OPERATORS[op_token]
        value = _parse_value(value_str)

        def condition(record, field=field, op_func=op_func, value=value):
            return op_func(record.get(field), value)

        tokens.append(condition)
        if logic:
            # AND is the only logical operator supported.
            pos = match.end()
        else:
            break

    def where_func(record):
        return all(cond(record) for cond in tokens)

    return where_func

def _apply_order_by(records, column: str, direction: str):
    """Sort records by the specified column."""
    reverse = direction.upper() == "DESC"
    try:
        return sorted(records, key=lambda r: r.get(column), reverse=reverse)
    except TypeError:
        raise ValueError(f"Cannot sort by column '{column}' due to incomparable values")

def execute_user_query(records, user_query):
    """
    Execute a simple SQL-like query on the provided list of dictionary records.

    Parameters
    ----------
    records : list[dict]
        The dataset to query.
    user_query : str
        A SQL-like string supporting SELECT, WHERE and ORDER BY clauses.

    Returns
    -------
    list[dict]
        The filtered, projected, and optionally sorted result set.

    Raises
    ------
    ValueError
        If the query is malformed or cannot be executed.
    """
    if not isinstance(records, list) or any(not isinstance(r, dict) for r in records):
        raise ValueError("records must be a list of dictionaries")

    match = SELECT_RE.match(user_query)
    if not match:
        raise ValueError("Query does not conform to supported syntax")

    # Parse SELECT columns
    cols_str = match.group("cols").strip()
    if cols_str == "*":
        selected_cols = None  # indicates all columns
    else:
        selected_cols = [c.strip() for c in cols_str.split(",")]
        if not all(selected_cols):
            raise ValueError("Empty column names are not allowed")

    # Build WHERE function
    where_clause = match.group("where")
    if where_clause is None:
        raise ValueError("Missing WHERE clause")
    try:
        where_func = _build_where_func(where_clause)
    except ValueError as e:
        raise ValueError(f"Invalid WHERE clause: {e}") from None

    # Filter records
    filtered = [rec for rec in records if where_func(rec)]

    # Order by, if present
    order_col = match.group("order")
    order_dir = match.lastindex and "DESC" if match.group(4) else "ASC"
    if order_col:
        try:
            filtered = _apply_order_by(filtered, order_col, order_dir)
        except ValueError as e:
            raise ValueError(f"ORDER BY error: {e}") from None

    # Project columns
    if selected_cols is not None:
        projected = [{k: v for k, v in rec.items() if k in selected_cols} for rec in filtered]
    else:
        projected = filtered

    return projected