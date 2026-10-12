import re
from operator import eq, ne, lt, le, gt, ge, and_, or_
from functools import reduce

# Mapping of comparison operators
_OP_MAP = {
    '=': eq,
    '==': eq,
    '!=': ne,
    '<>': ne,
    '<': lt,
    '<=': le,
    '>': gt,
    '>=': ge
}

# Supported logical operators
_LOGIC_MAP = {
    'AND': and_,
    'OR': or_
}


def _tokenize_condition(cond_str: str):
    """
    Tokenizes a simple WHERE condition string into a list of tokens.
    Supports: field, comparison operator, literal value (int/float/string),
    AND, OR.
    """
    token_pattern = r"""
        (?P<op>\bAND\b|\bOR\b) |
        (?P<cmp>=|==|!=|<>|<=|>=|<|>) |
        (?P<string>'[^']*'|"[^"]*"|\bNULL\b) |
        (?P<identifier>[A-Za-z_][A-Za-z0-9_]*) |
        (?P<number>\b\d+(\.\d+)?\b)
    """
    tokens = []
    for match in re.finditer(token_pattern, cond_str, re.VERBOSE | re.IGNORECASE):
        kind = match.lastgroup
        val = match.group()
        if kind == 'op':
            tokens.append(val.upper())
        elif kind == 'cmp':
            tokens.append(val)
        else:
            tokens.append(val.strip())
    if not tokens:
        raise ValueError("Empty WHERE condition")
    return tokens


def _build_condition_func(tokens):
    """
    Builds a function that evaluates the condition for a given record.
    Assumes tokens are in infix order with no parentheses and left-to-right evaluation.
    """
    # Convert tokens to a postfix expression using shunting-yard algorithm
    precedence = {'AND': 1, 'OR': 0}
    output_queue = []
    op_stack = []

    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if tok.upper() in _LOGIC_MAP:
            while (op_stack and op_stack[-1] != '(' and
                   precedence[op_stack[-1]] >= precedence[tok.upper()]):
                output_queue.append(op_stack.pop())
            op_stack.append(tok.upper())
            i += 1
        elif tok in _OP_MAP:
            # Comparison operator: consume left operand, operator, right operand
            left = output_queue.pop()
            op_func = _OP_MAP[tok]
            right = tokens[i + 1]
            # Prepare lambda for this comparison
            def cmp_func(record, l=left, op=op_func, r=right):
                try:
                    left_val = record[l]
                except KeyError:
                    raise ValueError(f"Field '{l}' not found in record")
                right_val = _parse_literal(r)
                return op(left_val, right_val)
            output_queue.append(cmp_func)
            i += 2
        else:
            # Identifier or literal
            output_queue.append(tok)
            i += 1

    while op_stack:
        output_queue.append(op_stack.pop())

    # Evaluate postfix expression to build a single function
    stack = []

    for item in output_queue:
        if callable(item):
            # Comparison function
            stack.append(item)
        elif isinstance(item, str) and item in _LOGIC_MAP:
            right = stack.pop()
            left = stack.pop()
            logic_func = _LOGIC_MAP[item]
            def combined(record, l=left, r=right, op=logic_func):
                return op(l(record), r(record))
            stack.append(combined)
        else:
            # Operand (identifier or literal) is pushed as is
            stack.append(item)

    if len(stack) != 1 or not callable(stack[0]):
        raise ValueError("Invalid WHERE clause syntax")
    return stack[0]


def _parse_literal(token):
    """Parse a literal token into Python type."""
    if token.upper() == 'NULL':
        return None
    if re.match(r"^'[^']*'$", token) or re.match(r'^\"[^\"]*\"$', token):
        return token[1:-1]
    if re.match(r'^\d+(\.\d+)?$', token):
        return float(token) if '.' in token else int(token)
    raise ValueError(f"Unsupported literal: {token}")


def _parse_select_clause(select_part):
    """Parse SELECT clause into list of fields or ['*']."""
    select_part = select_part.strip()
    if not select_part:
        raise ValueError("SELECT clause missing fields")
    if select_part == '*':
        return ['*']
    fields = [f.strip() for f in select_part.split(',')]
    if not all(fields):
        raise ValueError("Empty field name in SELECT clause")
    return fields


def _parse_order_by_clause(order_part):
    """Parse ORDER BY clause into list of (field, asc/desc)."""
    order_part = order_part.strip()
    if not order_part:
        raise ValueError("ORDER BY clause missing fields")
    orders = []
    for token in order_part.split(','):
        parts = token.strip().split()
        if not parts:
            continue
        field = parts[0]
        direction = 'ASC'
        if len(parts) > 1:
            dir_candidate = parts[1].upper()
            if dir_candidate in ('ASC', 'DESC'):
                direction = dir_candidate
        orders.append((field, direction))
    if not orders:
        raise ValueError("No valid fields in ORDER BY clause")
    return orders


def run_sql_query(dataset, sql_query):
    """
    Execute a simplified SQL-like query on a list of dictionaries.

    Supported syntax:
        SELECT <fields> [WHERE <condition>] [ORDER BY <field> [ASC|DESC], ...]
    """
    if not isinstance(dataset, list) or not all(isinstance(r, dict) for r in dataset):
        raise ValueError("Dataset must be a list of dictionaries")

    # Basic regex to split clauses
    pattern = re.compile(
        r"SELECT\s+(?P<select>.*?)"
        r"(?:\s+WHERE\s+(?P<where>.*?))?"
        r"(?:\s+ORDER\s+BY\s+(?P<order>.*))?$",
        re.IGNORECASE | re.DOTALL
    )
    match = pattern.match(sql_query.strip())
    if not match:
        raise ValueError("Malformed query")

    select_part = match.group('select')
    where_part = match.group('where')
    order_part = match.group('order')

    # SELECT
    fields = _parse_select_clause(select_part)

    # WHERE
    if where_part:
        tokens = _tokenize_condition(where_part)
        cond_func = _build_condition_func(tokens)
    else:
        cond_func = lambda record: True

    # Filter records
    try:
        filtered = [r for r in dataset if cond_func(r)]
    except Exception as e:
        raise ValueError(f"Error evaluating WHERE clause: {e}")

    # ORDER BY
    if order_part:
        orders = _parse_order_by_clause(order_part)
        def sort_key(record):
            key_vals = []
            for field, direction in orders:
                try:
                    val = record[field]
                except KeyError:
                    raise ValueError(f"Field '{field}' not found for ORDER BY")
                key_vals.append(val if direction == 'ASC' else _invert_value(val))
            return tuple(key_vals)
        filtered.sort(key=sort_key)

    # SELECT fields
    if fields == ['*']:
        result = filtered
    else:
        result = []
        for rec in filtered:
            new_rec = {}
            for f in fields:
                if f not in rec:
                    raise ValueError(f"Field '{f}' not found in record")
                new_rec[f] = rec[f]
            result.append(new_rec)

    return result


def _invert_value(val):
    """Helper to invert value for DESC sorting."""
    # For numbers and strings, we can rely on reversed ordering
    if isinstance(val, (int, float)):
        return -val
    if isinstance(val, str):
        # Reverse string ordering by using tuple of negative ordinals
        return ''.join(chr(255 - ord(c)) for c in val)
    # Fallback: use the value itself (will be sorted ascending)
    return val