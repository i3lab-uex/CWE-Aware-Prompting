import re
import operator
from functools import reduce

# Mapping of comparison operators used in WHERE clause
_COMPARISONS = {
    '=': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,
    '>': operator.gt,
    '>=': operator.ge,
    '<': operator.lt,
    '<=': operator.le,
}

# Mapping of logical operators used in WHERE clause
_LOGICAL = {
    'AND': lambda a, b: a and b,
    'OR': lambda a, b: a or b,
}

def _parse_select_clause(sql):
    """Return list of column names to select."""
    m = re.search(r'\bSELECT\s+(.*?)\s+WHERE\b', sql, re.IGNORECASE)
    if not m:
        # No WHERE clause: capture until end
        m = re.search(r'\bSELECT\s+(.*)', sql, re.IGNORECASE)
    if not m:
        raise ValueError("Missing SELECT clause")
    cols = [c.strip() for c in m.group(1).split(',')]
    if cols == ['*']:
        return None  # means all columns
    for col in cols:
        if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', col):
            raise ValueError(f"Invalid column name: {col}")
    return cols

def _tokenize_where(where_str):
    """Return list of tokens for WHERE clause."""
    # Basic tokenization: fields, operators, values, parentheses, logical ops
    tokens = []
    pos = 0
    length = len(where_str)
    while pos < length:
        ch = where_str[pos]
        if ch.isspace():
            pos += 1
            continue
        # Parentheses
        if ch in '()':
            tokens.append(ch)
            pos += 1
            continue
        # Logical operators
        for op in ('AND', 'OR'):
            if where_str[pos:pos+len(op)].upper() == op:
                tokens.append(op)
                pos += len(op)
                break
        else:
            # Comparison operators
            for op in ('>=', '<=', '!=', '<>', '=', '>', '<'):
                if where_str[pos:pos+len(op)] == op:
                    tokens.append(op)
                    pos += len(op)
                    break
            else:
                # Field name or value (quoted string or number)
                if ch == "'":
                    end = pos + 1
                    while end < length and where_str[end] != "'":
                        # Escape single quote by doubling
                        if where_str[end] == "'" and end + 1 < length and where_str[end+1] == "'":
                            end += 2
                        else:
                            end += 1
                    if end >= length:
                        raise ValueError("Unterminated string literal")
                    tokens.append(where_str[pos:end+1])
                    pos = end + 1
                else:
                    # Read until space or operator
                    start = pos
                    while pos < length and not where_str[pos].isspace() \
                          and not any(where_str.startswith(op, pos) for op in ('>=', '<=', '!=', '<>', '=', '>', '<')) \
                          and where_str[pos] not in '()':
                        pos += 1
                    tokens.append(where_str[start:pos])
    return tokens

def _build_condition(tokens, record):
    """Recursively evaluate condition expression."""
    def eval_expr(index):
        # Parse left operand
        token = tokens[index]
        if token == '(':
            val, next_index = eval_expr(index + 1)
            if tokens[next_index] != ')':
                raise ValueError("Mismatched parentheses")
            return val, next_index + 1
        # left operand should be a field name
        if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', token):
            raise ValueError(f"Invalid field name: {token}")
        left = record.get(token)
        # operator
        op_token = tokens[index + 1]
        if op_token not in _COMPARISONS:
            raise ValueError(f"Unsupported operator: {op_token}")
        comp = _COMPARISONS[op_token]
        # right operand
        right_token = tokens[index + 2]
        if re.match(r"^'.*'$", right_token):
            # strip quotes and handle doubled single quote
            val = right_token[1:-1].replace("''", "'")
        else:
            # try numeric conversion
            try:
                val = int(right_token)
            except ValueError:
                try:
                    val = float(right_token)
                except ValueError:
                    # treat as string literal without quotes
                    val = right_token
        left_val = comp(left, val)
        return left_val, index + 3

    # Now handle logical operators
    def parse_full(index):
        val, next_index = eval_expr(index)
        while next_index < len(tokens) and tokens[next_index] in _LOGICAL:
            logic_op = _LOGICAL[tokens[next_index]]
            right_val, next_index = eval_expr(next_index + 1)
            val = logic_op(val, right_val)
        return val

    result = parse_full(0)
    if result is None:
        raise ValueError("Failed to evaluate WHERE clause")
    return result

def _parse_order_by(sql):
    """Return list of (column, direction) tuples."""
    m = re.search(r'\bORDER\s+BY\b(.*)', sql, re.IGNORECASE)
    if not m:
        return None
    order_part = m.group(1).strip()
    if not order_part:
        return None
    orders = []
    for item in order_part.split(','):
        parts = item.strip().split()
        col = parts[0]
        if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', col):
            raise ValueError(f"Invalid ORDER BY column: {col}")
        direction = parts[1].upper() if len(parts) > 1 else 'ASC'
        if direction not in ('ASC', 'DESC'):
            raise ValueError(f"Invalid ORDER BY direction: {direction}")
        orders.append((col, direction))
    return orders

def handle_sql_query(records, sql_command):
    """
    Execute a simplified SQL-like query on a list of dictionaries.

    Parameters
    ----------
    records : list[dict]
        Dataset to query.
    sql_command : str
        Query string containing SELECT, WHERE and ORDER BY clauses.

    Returns
    -------
    list[dict]
        Query results as a list of dictionaries.

    Raises
    ------
    ValueError
        If the query is malformed or execution fails.
    """
    if not isinstance(records, list):
        raise ValueError("records must be a list")
    for r in records:
        if not isinstance(r, dict):
            raise ValueError("each record must be a dictionary")

    # Normalize whitespace
    sql = re.sub(r'\s+', ' ', sql_command.strip())

    # SELECT clause
    select_cols = _parse_select_clause(sql)

    # WHERE clause
    where_match = re.search(r'\bWHERE\b(.*?)\s*(ORDER\s+BY|$)', sql, re.IGNORECASE)
    filtered = records
    if where_match:
        where_str = where_match.group(1).strip()
        tokens = _tokenize_where(where_str)
        # Apply filter
        filtered = []
        for rec in records:
            try:
                if _build_condition(tokens, rec):
                    filtered.append(rec)
            except Exception as exc:
                raise ValueError(f"WHERE evaluation error: {exc}") from exc

    # ORDER BY clause
    orders = _parse_order_by(sql)
    if orders:
        def sort_key(rec):
            return tuple(
                rec.get(col) for col, _ in orders
            )
        reverse = any(dir == 'DESC' for _, dir in orders)
        filtered.sort(key=sort_key, reverse=reverse)

    # SELECT projection
    if select_cols is None:
        result = filtered
    else:
        result = [{k: rec.get(k) for k in select_cols} for rec in filtered]

    return result