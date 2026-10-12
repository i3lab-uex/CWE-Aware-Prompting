import re
import operator
from functools import reduce

# Mapping of supported operators in WHERE clauses
OPERATORS = {
    '=': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,  # common SQL alias
    '<': operator.lt,
    '<=': operator.le,
    '>': operator.gt,
    '>=': operator.ge,
}

# Regex patterns for parsing
SELECT_RE = re.compile(r'^SELECT\s+(?P<columns>[\*\w,\s]+)\s+FROM\s+\w+', re.IGNORECASE)
WHERE_RE = re.compile(r'WHERE\s+(?P<condition>.+?)\s*(ORDER|$)', re.IGNORECASE)
ORDER_RE = re.compile(r'ORDER\s+BY\s+(?P<column>\w+)(?:\s+(ASC|DESC))?', re.IGNORECASE)

# Tokenize simple WHERE expressions (supports AND, OR)
TOKEN_RE = re.compile(r'\s*(AND|OR|\(|\)|[^\s()]+)\s*', re.IGNORECASE)

def _parse_select(command):
    match = SELECT_RE.search(command)
    if not match:
        raise ValueError("SELECT clause missing or malformed")
    cols = [c.strip() for c in match.group('columns').split(',')]
    if len(cols) == 1 and cols[0] == '*':
        return None  # None indicates all columns
    return cols

def _parse_where(command):
    match = WHERE_RE.search(command)
    if not match:
        return None
    condition_str = match.group('condition')
    tokens = [t.upper() if t.upper() in ('AND', 'OR') else t for t in TOKEN_RE.findall(condition_str)]
    return tokens

def _parse_order(command):
    match = ORDER_RE.search(command)
    if not match:
        return None
    column = match.group('column')
    direction = match.group(3)
    reverse = direction and direction.upper() == 'DESC'
    return column, reverse

def _eval_condition(tokens, record):
    """Evaluate a simple boolean expression from tokens."""
    def eval_atom(tok):
        # Expect format: field operator value
        if tok == '(' or tok == ')':
            return None  # handled in parse
        parts = re.split(r'\s*(=|!=|<>|<=|>=|<|>)\s*', tok, maxsplit=1)
        if len(parts) != 3:
            raise ValueError(f"Invalid condition token: {tok}")
        field, op_sym, val = parts
        if field not in record:
            raise ValueError(f"Field '{field}' not found in record")
        # Try to interpret val as number or strip quotes
        if (val.startswith("'") and val.endswith("'")) or (val.startswith('"') and val.endswith('"')):
            val = val[1:-1]
        else:
            try:
                if '.' in val:
                    val = float(val)
                else:
                    val = int(val)
            except ValueError:
                pass  # keep as string
        op_func = OPERATORS.get(op_sym)
        if not op_func:
            raise ValueError(f"Unsupported operator: {op_sym}")
        return op_func(record[field], val)

    # Convert tokens to Reverse Polish Notation (Shunting-yard) for AND/OR
    precedence = {'AND': 2, 'OR': 1}
    output_queue = []
    op_stack = []

    for tok in tokens:
        if tok.upper() in ('AND', 'OR'):
            while op_stack and op_stack[-1] != '(' and precedence[op_stack[-1]] >= precedence[tok.upper()]:
                output_queue.append(op_stack.pop())
            op_stack.append(tok.upper())
        elif tok == '(':
            op_stack.append(tok)
        elif tok == ')':
            while op_stack and op_stack[-1] != '(':
                output_queue.append(op_stack.pop())
            if not op_stack or op_stack[-1] != '(':
                raise ValueError("Mismatched parentheses in WHERE clause")
            op_stack.pop()
        else:
            output_queue.append(tok)

    while op_stack:
        if op_stack[-1] in ('(', ')'):
            raise ValueError("Mismatched parentheses in WHERE clause")
        output_queue.append(op_stack.pop())

    # Evaluate RPN
    stack = []
    for tok in output_queue:
        if tok.upper() == 'AND':
            b, a = stack.pop(), stack.pop()
            stack.append(a and b)
        elif tok.upper() == 'OR':
            b, a = stack.pop(), stack.pop()
            stack.append(a or b)
        else:
            stack.append(eval_atom(tok))
    if len(stack) != 1:
        raise ValueError("Invalid WHERE clause evaluation")
    return stack[0]

def run_sql_query(records, command):
    """
    Execute a simple SQL-like query on an in-memory list of dictionaries.

    Supported syntax:
        SELECT <columns> FROM <table>
        [WHERE <condition>]
        [ORDER BY <column> [ASC|DESC]]

    The <table> name is ignored; the function operates on the supplied records.
    Columns can be '*' to select all, or a comma‑separated list of keys.

    Parameters
    ----------
    records : List[Dict]
        The dataset to query.
    command : str
        SQL‑like statement.

    Returns
    -------
    List[Dict]
        The query result set.

    Raises
    ------
    ValueError
        If the command is malformed or cannot be executed.
    """
    if not isinstance(records, list):
        raise ValueError("records must be a list")
    if not records:
        return []

    # Normalize whitespace
    cmd = re.sub(r'\s+', ' ', command.strip())

    # Parse SELECT
    cols = _parse_select(cmd)

    # Parse WHERE (optional)
    where_tokens = _parse_where(cmd)

    # Parse ORDER BY (optional)
    order_info = _parse_order(cmd)

    # Filter records
    def record_passes(rec):
        if where_tokens is None:
            return True
        try:
            return _eval_condition(where_tokens, rec)
        except Exception as e:
            raise ValueError(f"Error evaluating WHERE clause: {e}") from None

    filtered = [rec for rec in records if record_passes(rec)]

    # Order results
    if order_info:
        column, reverse = order_info
        try:
            filtered.sort(key=lambda r: r.get(column), reverse=reverse)
        except Exception as e:
            raise ValueError(f"Ordering failed: {e}") from None

    # Project columns
    if cols is not None:
        result = [{k: rec.get(k) for k in cols} for rec in filtered]
    else:
        result = [dict(rec) for rec in filtered]

    return result