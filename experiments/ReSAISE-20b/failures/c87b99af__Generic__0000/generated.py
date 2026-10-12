import re
import operator
from functools import partial

# Supported binary operators for WHERE clauses.
OPERATORS = {
    '=': operator.eq,
    '==': operator.eq,
    '<>': operator.ne,
    '!=': operator.ne,
    '>': operator.gt,
    '>=': operator.ge,
    '<': operator.lt,
    '<=': operator.le
}

# Regular expression to parse a very small subset of SQL.
QUERY_RE = re.compile(
    r"""
    ^\s*SELECT\s+(?P<fields>[\*\w,\s]+?)          # SELECT fields
    \s+FROM\s+\w+                                # FROM table_name (ignored)
    (\s+WHERE\s+(?P<where>.+?))?                # optional WHERE
    (\s+ORDER\s+BY\s+(?P<order>\w+\s*(?:,|\s)+\w*))? # optional ORDER BY
    \s*;?\s*$                                    # optional trailing semicolon
    """,
    re.IGNORECASE | re.VERBOSE,
)

# Regular expression to split a simple condition into field, operator, value.
COND_RE = re.compile(
    r"""
    (?P<field>\w+)\s*
    (?P<op>=|==|<>|!=|>|>=|<|<=)\s*
    (?P<value>
        (?:'[^']*') |     # single quoted string
        (?:"[^"]*") |     # double quoted string
        (?:\d+\.\d+|\d+)   # number
    )
    """,
    re.VERBOSE,
)

def _parse_value(val: str):
    """Convert a string literal to its Python value."""
    val = val.strip()
    if (val.startswith("'") and val.endswith("'")) or (
        val.startswith('"') and val.endswith('"')
    ):
        return val[1:-1]
    try:
        if '.' in val:
            return float(val)
        return int(val)
    except ValueError:
        raise ValueError(f"Unsupported literal: {val}")

def _build_where_func(where_clause: str):
    """Return a function that evaluates the WHERE clause for a record."""
    # For simplicity, only support conjunctions of simple comparisons
    # separated by AND/OR (case-insensitive). No parentheses.
    tokens = re.split(r'\s+(AND|OR)\s+', where_clause, flags=re.IGNORECASE)
    if not tokens:
        raise ValueError("Empty WHERE clause")

    funcs = []
    connectors = []

    for i, token in enumerate(tokens):
        if i % 2 == 0:
            # Condition
            m = COND_RE.fullmatch(token.strip())
            if not m:
                raise ValueError(f"Invalid condition: {token}")
            field = m.group('field')
            op_str = m.group('op')
            value = _parse_value(m.group('value'))
            op_func = OPERATORS[op_str]
            funcs.append(partial(op_func, value=value))
        else:
            connectors.append(token.upper())

    def where(record):
        result = funcs[0](record.get(tokens[0].split()[0]))
        for op, func in zip(connectors, funcs[1:]):
            if op == 'AND':
                result = result and func(record.get(tokens[0].split()[0]))
            else:  # OR
                result = result or func(record.get(tokens[0].split()[0]))
        return result

    return where

def execute_user_query(records, user_query):
    """
    Execute a very small subset of SQL on a list of dictionary records.

    Parameters
    ----------
    records : list[dict]
        Dataset to query.
    user_query : str
        SQL-like string (SELECT, WHERE, ORDER BY).

    Returns
    -------
    list[dict]
        Query result.

    Raises
    ------
    ValueError
        If query syntax is invalid or evaluation fails.
    """
    if not isinstance(records, list) or any(not isinstance(r, dict) for r in records):
        raise ValueError("records must be a list of dictionaries")

    m = QUERY_RE.fullmatch(user_query)
    if not m:
        raise ValueError("Query format is invalid")

    fields = [f.strip() for f in m.group('fields').split(',')] if m.group('fields') != '*' else None
    where_clause = m.group('where')
    order_by_clause = m.group('order')

    # Apply WHERE
    filtered = records
    if where_clause:
        try:
            where_func = _build_where_func(where_clause)
            filtered = [rec for rec in records if where_func(rec)]
        except Exception as exc:
            raise ValueError(f"WHERE clause evaluation error: {exc}") from exc

    # Apply SELECT
    if fields:
        result = []
        for rec in filtered:
            try:
                projected = {field: rec[field] for field in fields}
            except KeyError as exc:
                raise ValueError(f"Field not found: {exc}") from exc
            result.append(projected)
    else:
        result = filtered

    # Apply ORDER BY
    if order_by_clause:
        order_fields = [f.strip() for f in re.split(r',\s*|\s+', order_by_clause) if f]
        try:
            result.sort(key=lambda r: tuple(r[field] for field in order_fields))
        except KeyError as exc:
            raise ValueError(f"Order by field not found: {exc}") from exc

    return result