import re
import operator
from functools import reduce
from typing import List, Dict, Callable, Any

# Mapping of supported comparison operators to functions
COMPARE_OPS: Dict[str, Callable[[Any, Any], bool]] = {
    '=': operator.eq,
    '!=': operator.ne,
    '<': operator.lt,
    '<=': operator.le,
    '>': operator.gt,
    '>=': operator.ge
}

# Mapping of logical operators to functions
LOGICAL_OPS: Dict[str, Callable[[bool, bool], bool]] = {
    'AND': lambda a, b: a and b,
    'OR': lambda a, b: a or b
}

# Regular expressions for parsing the query components
SELECT_RE = re.compile(r'^\s*SELECT\s+(?P<columns>[\w\*,\s]+)\s+', re.IGNORECASE)
WHERE_RE = re.compile(r'\s+WHERE\s+(?P<condition>.+?)\s*(ORDER BY|$)', re.IGNORECASE)
ORDER_BY_RE = re.compile(r'\s+ORDER\s+BY\s+(?P<order>.+?)\s*$', re.IGNORECASE)
# Condition token regex (supports parentheses, identifiers, literals, operators)
COND_TOKEN_RE = re.compile(
    r'\s*(?P<token>\(|\)|AND|OR|!=|<=|>=|=|<|>|[A-Za-z_][\w]*|\d+|\'[^\']*\'|"[^"]*")\s*',
    re.IGNORECASE
)

def _parse_columns(columns_str: str) -> List[str]:
    cols = [c.strip() for c in columns_str.split(',')]
    if not all(cols):
        raise ValueError("Empty column name detected")
    return cols

def _tokenize_condition(cond_str: str) -> List[str]:
    tokens = []
    pos = 0
    while pos < len(cond_str):
        match = COND_TOKEN_RE.match(cond_str, pos)
        if not match:
            raise ValueError(f"Invalid token in WHERE clause at position {pos}")
        tokens.append(match.group('token'))
        pos = match.end()
    return tokens

def _build_condition_ast(tokens: List[str]) -> Callable[[Dict], bool]:
    """
    Convert tokens into a function that evaluates the condition on a record.
    Supports simple infix expressions with AND/OR and parentheses.
    """
    # Shunting-yard algorithm to convert to Reverse Polish Notation
    output_queue: List[str] = []
    operator_stack: List[str] = []

    # Precedence
    precedence = {'OR': 1, 'AND': 2}
    for token in tokens:
        upper = token.upper()
        if upper in ('AND', 'OR'):
            while operator_stack and operator_stack[-1] != '(' and precedence[operator_stack[-1]] >= precedence[upper]:
                output_queue.append(operator_stack.pop())
            operator_stack.append(upper)
        elif token == '(':
            operator_stack.append(token)
        elif token == ')':
            while operator_stack and operator_stack[-1] != '(':
                output_queue.append(operator_stack.pop())
            if not operator_stack or operator_stack[-1] != '(':
                raise ValueError("Mismatched parentheses in WHERE clause")
            operator_stack.pop()  # Remove '('
        else:
            output_queue.append(token)

    while operator_stack:
        if operator_stack[-1] in ('(', ')'):
            raise ValueError("Mismatched parentheses in WHERE clause")
        output_queue.append(operator_stack.pop())

    # Build evaluator from RPN
    def eval_rpn(record: Dict) -> bool:
        stack: List[Any] = []
        for token in output_queue:
            upper = token.upper()
            if upper in LOGICAL_OPS:
                b, a = stack.pop(), stack.pop()
                stack.append(LOGICAL_OPS[upper](a, b))
            elif token in COMPARE_OPS:
                right = stack.pop()
                left = stack.pop()
                # Resolve identifiers to record values
                if isinstance(left, str) and left in record:
                    left = record[left]
                elif isinstance(left, str):
                    # try to interpret as literal string
                    left = _literal_value(left)
                if isinstance(right, str) and right in record:
                    right = record[right]
                elif isinstance(right, str):
                    right = _literal_value(right)
                stack.append(COMPARE_OPS[token](left, right))
            else:
                # Operand: could be identifier or literal
                stack.append(token)
        if len(stack) != 1:
            raise ValueError("Invalid WHERE clause expression")
        return bool(stack[0])

    return eval_rpn

def _literal_value(token: str) -> Any:
    """Convert string literal to int or leave as stripped string."""
    if token.startswith(("'", '"')) and token.endswith(("'", '"')):
        return token[1:-1]
    try:
        return int(token)
    except ValueError:
        pass
    return token

def _parse_order_by(order_str: str) -> List[tuple]:
    """
    Parse ORDER BY clause into a list of (column, ascending) tuples.
    """
    parts = [p.strip() for p in order_str.split(',')]
    orderings = []
    for part in parts:
        if not part:
            continue
        tokens = part.split()
        col = tokens[0]
        asc = True  # default
        if len(tokens) > 1:
            dir_token = tokens[1].upper()
            if dir_token == 'DESC':
                asc = False
            elif dir_token != 'ASC':
                raise ValueError(f"Invalid sort direction: {tokens[1]}")
        orderings.append((col, asc))
    return orderings

def submit_user_query(records: List[Dict], sql_statement: str) -> List[Dict]:
    """
    Execute a simple SQL-like query against an in-memory list of dictionaries.

    Supported syntax:
        SELECT <columns> [WHERE <condition>] [ORDER BY <order>]

    - <columns> is a comma-separated list of keys or '*' for all.
    - <condition> supports =, !=, <, <=, >, >=, AND, OR and parentheses.
    - <order> supports comma-separated column names with optional ASC/DESC.

    Parameters
    ----------
    records : list of dict
        The dataset to query.
    sql_statement : str
        The SQL-like statement.

    Returns
    -------
    list of dict
        Query result as a list of dictionaries (copies of the original).

    Raises
    ------
    ValueError
        If the query is malformed or cannot be executed.
    """
    if not isinstance(records, list) or any(not isinstance(r, dict) for r in records):
        raise ValueError("records must be a list of dictionaries")

    # 1. Parse SELECT
    m = SELECT_RE.match(sql_statement)
    if not m:
        raise ValueError("Query must start with SELECT")
    columns = _parse_columns(m.group('columns'))

    # Remaining part after SELECT
    remaining = sql_statement[m.end():]

    # 2. Parse WHERE (optional)
    where_clause = None
    remaining_after_where = remaining
    m_where = WHERE_RE.search(remaining)
    if m_where:
        where_clause = m_where.group('condition')
        remaining_after_where = remaining[m_where.end():]

    # 3. Parse ORDER BY (optional)
    order_by = []
    m_order = ORDER_BY_RE.search(remaining_after_where)
    if m_order:
        order_by = _parse_order_by(m_order.group('order'))
        remaining_after_where = remaining_after_where[m_order.end():]

    # Any leftover text is invalid
    if remaining_after_where.strip():
        raise ValueError("Unexpected trailing content in query")

    # 4. Filter records
    result = []
    if where_clause:
        tokens = _tokenize_condition(where_clause)
        cond_func = _build_condition_ast(tokens)
        for rec in records:
            try:
                if cond_func(rec):
                    result.append(rec.copy())
            except Exception as e:
                raise ValueError(f"Error evaluating WHERE clause: {e}") from e
    else:
        result = [rec.copy() for rec in records]

    # 5. Select columns
    if columns != ['*']:
        selected = []
        for rec in result:
            new_rec = {}
            for col in columns:
                if col not in rec:
                    raise ValueError(f"Column '{col}' does not exist in record")
                new_rec[col] = rec[col]
            selected.append(new_rec)
        result = selected

    # 6. Order by
    if order_by:
        def sort_key(rec):
            key = []
            for col, asc in order_by:
                if col not in rec:
                    raise ValueError(f"Order column '{col}' missing in record")
                key.append(rec[col])
            return tuple(key)

        try:
            result.sort(key=sort_key, reverse=any(not asc for _, asc in order_by))
        except Exception as e:
            raise ValueError(f"Error sorting results: {e}") from e

    return result