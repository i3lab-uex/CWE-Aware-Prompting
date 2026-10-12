import re
import operator
from functools import reduce

# Supported binary operators mapping
OPS = {
    '==': operator.eq,
    '=': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,
    '>=': operator.ge,
    '<=': operator.le,
    '>': operator.gt,
    '<': operator.lt
}

# Supported logical operators
LOGIC_OPS = {'AND', 'OR'}


def _parse_select_part(select_str):
    """Parse the SELECT part and return list of column names."""
    cols = [c.strip() for c in select_str.split(',')]
    if not all(cols):
        raise ValueError("Invalid SELECT clause")
    return cols


def _parse_order_by_part(order_str):
    """Parse ORDER BY part and return column name + ascending flag."""
    parts = order_str.strip().split()
    if not parts:
        raise ValueError("Invalid ORDER BY clause")
    col = parts[0]
    asc = True
    if len(parts) > 1:
        dir_ = parts[1].upper()
        if dir_ == 'DESC':
            asc = False
        elif dir_ != 'ASC':
            raise ValueError("ORDER BY direction must be ASC or DESC")
    return col, asc


def _tokenize_condition(cond_str):
    """Tokenise a simple condition into operands and operators."""
    # replace logical ops with placeholders
    cond_str = re.sub(r'\bAND\b', ' AND ', cond_str, flags=re.IGNORECASE)
    cond_str = re.sub(r'\bOR\b', ' OR ', cond_str, flags=re.IGNORECASE)
    tokens = [t.strip() for t in re.split(r'\s+', cond_str) if t]
    return tokens


def _build_condition_func(cond_tokens):
    """Build a function that evaluates the condition on a record."""
    def eval_operand(operand, record):
        # Try numeric
        try:
            return float(operand)
        except ValueError:
            pass
        # Try string literal in quotes
        if (operand.startswith('"') and operand.endswith('"')) or \
           (operand.startswith("'") and operand.endswith("'")):
            return operand[1:-1]
        # Treat as field name
        if operand not in record:
            raise ValueError(f"Field {operand!r} not found in dataset")
        return record[operand]

    def parse_expr(tokens):
        # Recursive descent for simple expressions without parentheses
        if len(tokens) < 3:
            raise ValueError("Incomplete condition expression")
        left = eval_operand(tokens[0], None)
        op_token = tokens[1]
        right = eval_operand(tokens[2], None)

        if op_token not in OPS:
            raise ValueError(f"Unsupported operator {op_token!r}")
        op_func = OPS[op_token]

        def expr(record):
            l_val = eval_operand(tokens[0], record)
            r_val = eval_operand(tokens[2], record)
            return op_func(l_val, r_val)

        # Handle logical operators
        if len(tokens) > 3:
            logic_op = tokens[3].upper()
            if logic_op not in LOGIC_OPS:
                raise ValueError(f"Unsupported logical operator {logic_op!r}")
            rest = parse_expr(tokens[4:])
            if logic_op == 'AND':
                return lambda record: expr(record) and rest(record)
            else:
                return lambda record: expr(record) or rest(record)

        return expr

    return parse_expr(cond_tokens)


def execute_query_cmd(dataset_list, sql_query):
    """
    Execute a simple SQL-like query on a list of dictionaries.

    Supported syntax:
        SELECT <col1>,<col2>,... [WHERE <condition>] [ORDER BY <col> [ASC|DESC]]
    """
    if not isinstance(dataset_list, list):
        raise ValueError("dataset_list must be a list")
    if not isinstance(sql_query, str):
        raise ValueError("sql_query must be a string")

    # Basic regex to extract clauses
    pattern = re.compile(
        r"SELECT\s+(?P<select>.+?)"
        r"(?:\s+WHERE\s+(?P<where>.+?))?"
        r"(?:\s+ORDER\s+BY\s+(?P<order>.+))?$",
        re.IGNORECASE | re.DOTALL
    )
    match = pattern.match(sql_query.strip())
    if not match:
        raise ValueError("Query format is invalid")

    select_part = match.group('select')
    where_part = match.group('where')
    order_part = match.group('order')

    # Parse SELECT columns
    selected_cols = _parse_select_part(select_part)

    # Filter dataset according to WHERE clause if present
    filtered = dataset_list
    if where_part:
        tokens = _tokenize_condition(where_part)
        cond_func = _build_condition_func(tokens)
        try:
            filtered = [rec for rec in dataset_list if cond_func(rec)]
        except Exception as exc:
            raise ValueError(f"Error evaluating WHERE clause: {exc}") from exc

    # Project selected columns
    result = []
    for rec in filtered:
        projected = {}
        for col in selected_cols:
            if col not in rec:
                raise ValueError(f"Column {col!r} not found in record")
            projected[col] = rec[col]
        result.append(projected)

    # Order by if present
    if order_part:
        order_col, asc = _parse_order_by_part(order_part)
        if not result:
            return result
        if order_col not in result[0]:
            raise ValueError(f"ORDER BY column {order_col!r} not found")
        try:
            result.sort(key=lambda r: r[order_col], reverse=not asc)
        except TypeError as exc:
            raise ValueError(f"Cannot order by column {order_col!r}: {exc}") from exc

    return result