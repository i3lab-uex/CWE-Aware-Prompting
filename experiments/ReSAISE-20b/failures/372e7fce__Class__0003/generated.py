import re
from operator import eq, ne, lt, le, gt, ge
from functools import reduce

# Mapping of comparison operators to functions
_OPS = {
    '=': eq,
    '!=': ne,
    '<': lt,
    '<=': le,
    '>': gt,
    '>=': ge,
}

# Allowed logical operators
_LOGICAL_OPS = {'AND', 'OR'}

def _parse_query(sql: str):
    """
    Very small SQL‑like parser that extracts SELECT, WHERE and ORDER BY clauses.
    The query syntax is limited to:
        SELECT <columns>
        [WHERE <condition>]
        [ORDER BY <column> [ASC|DESC]]
    """
    # Normalize whitespace
    sql = re.sub(r'\s+', ' ', sql.strip())

    select_match = re.match(r'^SELECT\s+(?P<select>.+?)\s*(WHERE|ORDER BY|$)', sql, re.IGNORECASE)
    if not select_match:
        raise ValueError("Query must start with SELECT")
    select_part = select_match.group('select')

    # Find WHERE clause
    where_match = re.search(r'\bWHERE\b\s+(?P<where>.+?)\s*(ORDER BY|$)', sql, re.IGNORECASE)
    where_part = where_match.group('where') if where_match else None

    # Find ORDER BY clause
    order_match = re.search(r'\bORDER\s+BY\b\s+(?P<order>.+)$', sql, re.IGNORECASE)
    order_part = order_match.group('order') if order_match else None

    return select_part, where_part, order_part


def _evaluate_condition(record: dict, condition: str):
    """
    Evaluate a simple condition of the form:
        field <operator> value
    Supports =, !=, <, <=, >, >= and string/number literals.
    """
    # Split on first occurrence of an operator
    op_pattern = r'(<=|>=|!=|=|<|>)'
    parts = re.split(op_pattern, condition)
    if len(parts) != 3:
        raise ValueError(f"Unsupported condition format: {condition}")

    field, op_str, value_raw = parts[0].strip(), parts[1], parts[2].strip()

    if field not in record:
        raise ValueError(f"Field '{field}' not found in record")

    op_func = _OPS.get(op_str)
    if not op_func:
        raise ValueError(f"Unsupported operator '{op_str}'")

    # Try to interpret value as int or float, otherwise strip quotes
    if re.match(r'^-?\d+(\.\d+)?$', value_raw):
        try:
            if '.' in value_raw:
                value = float(value_raw)
            else:
                value = int(value_raw)
        except ValueError:
            raise ValueError(f"Invalid numeric literal: {value_raw}")
    else:
        # Remove surrounding quotes if present
        value = re.sub(r"^(['\"])(.*)\1$", r'\2', value_raw)

    return op_func(record[field], value)


def _apply_ordering(rows, order_part: str):
    """
    Order rows by a single column optionally with ASC/DESC.
    """
    parts = order_part.split()
    if not parts:
        return rows

    col = parts[0]
    direction = parts[1].upper() if len(parts) > 1 else 'ASC'

    reverse = direction == 'DESC'
    try:
        return sorted(rows, key=lambda r: r.get(col), reverse=reverse)
    except TypeError as exc:
        raise ValueError(f"Cannot order by column '{col}': {exc}") from exc


def execute_query_cmd(dataset_list, sql_query):
    """
    Execute a very limited SQL‑like query on an in‑memory dataset.

    Parameters
    ----------
    dataset_list : list[dict]
        The data to query.
    sql_query : str
        Query string.

    Returns
    -------
    list[dict]
        Resulting rows after applying SELECT, WHERE and ORDER BY.

    Raises
    ------
    ValueError
        If the query is malformed or cannot be executed.
    """
    if not isinstance(dataset_list, list):
        raise ValueError("dataset_list must be a list")
    if not isinstance(sql_query, str):
        raise ValueError("sql_query must be a string")

    select_part, where_part, order_part = _parse_query(sql_query)

    # Resolve selected columns
    if select_part.strip() == '*':
        selected_cols = None  # means all columns
    else:
        selected_cols = [c.strip() for c in select_part.split(',')]
        # Validate column names
        if dataset_list:
            sample = dataset_list[0]
            for col in selected_cols:
                if col not in sample:
                    raise ValueError(f"Selected column '{col}' does not exist")

    # Filter rows
    filtered = []
    for rec in dataset_list:
        if where_part:
            try:
                keep = _evaluate_condition(rec, where_part)
            except ValueError as exc:
                raise ValueError(f"WHERE clause error: {exc}") from exc
            if not keep:
                continue
        filtered.append(rec)

    # Order rows
    if order_part:
        filtered = _apply_ordering(filtered, order_part)

    # Project columns
    if selected_cols is not None:
        result = [{k: r[k] for k in selected_cols} for r in filtered]
    else:
        result = [dict(r) for r in filtered]  # shallow copy

    return result