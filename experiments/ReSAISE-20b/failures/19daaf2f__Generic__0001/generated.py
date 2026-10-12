import re
import operator
from functools import reduce

# Mapping of string operators to functions
OPERATORS = {
    '=': operator.eq,
    '==': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le,
}

LOGICAL_OPERATORS = {
    'AND': lambda a, b: a and b,
    'OR': lambda a, b: a or b,
}


def _parse_select_clause(clause):
    """Parse SELECT clause into list of columns."""
    columns = [c.strip() for c in clause.split(',')]
    if len(columns) == 1 and columns[0] == '*':
        return None  # indicate all columns
    return columns


def _tokenize_where(condition):
    """Tokenize a simple WHERE condition into (col, op, value) tuples."""
    # Split by AND/OR
    tokens = re.split(r'\s+(AND|OR)\s+', condition, flags=re.IGNORECASE)
    parts = []
    i = 0
    while i < len(tokens):
        if tokens[i].upper() in LOGICAL_OPERATORS:
            parts.append(('LOGIC', tokens[i].upper()))
            i += 1
        else:
            # Parse column op value
            m = re.match(r"(\w+)\s*(=|==|!=|<>|>=|<=|>|<)\s*('([^']*)'|\"([^\"]*)\"|(\d+\.?\d*))", tokens[i])
            if not m:
                raise ValueError(f"Invalid WHERE clause token: {tokens[i]}")
            col = m.group(1)
            op = m.group(2)
            if m.group(4) is not None:
                val = m.group(4)
            elif m.group(5) is not None:
                val = m.group(5)
            else:
                # numeric
                val = float(m.group(6)) if '.' in m.group(6) else int(m.group(6))
            parts.append(('COND', (col, op, val)))
            i += 1
    return parts


def _evaluate_where(record, tokens):
    """Evaluate the tokenized WHERE clause against a record."""
    def eval_cond(cond):
        col, op, val = cond
        if col not in record:
            raise ValueError(f"Column {col} not found in record")
        return OPERATORS[op](record[col], val)

    stack = []
    i = 0
    while i < len(tokens):
        typ, val = tokens[i]
        if typ == 'COND':
            stack.append(eval_cond(val))
        elif typ == 'LOGIC':
            op_func = LOGICAL_OPERATORS[val]
            if len(stack) < 2:
                raise ValueError("Invalid logical expression in WHERE clause")
            right = stack.pop()
            left = stack.pop()
            stack.append(op_func(left, right))
        i += 1
    if len(stack) != 1:
        raise ValueError("Failed to evaluate WHERE clause")
    return stack[0]


def _parse_order_by(clause):
    """Parse ORDER BY clause into (column, ascending) tuple."""
    parts = clause.strip().split()
    if len(parts) == 0:
        raise ValueError("Empty ORDER BY clause")
    col = parts[0]
    ascending = True
    if len(parts) > 1:
        dir_word = parts[1].upper()
        if dir_word == 'DESC':
            ascending = False
        elif dir_word != 'ASC':
            raise ValueError(f"Invalid ORDER BY direction: {dir_word}")
    return col, ascending


def run_sql_query(dataset, sql_query):
    """
    Execute a simplified SQL-like query on a list of dictionaries.

    Supported clauses:
        SELECT columns
        WHERE condition  (supports =, !=, <, <=, >, >=, AND, OR)
        ORDER BY column [ASC|DESC]

    Parameters
    ----------
    dataset : list[dict]
        The data to query.
    sql_query : str
        The SQL-like query string.

    Returns
    -------
    list[dict]
        Query results.

    Raises
    ------
    ValueError
        If the query is malformed or execution fails.
    """
    if not isinstance(dataset, list):
        raise ValueError("dataset must be a list of dictionaries")
    if not isinstance(sql_query, str):
        raise ValueError("sql_query must be a string")

    # Basic tokenization
    sql = sql_query.strip()
    select_match = re.search(r'SELECT\s+(.*?)\s+WHERE', sql, flags=re.IGNORECASE | re.DOTALL)
    if not select_match:
        # Maybe no WHERE
        select_match = re.search(r'SELECT\s+(.*?)(\s+ORDER BY|\s*$)', sql, flags=re.IGNORECASE | re.DOTALL)
    if not select_match:
        raise ValueError("Missing SELECT clause")
    select_clause = select_match.group(1)

    # Determine WHERE
    where_match = re.search(r'WHERE\s+(.*?)(\s+ORDER BY|\s*$)', sql, flags=re.IGNORECASE | re.DOTALL)
    where_clause = None
    if where_match:
        where_clause = where_match.group(1).strip()

    # Determine ORDER BY
    order_by_match = re.search(r'ORDER\s+BY\s+(.*)$', sql, flags=re.IGNORECASE)
    order_by_clause = None
    if order_by_match:
        order_by_clause = order_by_match.group(1).strip()

    # Parse SELECT columns
    select_columns = _parse_select_clause(select_clause)

    # Filter dataset by WHERE clause if present
    filtered_data = []
    for record in dataset:
        try:
            passes_where = True
            if where_clause:
                tokens = _tokenize_where(where_clause)
                passes_where = _evaluate_where(record, tokens)
            if passes_where:
                filtered_data.append(record)
        except Exception as e:
            raise ValueError(f"Failed to evaluate WHERE clause: {e}")

    # Apply ORDER BY if present
    if order_by_clause:
        try:
            col, ascending = _parse_order_by(order_by_clause)
            filtered_data.sort(key=lambda r: r.get(col), reverse=not ascending)
        except Exception as e:
            raise ValueError(f"Failed to apply ORDER BY: {e}")

    # Project selected columns
    if select_columns is None:
        result = [dict(rec) for rec in filtered_data]
    else:
        result = []
        for rec in filtered_data:
            projected = {}
            for col in select_columns:
                if col not in rec:
                    raise ValueError(f"Column {col} not found in record")
                projected[col] = rec[col]
            result.append(projected)

    return result