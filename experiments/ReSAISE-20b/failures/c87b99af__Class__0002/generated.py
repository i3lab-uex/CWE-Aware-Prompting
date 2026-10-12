import re
import operator
from functools import reduce

# Mapping of string comparison operators to actual functions
_COMPARISONS = {
    '=': operator.eq,
    '==': operator.eq,
    '<>': operator.ne,
    '!=': operator.ne,
    '>': operator.gt,
    '>=': operator.ge,
    '<': operator.lt,
    '<=': operator.le,
}

# Allowed logical operators
_LOGICAL_OPS = {
    'AND': lambda a, b: a and b,
    'OR': lambda a, b: a or b,
}

def _parse_select_clause(query):
    """
    Extract the list of fields to select.
    """
    m = re.search(r'\bSELECT\b\s+(.*?)\s+\bFROM\b', query, flags=re.IGNORECASE | re.DOTALL)
    if not m:
        raise ValueError("Missing or malformed SELECT clause")
    fields_str = m.group(1).strip()
    if fields_str == '*':
        return None  # select all
    fields = [f.strip() for f in fields_str.split(',')]
    if not fields:
        raise ValueError("No fields specified in SELECT clause")
    return fields

def _parse_where_clause(query):
    """
    Extract the WHERE condition string.
    """
    m = re.search(r'\bWHERE\b\s+(.*?)\s*(?:ORDER BY|$)', query, flags=re.IGNORECASE | re.DOTALL)
    if not m:
        return None
    condition = m.group(1).strip()
    if not condition:
        raise ValueError("Empty WHERE clause")
    return condition

def _parse_order_by_clause(query):
    """
    Extract ORDER BY fields and direction.
    """
    m = re.search(r'\bORDER\s+BY\b\s+(.*?)(?:$|WHERE)', query, flags=re.IGNORECASE | re.DOTALL)
    if not m:
        return None
    order_str = m.group(1).strip()
    if not order_str:
        raise ValueError("Empty ORDER BY clause")
    parts = [p.strip() for p in order_str.split(',')]
    orders = []
    for part in parts:
        tokens = part.split()
        field = tokens[0]
        direction = tokens[1].upper() if len(tokens) > 1 else 'ASC'
        if direction not in ('ASC', 'DESC'):
            raise ValueError(f"Invalid ORDER BY direction: {direction}")
        orders.append((field, direction))
    return orders

def _tokenize_condition(cond):
    """
    Very simple tokenizer for conditions. Supports:
      - comparisons with ==, =, !=, <>, >, >=, <, <=
      - logical AND / OR (case-insensitive)
    """
    tokens = []
    pattern = r"""(?P<LPAREN>\()|(?P<RPARAN>\))|
                  (?P<AND>AND\b)|(?P<OR>OR\b)|
                  (?P<OP>=|==|!=|<>|<=|>=|<|>)|
                  (?P<STRING>'[^']*')|
                  (?P<DWORD>[A-Za-z_][A-Za-z0-9_]*)|
                  (?P<NUMBER>\d+(?:\.\d+)?)"""
    for m in re.finditer(pattern, cond, flags=re.IGNORECASE | re.VERBOSE):
        kind = m.lastgroup
        val = m.group()
        tokens.append((kind, val))
    return tokens

def _build_condition_func(tokens):
    """
    Build a function that evaluates the condition against a record.
    The function will raise ValueError if tokens are invalid.
    """
    def parse_expr(index):
        # Parse a single comparison: field op value
        if index >= len(tokens):
            raise ValueError("Incomplete condition")
        kind, val = tokens[index]
        if kind != 'DWORD':
            raise ValueError("Expected field name")
        field = val
        index += 1

        if index >= len(tokens):
            raise ValueError("Expected operator after field")
        op_kind, op_val = tokens[index]
        if op_kind != 'OP':
            raise ValueError("Expected comparison operator")
        cmp_func = _COMPARISONS[op_val]
        index += 1

        if index >= len(tokens):
            raise ValueError("Expected value after operator")
        val_kind, val_val = tokens[index]
        if val_kind == 'STRING':
            value = val_val[1:-1]  # strip quotes
        elif val_kind == 'NUMBER':
            value = float(val_val) if '.' in val_val else int(val_val)
        elif val_kind == 'DWORD':
            # Treat as field reference
            value = None  # placeholder, will fetch from record later
        else:
            raise ValueError("Expected value after operator")
        index += 1

        def comp(record):
            left = record.get(field)
            right = value
            if val_kind == 'DWORD':
                # field-to-field comparison
                right = record.get(val_val)
            return cmp_func(left, right)

        return comp, index

    def parse_factor(index):
        kind, val = tokens[index]
        if kind == 'LPAREN':
            sub_func, next_index = parse_expr(index + 1)
            if tokens[next_index][0] != 'RPARAN':
                raise ValueError("Missing closing parenthesis")
            return sub_func, next_index + 1
        else:
            return parse_expr(index)

    def parse_term(index):
        func, index = parse_factor(index)
        while index < len(tokens) and tokens[index][0] == 'AND':
            right_func, next_index = parse_factor(index + 1)
            prev_func = func
            func = lambda rec, f=prev_func, g=right_func: f(rec) and g(rec)
            index = next_index
        return func, index

    def parse_expr(index):
        func, index = parse_term(index)
        while index < len(tokens) and tokens[index][0] == 'OR':
            right_func, next_index = parse_term(index + 1)
            prev_func = func
            func = lambda rec, f=prev_func, g=right_func: f(rec) or g(rec)
            index = next_index
        return func, index

    final_func, idx = parse_expr(0)
    if idx != len(tokens):
        raise ValueError("Unexpected tokens in condition")
    return final_func

def execute_user_query(records, user_query):
    """
    Execute a simple SQL‑like query on a list of dictionaries.

    Parameters
    ----------
    records : list[dict]
        Dataset to query.
    user_query : str
        Query string containing SELECT, optional WHERE and ORDER BY.

    Returns
    -------
    list[dict]
        Resulting records after applying SELECT, filtering and sorting.

    Raises
    ------
    ValueError
        If the query syntax is invalid or evaluation fails.
    """
    if not isinstance(records, list):
        raise ValueError("records must be a list")
    if not isinstance(user_query, str):
        raise ValueError("user_query must be a string")

    # Normalise whitespace
    query = re.sub(r'\s+', ' ', user_query.strip())

    # Parse clauses
    select_fields = _parse_select_clause(query)
    where_cond_str = _parse_where_clause(query)
    order_by = _parse_order_by_clause(query)

    # Filter records
    if where_cond_str:
        tokens = _tokenize_condition(where_cond_str)
        cond_func = _build_condition_func(tokens)
        try:
            filtered = [r for r in records if cond_func(r)]
        except Exception as e:
            raise ValueError(f"Error evaluating WHERE clause: {e}") from e
    else:
        filtered = list(records)

    # Sort records
    if order_by:
        def sort_key(rec):
            key = []
            for field, direction in order_by:
                val = rec.get(field)
                # None values should be treated as less than any other value
                key.append((val is None, val))
            return tuple(key)

        reverse = any(direction == 'DESC' for _, direction in order_by)
        try:
            filtered.sort(key=sort_key, reverse=reverse)
        except Exception as e:
            raise ValueError(f"Error during ORDER BY: {e}") from e

    # Project selected fields
    if select_fields is None:
        result = filtered
    else:
        result = [{k: rec.get(k) for k in select_fields} for rec in filtered]

    return result