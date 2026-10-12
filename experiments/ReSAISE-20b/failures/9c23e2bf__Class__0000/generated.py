import re
import operator
from functools import reduce

# Supported comparison operators mapping from string to callable
_COMPARISONS = {
    '=': operator.eq,
    '==': operator.eq,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le,
    '!=': operator.ne,
}

# Supported logical operators mapping
_LOGICALS = {
    'AND': lambda a, b: a and b,
    'OR': lambda a, b: a or b,
}

def _parse_select(query):
    """
    Parse the SELECT clause to determine which fields to keep.
    If '*' is used, all fields are returned.
    """
    match = re.search(r'\bSELECT\b\s+(?P<fields>[\*\w,\s]+)', query, re.IGNORECASE)
    if not match:
        raise ValueError("Missing or malformed SELECT clause.")
    fields_str = match.group('fields').strip()
    if fields_str == '*':
        return None  # None indicates all fields
    fields = [f.strip() for f in fields_str.split(',')]
    if not all(fields):
        raise ValueError("Empty field name detected in SELECT clause.")
    return fields

def _tokenize_where(where_clause):
    """
    Tokenise a simple WHERE clause into operands and operators.
    Supports only comparisons between field names and literal values
    (numeric or quoted strings) and logical operators AND/OR.
    """
    tokens = []
    # Regex to capture field, operator, value
    comp_re = re.compile(r'(?P<field>\w+)\s*(?P<op>[=<>!]+)\s*(?P<value>(?:\'[^\']*\'|\"[^\"]*\"|\d+(?:\.\d+)?))', re.IGNORECASE)
    # Split by AND/OR
    parts = re.split(r'\b(AND|OR)\b', where_clause, flags=re.IGNORECASE)
    parts = [p.strip() for p in parts if p.strip()]
    i = 0
    while i < len(parts):
        part = parts[i]
        if part.upper() in _LOGICALS:
            tokens.append(part.upper())
            i += 1
        else:
            m = comp_re.match(part)
            if not m:
                raise ValueError(f"Unsupported WHERE condition: '{part}'")
            field = m.group('field')
            op_str = m.group('op')
            value_raw = m.group('value')
            # Convert numeric literals
            if re.fullmatch(r'\d+\.\d+', value_raw):
                value = float(value_raw)
            elif re.fullmatch(r'\d+', value_raw):
                value = int(value_raw)
            else:
                # Strip quotes
                value = value_raw[1:-1]
            tokens.append((field, _COMPARISONS[op_str], value))
            i += 1
    return tokens

def _evaluate_where(tokens, record):
    """
    Evaluate the tokenised WHERE clause against a single record.
    """
    if not tokens:
        return True
    # Convert infix to postfix for easier evaluation (shunting yard)
    precedence = {'AND': 2, 'OR': 1}
    output_queue = []
    op_stack = []

    for token in tokens:
        if isinstance(token, tuple):
            output_queue.append(token)
        elif token in _LOGICALS:
            while (op_stack and op_stack[-1] in _LOGICALS
                   and precedence[op_stack[-1]] >= precedence[token]):
                output_queue.append(op_stack.pop())
            op_stack.append(token)
        else:
            raise ValueError(f"Unexpected token in WHERE clause: {token}")

    while op_stack:
        output_queue.append(op_stack.pop())

    # Evaluate postfix
    stack = []
    for token in output_queue:
        if isinstance(token, tuple):
            field, op_func, value = token
            record_value = record.get(field)
            stack.append(op_func(record_value, value))
        else:  # logical operator
            b = stack.pop()
            a = stack.pop()
            stack.append(_LOGICALS[token](a, b))
    return stack[0]

def _parse_order_by(query):
    """
    Parse ORDER BY clause. Supports optional ASC/DESC per field.
    Returns a list of (field, reverse) tuples.
    """
    match = re.search(r'\bORDER\s+BY\b\s+(?P<order>[\w,\s]+)', query, re.IGNORECASE)
    if not match:
        return None
    order_str = match.group('order').strip()
    fields = []
    for part in order_str.split(','):
        part = part.strip()
        if not part:
            continue
        tokens = part.split()
        field = tokens[0]
        direction = tokens[1].upper() if len(tokens) > 1 else 'ASC'
        if direction not in ('ASC', 'DESC'):
            raise ValueError(f"Unsupported ORDER BY direction: {direction}")
        fields.append((field, direction == 'DESC'))
    return fields

def run_custom_query(dataset, query):
    """
    Execute a simple SQL-like query on an in-memory dataset.

    Parameters
    ----------
    dataset : list[dict]
        List of records, each record is a dictionary.
    query : str
        SQL-like statement supporting SELECT, WHERE and ORDER BY.

    Returns
    -------
    list[dict]
        The query result as a list of dictionaries.

    Raises
    ------
    ValueError
        If the query syntax is invalid or cannot be processed.
    """
    if not isinstance(dataset, list):
        raise ValueError("Dataset must be a list of dictionaries.")
    if not all(isinstance(r, dict) for r in dataset):
        raise ValueError("All items in dataset must be dictionaries.")

    # Normalize query string
    q = query.strip()
    if not q:
        raise ValueError("Query is empty.")

    # Parse SELECT
    fields = _parse_select(q)

    # Parse WHERE
    where_match = re.search(r'\bWHERE\b\s+(?P<where>.+?)(?:\bORDER\s+BY\b|$)', q, re.IGNORECASE)
    where_tokens = None
    if where_match:
        where_clause = where_match.group('where').strip()
        if not where_clause:
            raise ValueError("Empty WHERE clause.")
        where_tokens = _tokenize_where(where_clause)

    # Parse ORDER BY
    order_by_fields = _parse_order_by(q)

    # Apply WHERE filter
    filtered = [rec for rec in dataset if _evaluate_where(where_tokens, rec)]

    # Apply ORDER BY
    if order_by_fields:
        def sort_key(rec):
            return tuple(
                (rec.get(f),) if not rev else (-float('inf') if rec.get(f) is None else -rec[f]) 
                for f, rev in order_by_fields
            )
        # Since we cannot rely on numeric negation for all types, we sort manually
        def cmp_func(rec):
            key = []
            for f, rev in order_by_fields:
                val = rec.get(f)
                if isinstance(val, (int, float)):
                    key.append(-val if rev else val)
                elif isinstance(val, str):
                    key.append('' if rev else val)  # placeholder for reverse
                else:
                    key.append(val)
            return tuple(key)

        filtered.sort(key=cmp_func)

    # Apply SELECT projection
    if fields is not None:
        result = [{k: rec.get(k) for k in fields} for rec in filtered]
    else:
        result = [rec.copy() for rec in filtered]

    return result