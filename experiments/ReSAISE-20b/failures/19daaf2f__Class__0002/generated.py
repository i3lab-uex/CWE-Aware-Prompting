import re
import operator
from functools import reduce

# Supported comparison operators mapping from string to actual functions
_COMPARISONS = {
    '=': operator.eq,
    '==': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,
    '>': operator.gt,
    '>=': operator.ge,
    '<': operator.lt,
    '<=': operator.le
}

# Supported logical operators mapping from string to actual functions
_LOGICALS = {
    'AND': lambda a, b: a and b,
    'OR':  lambda a, b: a or b
}

def _tokenize_condition(cond_str):
    """
    Very small tokenizer for WHERE clauses.
    Supports identifiers, literals (int/float/string quoted), and operators.
    Returns a list of tokens in order.
    """
    token_spec = [
        ('SKIP',   r'\s+'),
        ('AND',    r'(?i)AND\b'),
        ('OR',     r'(?i)OR\b'),
        ('OP',     r'==|!=|>=|<=|<>|>|<|='),
        ('NUM',    r'\d+(\.\d*)?'),          # integer or float
        ('STR',    r"'([^'\\]|\\.)*'"),      # single quoted string
        ('ID',     r'[A-Za-z_][A-Za-z0-9_]*'),
        ('MISMATCH', r'.')
    ]
    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_spec)
    tokens = []
    for mo in re.finditer(tok_regex, cond_str):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise ValueError(f'Unexpected token in WHERE clause: {value}')
        tokens.append((kind, value))
    return tokens

def _parse_condition(tokens):
    """
    Recursive descent parser for simple boolean expressions.
    Returns a callable that takes a record dict and returns True/False.
    """
    def parse_expr(index):
        # Parse first term
        func, next_index = parse_term(index)
        while next_index < len(tokens) and tokens[next_index][0] in ('AND', 'OR'):
            op_type = tokens[next_index][0]
            next_index += 1
            right_func, next_index = parse_term(next_index)
            left_func = func
            op_func = _LOGICALS[op_type.upper()]
            # Combine into new function
            func = lambda record, lf=left_func, rf=right_func, op=op_func: op(lf(record), rf(record))
        return func, next_index

    def parse_term(index):
        # Expect IDENT OP VALUE
        if index + 2 >= len(tokens):
            raise ValueError('Incomplete condition in WHERE clause')
        id_type, field = tokens[index]
        op_type, op_str = tokens[index + 1]
        val_type, val_raw = tokens[index + 2]

        if id_type != 'ID':
            raise ValueError('Expected identifier in WHERE clause')
        if op_type != 'OP' or op_str not in _COMPARISONS:
            raise ValueError(f'Unsupported comparison operator: {op_str}')

        comp_func = _COMPARISONS[op_str]

        # Convert value to appropriate Python type
        if val_type == 'NUM':
            if '.' in val_raw:
                value = float(val_raw)
            else:
                value = int(val_raw)
        elif val_type == 'STR':
            # Strip quotes and unescape
            value = bytes(val_raw[1:-1], "utf-8").decode("unicode_escape")
        else:
            raise ValueError('Unsupported value type in WHERE clause')

        def eval_func(record, f=field, c=comp_func, v=value):
            if f not in record:
                return False
            try:
                return c(record[f], v)
            except Exception:
                return False

        return eval_func, index + 3

    func, final_index = parse_expr(0)
    if final_index != len(tokens):
        raise ValueError('Could not fully parse WHERE clause')
    return func

def _parse_select_clause(select_part):
    """
    Parse SELECT part to determine which columns to keep.
    Supports '*' for all columns or comma-separated list.
    """
    select_part = select_part.strip()
    if select_part == '*':
        return None  # None indicates all columns
    cols = [c.strip() for c in select_part.split(',')]
    if not all(re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', c) for c in cols):
        raise ValueError('Invalid column name in SELECT clause')
    return cols

def _parse_order_by_clause(order_part):
    """
    Parse ORDER BY clause.
    Supports column name optionally followed by ASC/DESC.
    Returns (column, reverse_bool)
    """
    order_part = order_part.strip()
    parts = order_part.split()
    if not parts:
        raise ValueError('ORDER BY clause is empty')
    col = parts[0]
    if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', col):
        raise ValueError('Invalid column name in ORDER BY clause')
    reverse = False
    if len(parts) > 1:
        dir_ = parts[1].upper()
        if dir_ == 'DESC':
            reverse = True
        elif dir_ != 'ASC':
            raise ValueError('ORDER BY direction must be ASC or DESC')
    return col, reverse

def run_sql_query(dataset, sql_query):
    """
    Execute a limited SQL-like query on an in-memory dataset.

    Parameters
    ----------
    dataset : list[dict]
        The data to query.
    sql_query : str
        Query string.

    Returns
    -------
    list[dict]
        Result rows as dictionaries.

    Raises
    ------
    ValueError
        If the query cannot be parsed or executed.
    """
    if not isinstance(dataset, list) or any(not isinstance(r, dict) for r in dataset):
        raise ValueError('Dataset must be a list of dictionaries')

    # Basic structure: SELECT ... WHERE ... ORDER BY ...
    pattern = re.compile(
        r'^SELECT\s+(?P<select>.+?)\s+'
        r'(WHERE\s+(?P<where>.+?))?\s*'
        r'(ORDER\s+BY\s+(?P<order>.+?))?\s*$',
        re.IGNORECASE | re.DOTALL
    )
    match = pattern.match(sql_query.strip())
    if not match:
        raise ValueError('Query is not a valid SELECT statement')

    select_part = match.group('select')
    where_part = match.group('where')
    order_part = match.group('order')

    # SELECT
    selected_cols = _parse_select_clause(select_part)

    # WHERE
    if where_part:
        tokens = _tokenize_condition(where_part)
        filter_func = _parse_condition(tokens)
    else:
        filter_func = lambda record: True

    # ORDER BY
    if order_part:
        order_col, reverse = _parse_order_by_clause(order_part)
    else:
        order_col, reverse = None, False

    # Apply filter
    try:
        filtered = [record for record in dataset if filter_func(record)]
    except Exception as e:
        raise ValueError(f'Error evaluating WHERE clause: {e}')

    # Apply ordering
    if order_col:
        try:
            filtered.sort(key=lambda r: r.get(order_col, None), reverse=reverse)
        except Exception as e:
            raise ValueError(f'Error during ORDER BY: {e}')

    # Apply projection
    if selected_cols is not None:
        result = [{k: v for k, v in r.items() if k in selected_cols} for r in filtered]
    else:
        result = [dict(r) for r in filtered]

    return result