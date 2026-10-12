import re
import operator
from functools import reduce

# Map of supported comparison operators
_COMPARATORS = {
    '=': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le,
}

# Map of supported logical operators
_LOGICAL = {
    'AND': lambda a, b: a and b,
    'OR':  lambda a, b: a or b,
}

def _tokenize(expr):
    """
    Very small tokenizer for simple WHERE expressions.
    Supports identifiers, literals (numbers or quoted strings), and
    comparison/logical operators.
    """
    token_spec = [
        ('NUMBER',   r'\d+(\.\d*)?'),            # Integer or decimal number
        ('STRING',   r'\'[^\']*\'|"[^"]*"'),    # Single or double quoted string
        ('IDENT',    r'[A-Za-z_][A-Za-z0-9_]*'),# Identifiers
        ('OP',       r'!=|<>|>=|<=|=|>|<'),     # Comparison operators
        ('LOG',      r'\bAND\b|\bOR\b'),         # Logical operators
        ('SKIP',     r'[ \t]+'),                # Skip spaces and tabs
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_spec)
    for mo in re.finditer(tok_regex, expr):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'SKIP':
            continue
        yield (kind, value)

def _build_where_func(where_clause):
    """
    Build a function that evaluates the WHERE clause for a record.
    Supports only binary comparisons combined with AND/OR.
    """
    tokens = list(_tokenize(where_clause))
    if not tokens:
        raise ValueError("Empty WHERE clause")

    # Convert infix to postfix (shunting-yard) for evaluation
    output = []
    ops_stack = []

    precedence = {'AND': 1, 'OR': 2}
    for kind, token in tokens:
        if kind == 'IDENT':
            output.append(('VAR', token))
        elif kind in ('NUMBER', 'STRING'):
            # Remove surrounding quotes for strings
            if token[0] in ('"', "'"):
                val = token[1:-1]
            else:
                val = float(token) if '.' in token else int(token)
            output.append(('VAL', val))
        elif kind == 'OP':
            ops_stack.append(('CMP', token))
        elif kind == 'LOG':
            while (ops_stack and ops_stack[-1][0] in ('CMP', 'LOG')
                   and precedence.get(ops_stack[-1][1], 3) <= precedence[token]):
                output.append(ops_stack.pop())
            ops_stack.append(('LOG', token))
        else:
            raise ValueError(f"Unsupported token: {token}")

    while ops_stack:
        output.append(ops_stack.pop())

    # Build a lambda that evaluates the postfix expression
    def eval_record(record):
        stack = []
        for typ, val in output:
            if typ == 'VAR':
                stack.append(record.get(val))
            elif typ == 'VAL':
                stack.append(val)
            elif typ == 'CMP':
                right = stack.pop()
                left = stack.pop()
                cmp_func = _COMPARATORS.get(val)
                if not cmp_func:
                    raise ValueError(f"Unsupported comparison operator: {val}")
                stack.append(cmp_func(left, right))
            elif typ == 'LOG':
                b = stack.pop()
                a = stack.pop()
                log_func = _LOGICAL.get(val)
                if not log_func:
                    raise ValueError(f"Unsupported logical operator: {val}")
                stack.append(log_func(a, b))
            else:
                raise ValueError(f"Unknown expression part: {typ}")
        if len(stack) != 1:
            raise ValueError("Malformed WHERE expression")
        return bool(stack[0])

    return eval_record

def submit_user_query(records, sql_statement):
    """
    Execute a simple SQL-like query on a list of dictionaries.
    
    Supports:
        SELECT <columns>
        [WHERE <condition>]
        [ORDER BY <column> [ASC|DESC]]
    """
    if not isinstance(records, list):
        raise ValueError("records must be a list")
    if not all(isinstance(r, dict) for r in records):
        raise ValueError("all items in records must be dictionaries")

    # Basic parsing
    pattern = r"""
        ^\s*SELECT\s+(?P<select>[\w\*,\s]+)
        (\s+WHERE\s+(?P<where>.+?))?
        (\s+ORDER\s+BY\s+(?P<order_by>\w+)(\s+(?P<order_dir>ASC|DESC))?)?
        \s*$
    """
    match = re.match(pattern, sql_statement, re.IGNORECASE | re.VERBOSE)
    if not match:
        raise ValueError("Invalid query format")

    select_part = match.group('select').strip()
    where_part = match.group('where')
    order_by_col = match.group('order_by')
    order_dir = match.group('order_dir') or 'ASC'

    # Determine columns to select
    if select_part == '*':
        selected_columns = None  # all columns
    else:
        selected_columns = [col.strip() for col in select_part.split(',')]
        if not all(selected_columns):
            raise ValueError("Empty column name in SELECT clause")

    # Build where function if present
    if where_part:
        try:
            where_func = _build_where_func(where_part.strip())
        except Exception as e:
            raise ValueError(f"Invalid WHERE clause: {e}") from e
    else:
        where_func = lambda r: True

    # Filter records
    try:
        filtered = [rec for rec in records if where_func(rec)]
    except Exception as e:
        raise ValueError(f"Error evaluating WHERE clause: {e}") from e

    # Order results if requested
    if order_by_col:
        reverse = order_dir.upper() == 'DESC'
        try:
            filtered.sort(key=lambda r: r.get(order_by_col), reverse=reverse)
        except Exception as e:
            raise ValueError(f"Error in ORDER BY clause: {e}") from e

    # Project selected columns
    if selected_columns is not None:
        try:
            result = [{k: rec.get(k) for k in selected_columns} for rec in filtered]
        except Exception as e:
            raise ValueError(f"Error projecting columns: {e}") from e
    else:
        result = filtered

    return result