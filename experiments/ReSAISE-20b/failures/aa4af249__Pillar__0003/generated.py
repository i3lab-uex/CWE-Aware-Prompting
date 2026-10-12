import re
import operator
from functools import reduce

# Mapping of comparison operators to functions
_COMPARISONS = {
    '=': operator.eq,
    '==': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le
}

# Supported logical operators
_LOGICAL_OPS = {
    'AND': lambda a, b: a and b,
    'OR': lambda a, b: a or b
}

def _tokenize_where(expr):
    """Tokenise a simple WHERE expression into operands and operators."""
    # Token regex: field names, string literals, numbers, comparison ops, logical ops
    token_pattern = re.compile(r"""
        (?P<field>\b\w+\b)               |
        (?P<string>'[^']*'|"[^"]*")      |
        (?P<number>\b\d+(\.\d*)?\b)      |
        (?P<comp>(<=|>=|<>|!=|=|>|<))   |
        (?P<logic>\b(?:AND|OR)\b)        |
        \s+
    """, re.VERBOSE | re.IGNORECASE)

    tokens = []
    for match in token_pattern.finditer(expr):
        kind = match.lastgroup
        value = match.group(kind)
        if kind == 'field':
            tokens.append(('FIELD', value))
        elif kind == 'string':
            tokens.append(('STRING', value[1:-1]))
        elif kind == 'number':
            if '.' in value:
                tokens.append(('NUMBER', float(value)))
            else:
                tokens.append(('NUMBER', int(value)))
        elif kind == 'comp':
            tokens.append(('COMP', value))
        elif kind == 'logic':
            tokens.append(('LOGIC', value.upper()))
    return tokens

def _build_condition(tokens, record):
    """Recursively evaluate the token list against a single record."""
    # Convert tokens to Reverse Polish Notation using shunting-yard algorithm
    precedence = {'AND': 1, 'OR': 2}
    output_queue = []
    op_stack = []

    for token in tokens:
        ttype, val = token
        if ttype in ('FIELD', 'STRING', 'NUMBER'):
            output_queue.append(token)
        elif ttype == 'COMP':
            op_stack.append(token)
        elif ttype == 'LOGIC':
            while op_stack and op_stack[-1][0] == 'COMP':
                output_queue.append(op_stack.pop())
            while op_stack and op_stack[-1][0] == 'LOGIC' and precedence[op_stack[-1][1]] <= precedence[val]:
                output_queue.append(op_stack.pop())
            op_stack.append(token)
    while op_stack:
        output_queue.append(op_stack.pop())

    # Evaluate RPN
    stack = []
    it = iter(output_queue)
    for token in it:
        ttype, val = token
        if ttype == 'FIELD':
            stack.append(record.get(val))
        elif ttype in ('STRING', 'NUMBER'):
            stack.append(val)
        elif ttype == 'COMP':
            right = stack.pop()
            left = stack.pop()
            comp_func = _COMPARISONS.get(val)
            if not comp_func:
                raise ValueError(f"Unsupported comparison operator: {val}")
            stack.append(comp_func(left, right))
        elif ttype == 'LOGIC':
            right = stack.pop()
            left = stack.pop()
            logic_func = _LOGICAL_OPS.get(val)
            if not logic_func:
                raise ValueError(f"Unsupported logical operator: {val}")
            stack.append(logic_func(left, right))
    if len(stack) != 1:
        raise ValueError("Malformed WHERE clause.")
    return stack[0]

def process_sql_request(dataset_records, sql_statement):
    """
    Execute a simplified SQL-like query on a list of dictionaries.

    Parameters
    ----------
    dataset_records : List[Dict]
        The data to query.
    sql_statement : str
        Query string containing SELECT, optional WHERE and ORDER BY clauses.

    Returns
    -------
    List[Dict]
        Result set after applying the query.

    Raises
    ------
    ValueError
        If the statement is malformed or execution fails.
    """
    if not isinstance(dataset_records, list):
        raise ValueError("dataset_records must be a list of dictionaries.")
    if not all(isinstance(rec, dict) for rec in dataset_records):
        raise ValueError("All records must be dictionaries.")

    # Basic parsing
    select_match = re.search(r"SELECT\s+(.*?)\s+FROM", sql_statement, re.IGNORECASE)
    if not select_match:
        raise ValueError("Missing or malformed SELECT clause.")
    columns_str = select_match.group(1).strip()
    if columns_str == '*':
        selected_columns = None  # all fields
    else:
        selected_columns = [col.strip() for col in columns_str.split(',')]
        if not all(selected_columns):
            raise ValueError("Empty column name in SELECT clause.")

    where_match = re.search(r"WHERE\s+(.*?)(?:\s+ORDER\s+BY|\s*$)", sql_statement, re.IGNORECASE | re.DOTALL)
    where_expr = None
    if where_match:
        where_expr = where_match.group(1).strip()
        if not where_expr:
            raise ValueError("Empty WHERE clause.")

    order_match = re.search(r"ORDER\s+BY\s+(.*?)(?:\s*$)", sql_statement, re.IGNORECASE | re.DOTALL)
    order_by = None
    if order_match:
        order_str = order_match.group(1).strip()
        # Support optional ASC/DESC
        parts = [p.strip() for p in order_str.split(',')]
        order_by = []
        for part in parts:
            m = re.match(r"(\w+)\s*(ASC|DESC)?", part, re.IGNORECASE)
            if not m:
                raise ValueError(f"Malformed ORDER BY clause: {part}")
            col, dir_ = m.group(1), (m.group(2) or 'ASC').upper()
            order_by.append((col, dir_))

    # Apply WHERE
    if where_expr:
        tokens = _tokenize_where(where_expr)
        filtered_records = []
        for rec in dataset_records:
            try:
                if _build_condition(tokens, rec):
                    filtered_records.append(rec)
            except Exception as e:
                raise ValueError(f"Error evaluating WHERE clause: {e}")
    else:
        filtered_records = dataset_records[:]

    # Apply ORDER BY
    if order_by:
        def sort_key(rec):
            key = []
            for col, dir_ in order_by:
                val = rec.get(col)
                # None values are considered less than any other value
                key.append((val is not None, val))
            return tuple(key)

        reverse = any(dir_ == 'DESC' for _, dir_ in order_by)
        filtered_records.sort(key=sort_key, reverse=reverse)

    # Apply SELECT columns
    if selected_columns is not None:
        result = []
        for rec in filtered_records:
            new_rec = {}
            for col in selected_columns:
                if col not in rec:
                    raise ValueError(f"Column '{col}' not found in records.")
                new_rec[col] = rec[col]
            result.append(new_rec)
    else:
        result = filtered_records

    return result