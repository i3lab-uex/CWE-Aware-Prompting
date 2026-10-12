import re
import operator
from functools import reduce
from typing import List, Dict, Callable

# Mapping of simple comparison operators to Python functions
_COMPARISONS: Dict[str, Callable[[any, any], bool]] = {
    '=': operator.eq,
    '==': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,
    '>': operator.gt,
    '>=': operator.ge,
    '<': operator.lt,
    '<=': operator.le
}

# Supported logical connectors
_LOGICALS = {'AND', 'OR'}


def _parse_where_clause(clause: str) -> Callable[[Dict], bool]:
    """
    Convert a WHERE clause string into a predicate function.
    Supports simple expressions with AND / OR and
    comparison operators: =, !=, <>, >, >=, <, <=.
    """
    tokens = re.findall(r"[\w\.]+|[=<>!]+|\(|\)|AND|OR", clause.upper())
    if not tokens:
        raise ValueError("Empty WHERE clause")

    # Convert infix to postfix (Reverse Polish Notation) for evaluation
    precedence = {'OR': 1, 'AND': 2}
    output_queue: List[str] = []
    op_stack: List[str] = []

    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token in _COMPARISONS:
            # Binary comparison: field op value
            if i < 2 or i + 1 >= len(tokens):
                raise ValueError("Malformed comparison in WHERE clause")
            left = tokens[i - 1]
            right = tokens[i + 1]
            # Build a lambda for this comparison
            def cmp_func(record, l=left, op=_COMPARISONS[token], r=right):
                try:
                    lhs = record.get(l)
                    # Try to interpret right side as literal
                    if re.match(r"^'.*'$", r):
                        rhs = r[1:-1]
                    elif re.match(r"^\d+(\.\d*)?$", r):
                        rhs = float(r) if '.' in r else int(r)
                    else:
                        # Assume right side is a field name
                        rhs = record.get(r)
                    return op(lhs, rhs)
                except Exception:
                    return False
            output_queue.append(cmp_func)
            i += 2  # skip right operand
        elif token in _LOGICALS:
            while op_stack and op_stack[-1] in _LOGICALS and precedence[op_stack[-1]] >= precedence[token]:
                output_queue.append(op_stack.pop())
            op_stack.append(token)
        elif token == '(':
            op_stack.append(token)
        elif token == ')':
            while op_stack and op_stack[-1] != '(':
                output_queue.append(op_stack.pop())
            if not op_stack or op_stack[-1] != '(':
                raise ValueError("Mismatched parentheses in WHERE clause")
            op_stack.pop()  # Remove '('
        else:
            # Operand (field or value) is handled with comparison
            pass
        i += 1

    while op_stack:
        if op_stack[-1] in ('(', ')'):
            raise ValueError("Mismatched parentheses in WHERE clause")
        output_queue.append(op_stack.pop())

    # Build final predicate from RPN
    def predicate(record: Dict) -> bool:
        stack = []
        for token in output_queue:
            if callable(token):
                # Binary comparison function
                stack.append(token(record))
            else:  # logical operator
                if len(stack) < 2:
                    raise ValueError("Malformed WHERE clause")
                b = stack.pop()
                a = stack.pop()
                if token == 'AND':
                    stack.append(a and b)
                elif token == 'OR':
                    stack.append(a or b)
        return bool(stack[0]) if stack else True

    return predicate


def run_custom_query(dataset: List[Dict], query: str) -> List[Dict]:
    """
    Execute a simple SQL-like SELECT query on an in-memory dataset.

    Supported syntax:
        SELECT <fields> [WHERE <condition>] [ORDER BY <field> ASC|DESC]

    * <fields> can be '*' or a comma-separated list of keys.
    * <condition> supports =, !=, <>, >, >=, <, <= and logical AND/OR.
    * ORDER BY sorts the resulting rows; default is ASC.

    Parameters
    ----------
    dataset : List[Dict]
        The data to query.
    query : str
        The SQL-like statement.

    Returns
    -------
    List[Dict]
        Query results as a list of dictionaries.

    Raises
    ------
    ValueError
        If the query is malformed or cannot be processed.
    """
    if not isinstance(dataset, list):
        raise ValueError("dataset must be a list of dictionaries")
    if not isinstance(query, str):
        raise ValueError("query must be a string")

    # Normalize query
    q = query.strip()
    if not q.upper().startswith("SELECT "):
        raise ValueError("Only SELECT queries are supported")

    # Split into clauses
    select_part, *rest = re.split(r'\bWHERE\b|\bORDER BY\b', q, flags=re.IGNORECASE)
    select_part = select_part.strip()[len("SELECT "):].strip()

    # Determine selected fields
    if select_part == '*':
        selected_fields = None  # means all fields
    else:
        selected_fields = [f.strip() for f in select_part.split(',')]
        if not all(selected_fields):
            raise ValueError("Empty field names in SELECT clause")

    # Parse WHERE
    where_clause = None
    order_by_field = None
    order_desc = False

    # Extract WHERE clause if present
    where_match = re.search(r'\bWHERE\b(.*?)\bORDER BY\b', q, flags=re.IGNORECASE | re.DOTALL)
    if where_match:
        where_clause = where_match.group(1).strip()
    else:
        # Check if WHERE exists without ORDER BY
        where_match = re.search(r'\bWHERE\b(.*)', q, flags=re.IGNORECASE | re.DOTALL)
        if where_match:
            where_clause = where_match.group(1).strip()

    # Extract ORDER BY
    order_match = re.search(r'\bORDER BY\b(.*)', q, flags=re.IGNORECASE | re.DOTALL)
    if order_match:
        ob = order_match.group(1).strip()
        parts = ob.split()
        if not parts:
            raise ValueError("ORDER BY clause missing field")
        order_by_field = parts[0]
        if len(parts) > 1:
            direction = parts[1].upper()
            if direction == 'DESC':
                order_desc = True
            elif direction != 'ASC':
                raise ValueError("ORDER BY direction must be ASC or DESC")

    # Apply WHERE filter
    result = dataset
    if where_clause:
        predicate = _parse_where_clause(where_clause)
        try:
            result = list(filter(predicate, dataset))
        except Exception as exc:
            raise ValueError(f"Error evaluating WHERE clause: {exc}") from exc

    # Apply ORDER BY
    if order_by_field:
        try:
            result.sort(key=lambda r: r.get(order_by_field), reverse=order_desc)
        except Exception as exc:
            raise ValueError(f"Error sorting by '{order_by_field}': {exc}") from exc

    # Apply SELECT projection
    if selected_fields is not None:
        projected = []
        for row in result:
            new_row = {}
            for f in selected_fields:
                if f not in row:
                    raise ValueError(f"Field '{f}' does not exist in data")
                new_row[f] = row[f]
            projected.append(new_row)
        result = projected

    return result