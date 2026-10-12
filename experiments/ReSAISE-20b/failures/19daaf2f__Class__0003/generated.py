import re
import operator
from functools import reduce

# Map string operators to actual Python functions
_COMPARISONS = {
    '=': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,
    '>': operator.gt,
    '>=': operator.ge,
    '<': operator.lt,
    '<=': operator.le
}

_LOGICAL = {
    'AND': lambda a, b: a and b,
    'OR': lambda a, b: a or b
}

def _parse_select(select_part):
    """
    Parse the SELECT clause and return a list of column names.
    '*' means all columns.
    """
    select_part = select_part.strip()
    if not select_part:
        raise ValueError("SELECT clause cannot be empty")
    if select_part == '*':
        return ['*']
    columns = [col.strip() for col in select_part.split(',')]
    if not all(columns):
        raise ValueError("SELECT clause contains empty column name")
    return columns

def _parse_where(where_part):
    """
    Very small subset parser for WHERE clause.
    Supports expressions like:
        column operator value [AND|OR ...]
    Values are assumed to be quoted strings or numeric literals.
    """
    if not where_part:
        return lambda row: True

    tokens = re.findall(r"(\w+|\S)", where_part)
    if not tokens:
        raise ValueError("Malformed WHERE clause")

    def build_expr(tokens):
        # Recursive descent: parse left operand, operator, right operand
        if len(tokens) < 3:
            raise ValueError("Incomplete WHERE expression")
        col, op_sym, val = tokens[0], tokens[1], tokens[2]
        if op_sym not in _COMPARISONS:
            raise ValueError(f"Unsupported operator '{op_sym}' in WHERE clause")
        # Convert value
        if (val.startswith("'") and val.endswith("'")) or (val.startswith('"') and val.endswith('"')):
            val = val[1:-1]
        else:
            try:
                if '.' in val:
                    val = float(val)
                else:
                    val = int(val)
            except ValueError:
                pass  # keep as string

        comp_func = _COMPARISONS[op_sym]
        left_expr = lambda row: comp_func(row.get(col), val)

        # Handle AND/OR
        if len(tokens) > 3:
            op = tokens[3].upper()
            if op not in _LOGICAL:
                raise ValueError(f"Unsupported logical operator '{op}'")
            right_expr = build_expr(tokens[4:])
            return lambda row: _LOGICAL[op](left_expr(row), right_expr(row))
        else:
            return left_expr

    expr_func = build_expr(tokens)
    return expr_func

def _parse_order_by(order_part):
    """
    Parse ORDER BY clause. Returns list of (column, direction) tuples.
    """
    if not order_part:
        return []
    parts = [p.strip() for p in order_part.split(',')]
    result = []
    for part in parts:
        if not part:
            continue
        tokens = part.split()
        col = tokens[0]
        direction = 'ASC'
        if len(tokens) > 1:
            dir_token = tokens[1].upper()
            if dir_token in ('ASC', 'DESC'):
                direction = dir_token
            else:
                raise ValueError(f"Invalid ORDER BY direction '{dir_token}'")
        result.append((col, direction))
    return result

def run_sql_query(dataset, sql_query):
    """
    Execute a simple SQL-like query on a list of dictionaries.

    Parameters
    ----------
    dataset : list[dict]
        The data to query.
    sql_query : str
        Query string containing SELECT, WHERE and ORDER BY clauses.

    Returns
    -------
    list[dict]
        The resulting records.

    Raises
    ------
    ValueError
        If the query is malformed or execution fails.
    """
    if not isinstance(dataset, list):
        raise ValueError("Dataset must be a list of dictionaries")
    if not all(isinstance(r, dict) for r in dataset):
        raise ValueError("All items in dataset must be dictionaries")

    # Normalize query
    q = sql_query.strip().rstrip(';')
    if not q:
        raise ValueError("Empty query")

    # Regex to capture SELECT, WHERE, ORDER BY
    pattern = re.compile(
        r"SELECT\s+(?P<select>.+?)"
        r"(?:\s+WHERE\s+(?P<where>.*?))?"
        r"(?:\s+ORDER\s+BY\s+(?P<order>.+))?$",
        re.IGNORECASE | re.DOTALL
    )
    match = pattern.match(q)
    if not match:
        raise ValueError("Query must contain a SELECT clause")

    select_part = match.group('select')
    where_part = match.group('where') or ''
    order_part = match.group('order') or ''

    # Parse clauses
    selected_columns = _parse_select(select_part)
    where_func = _parse_where(where_part)
    order_by = _parse_order_by(order_part)

    # Filter rows
    try:
        filtered = [row for row in dataset if where_func(row)]
    except Exception as e:
        raise ValueError(f"Error evaluating WHERE clause: {e}") from e

    # Order rows
    if order_by:
        try:
            def sort_key(row):
                key = []
                for col, dir in order_by:
                    val = row.get(col)
                    # None values are placed at the end
                    key.append((val is None, val))
                return tuple(key)

            reverse = any(dir == 'DESC' for _, dir in order_by)
            filtered.sort(key=sort_key, reverse=reverse)
        except Exception as e:
            raise ValueError(f"Error in ORDER BY clause: {e}") from e

    # Project columns
    if selected_columns == ['*']:
        result = filtered
    else:
        try:
            result = [{col: row.get(col) for col in selected_columns} for row in filtered]
        except Exception as e:
            raise ValueError(f"Error selecting columns: {e}") from e

    return result