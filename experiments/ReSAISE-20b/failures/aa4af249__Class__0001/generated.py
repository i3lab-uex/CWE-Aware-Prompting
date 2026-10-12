import re
import operator
from functools import reduce
from typing import List, Dict, Callable

# Mapping of supported operators for WHERE clause
_OP_MAP = {
    '=': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,
    '>=': operator.ge,
    '<=': operator.le,
    '>': operator.gt,
    '<': operator.lt,
}

# Supported logical operators
_LOGIC_MAP = {
    'AND': lambda a, b: a and b,
    'OR': lambda a, b: a or b,
}

# Regular expressions for parsing the SQL-like query
_SELECT_RE = re.compile(r'\bSELECT\s+(?P<cols>[\w\*,\s]+)\b', re.IGNORECASE)
_FROM_RE = re.compile(r'\bFROM\s+\w+', re.IGNORECASE)  # ignored, just for syntax
_WHERE_RE = re.compile(r'\bWHERE\s+(?P<cond>.+?)(?:\bORDER\b|\z)', re.IGNORECASE | re.DOTALL)
_ORDER_BY_RE = re.compile(r'\bORDER\s+BY\s+(?P<col>\w+)(?:\s+(?P<dir>ASC|DESC))?', re.IGNORECASE)

def _parse_where(cond_str: str) -> Callable[[Dict], bool]:
    """
    Very small expression parser that supports:
      - Comparisons using =, !=, <>, >, >=, <, <=
      - Logical AND/OR (case insensitive)
    It returns a function that takes a record dict and evaluates the condition.
    """
    # Tokenize
    tokens = re.findall(r'\w+|!=|<>|>=|<=|=|>|<|\(|\)', cond_str)
    if not tokens:
        raise ValueError("Empty WHERE clause")

    def parse_expr(index: int) -> (Callable[[Dict], bool], int):
        # Parse a single comparison or parenthesized expression
        if tokens[index] == '(':
            func, idx = parse_expr(index + 1)
            if tokens[idx] != ')':
                raise ValueError("Missing closing parenthesis in WHERE clause")
            return func, idx + 1

        # Expect column
        if not re.match(r'\w+', tokens[index]):
            raise ValueError(f"Expected column name, got '{tokens[index]}'")
        col = tokens[index]
        idx = index + 1

        # Expect operator
        if tokens[idx] not in _OP_MAP:
            raise ValueError(f"Unsupported operator '{tokens[idx]}'")
        op_func = _OP_MAP[tokens[idx]]
        idx += 1

        # Expect value (numeric or quoted string)
        val_token = tokens[idx]
        if re.match(r'\d+(\.\d*)?', val_token):  # number
            val = float(val_token) if '.' in val_token else int(val_token)
        elif re.match(r"'([^']*)'", val_token):
            val = val_token[1:-1]
        else:
            raise ValueError(f"Unsupported value '{val_token}'")
        idx += 1

        def comparison(rec: Dict) -> bool:
            if col not in rec:
                raise ValueError(f"Column '{col}' not found in record")
            return op_func(rec[col], val)

        return comparison, idx

    def parse_logic(index: int) -> (Callable[[Dict], bool], int):
        left_func, idx = parse_expr(index)
        while idx < len(tokens) and tokens[idx].upper() in _LOGIC_MAP:
            logic_op = _LOGIC_MAP[tokens[idx].upper()]
            idx += 1
            right_func, idx = parse_expr(idx)
            prev_left = left_func

            def combined(rec: Dict, l=prev_left, r=right_func, op=logic_op) -> bool:
                return op(l(rec), r(rec))

            left_func = combined
        return left_func, idx

    func, final_idx = parse_logic(0)
    if final_idx != len(tokens):
        raise ValueError("Unexpected tokens in WHERE clause")
    return func

def process_sql_request(dataset_records: List[Dict], sql_statement: str) -> List[Dict]:
    """
    Execute a limited SQL-like query against an in-memory list of dictionaries.

    Supported syntax:
        SELECT <columns> FROM <table> [WHERE <condition>] [ORDER BY <column> [ASC|DESC]]

    - `<columns>` can be '*' or a comma-separated list of column names.
    - `<condition>` supports simple comparisons and logical AND/OR.
    - ORDER BY sorts the final result.

    Raises ValueError on syntax errors or unsupported features.
    """
    if not isinstance(dataset_records, list) or not all(isinstance(r, dict) for r in dataset_records):
        raise ValueError("dataset_records must be a list of dictionaries")

    # Parse SELECT clause
    m = _SELECT_RE.search(sql_statement)
    if not m:
        raise ValueError("Missing or malformed SELECT clause")
    cols_part = m.group('cols').strip()
    if cols_part == '*':
        selected_cols = None  # all columns
    else:
        selected_cols = [c.strip() for c in cols_part.split(',')]
        if not all(re.match(r'\w+', c) for c in selected_cols):
            raise ValueError("Invalid column names in SELECT clause")

    # Verify FROM clause exists (we don't use the table name)
    if not _FROM_RE.search(sql_statement):
        raise ValueError("Missing or malformed FROM clause")

    # Parse WHERE clause if present
    where_func = None
    m_where = _WHERE_RE.search(sql_statement)
    if m_where:
        cond_str = m_where.group('cond').strip()
        where_func = _parse_where(cond_str)

    # Parse ORDER BY clause if present
    order_col, order_dir = None, 'ASC'
    m_order = _ORDER_BY_RE.search(sql_statement)
    if m_order:
        order_col = m_order.group('col')
        dir_token = m_order.group('dir')
        if dir_token:
            order_dir = dir_token.upper()
        if not re.match(r'\w+', order_col):
            raise ValueError("Invalid column name in ORDER BY clause")

    # Apply WHERE filter
    filtered = dataset_records
    if where_func:
        try:
            filtered = [rec for rec in filtered if where_func(rec)]
        except Exception as e:
            raise ValueError(f"Error evaluating WHERE clause: {e}")

    # Apply ORDER BY
    if order_col:
        try:
            filtered.sort(key=lambda r: r.get(order_col), reverse=(order_dir == 'DESC'))
        except Exception as e:
            raise ValueError(f"Error during ORDER BY: {e}")

    # Apply SELECT projection
    if selected_cols is not None:
        result = [{c: rec.get(c) for c in selected_cols} for rec in filtered]
    else:
        result = [dict(rec) for rec in filtered]

    return result