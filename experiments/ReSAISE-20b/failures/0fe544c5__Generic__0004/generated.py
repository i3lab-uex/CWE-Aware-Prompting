import re
from operator import eq, ne, lt, le, gt, ge
from functools import reduce

# Mapping of string operators to actual functions
OPERATORS = {
    '=': eq,
    '!=': ne,
    '<': lt,
    '<=': le,
    '>': gt,
    '>=': ge
}

def _tokenize_condition(cond_str):
    """
    Very small tokenizer that splits a condition string into
    (field, operator, value) tuples and logical connectors.
    Supports: AND, OR, parentheses.
    """
    # Normalize spaces around operators
    for op in sorted(OPERATORS.keys(), key=len, reverse=True):
        cond_str = re.sub(r'\s*' + re.escape(op) + r'\s*', f' {op} ', cond_str)
    tokens = re.findall(r"\w+|[=<>!]+|\(|\)|AND|OR", cond_str, flags=re.IGNORECASE)
    return tokens

def _parse_condition(tokens):
    """
    Convert token list into a nested structure that can be evaluated.
    Returns a lambda function that takes a record and returns bool.
    """
    def parse_expr(index):
        stack = []
        ops = []

        def apply_operator():
            op = ops.pop()
            right = stack.pop()
            left = stack.pop()
            if op == 'AND':
                stack.append(lambda r, l=left, y=right: l(r) and y(r))
            elif op == 'OR':
                stack.append(lambda r, l=left, y=right: l(r) or y(r))
            else:
                # comparison operator
                stack.append(lambda r, l=left, y=right, opfn=OPERATORS[op]: opfn(r[l], y))

        while index < len(tokens):
            token = tokens[index]
            if token == '(':
                ops.append(token)
                index += 1
            elif token == ')':
                while ops and ops[-1] != '(':
                    apply_operator()
                if not ops or ops.pop() != '(':
                    raise ValueError("Mismatched parentheses in WHERE clause")
                index += 1
            elif token.upper() in ('AND', 'OR'):
                while ops and ops[-1] not in ('(', 'AND', 'OR'):
                    apply_operator()
                ops.append(token.upper())
                index += 1
            elif token in OPERATORS:
                # comparison operator: expect left operand on stack, right operand next
                op = token
                if not stack:
                    raise ValueError("Malformed comparison in WHERE clause")
                left = stack.pop()
                index += 1
                if index >= len(tokens):
                    raise ValueError("Missing right operand in WHERE clause")
                right_token = tokens[index]
                # Determine if value is numeric or string
                if re.match(r"^-?\d+(\.\d+)?$", right_token):
                    right = float(right_token) if '.' in right_token else int(right_token)
                elif re.match(r"^'.*'$", right_token):
                    right = right_token.strip("'")
                else:
                    # treat as field name
                    right = right_token
                ops.append(op)
                stack.append(left)  # left operand already on stack
                stack.append(right)  # right operand as value
                index += 1
            else:
                # token is a field name or literal
                stack.append(token)
                index += 1

        while ops:
            apply_operator()
        if len(stack) != 1:
            raise ValueError("Invalid WHERE clause")
        return stack[0], index

    func, _ = parse_expr(0)
    if not callable(func):
        raise ValueError("Failed to parse WHERE clause")
    return func

def _parse_sql(sql):
    """
    Parse a simple SQL-like statement.
    Supported syntax:
        SELECT <columns> WHERE <conditions> ORDER BY <column> [ASC|DESC]
    The FROM clause is omitted because the data source is passed as an argument.
    """
    sql = sql.strip()
    # Split by keywords, case-insensitive
    pattern = re.compile(
        r"SELECT\s+(?P<select>.+?)\s+"
        r"(WHERE\s+(?P<where>.+?))?"
        r"(ORDER\s+BY\s+(?P<orderby>\w+)(\s+(?P<orderdir>ASC|DESC))?)?$",
        flags=re.IGNORECASE | re.DOTALL
    )
    m = pattern.match(sql)
    if not m:
        raise ValueError("SQL syntax error")

    select_part = m.group('select').strip()
    where_part = m.group('where')
    orderby_part = m.group('orderby')
    orderdir_part = m.group('orderdir')

    # Parse SELECT columns
    if select_part == '*':
        selected_cols = None  # all fields
    else:
        selected_cols = [col.strip() for col in select_part.split(',')]
        if not all(selected_cols):
            raise ValueError("Empty column name in SELECT clause")

    # Parse WHERE condition
    where_func = None
    if where_part:
        tokens = _tokenize_condition(where_part)
        where_func = _parse_condition(tokens)

    # Parse ORDER BY
    order_by = None
    reverse = False
    if orderby_part:
        order_by = orderby_part.strip()
        if orderdir_part and orderdir_part.upper() == 'DESC':
            reverse = True

    return selected_cols, where_func, order_by, reverse

def handle_sql_query(records, sql_command):
    """
    Execute a simple SQL-like query on a list of record dictionaries.

    Parameters
    ----------
    records : List[Dict]
        The dataset to query.
    sql_command : str
        A SQL-like string containing SELECT, WHERE, and ORDER BY clauses.

    Returns
    -------
    List[Dict]
        The query result as a list of dictionaries.

    Raises
    ------
    ValueError
        If the query is malformed or execution fails.
    """
    if not isinstance(records, list):
        raise ValueError("records must be a list of dictionaries")
    if not all(isinstance(r, dict) for r in records):
        raise ValueError("All items in records must be dictionaries")

    selected_cols, where_func, order_by, reverse = _parse_sql(sql_command)

    # Filter records
    if where_func:
        try:
            filtered = [rec for rec in records if where_func(rec)]
        except Exception as e:
            raise ValueError(f"Error evaluating WHERE clause: {e}") from e
    else:
        filtered = records[:]

    # Order records
    if order_by:
        try:
            filtered.sort(key=lambda r: r.get(order_by, None), reverse=reverse)
        except Exception as e:
            raise ValueError(f"Error sorting by '{order_by}': {e}") from e

    # Project columns
    if selected_cols is None:
        result = [rec.copy() for rec in filtered]
    else:
        result = []
        for rec in filtered:
            projected = {}
            for col in selected_cols:
                if col not in rec:
                    raise ValueError(f"Column '{col}' does not exist in records")
                projected[col] = rec[col]
            result.append(projected)

    return result