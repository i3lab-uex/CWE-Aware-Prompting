import re
import operator
from functools import reduce

# Mapping of comparison operators to functions
_COMPARISONS = {
    '=': operator.eq,
    '!=': operator.ne,
    '<': operator.lt,
    '<=': operator.le,
    '>': operator.gt,
    '>=': operator.ge
}

# Mapping of logical operators to functions
_LOGICALS = {
    'AND': operator.and_,
    'OR': operator.or_
}


def _tokenize_where(where_clause: str):
    """
    Tokenizes a simple WHERE clause into a list of tokens.
    Supports parentheses, AND/OR, and comparisons with literals.
    """
    # Regex for operators and identifiers
    token_spec = [
        ('LPAREN', r'\('),
        ('RPAREN', r'\)'),
        ('ANDOR', r'\b(?:AND|OR)\b'),
        ('COMPARISON', r'!=|<=|>=|=|<|>'),
        ('NUMBER', r'\b-?\d+(\.\d+)?\b'),
        ('STRING', r"'([^']*)'"),
        ('IDENT', r'\b[A-Za-z_][A-Za-z0-9_]*\b'),
        ('SKIP', r'\s+')
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_spec)
    tokens = []
    for mo in re.finditer(tok_regex, where_clause):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'SKIP':
            continue
        elif kind == 'STRING':
            value = mo.group(1)  # capture without quotes
        tokens.append((kind, value))
    return tokens


def _build_condition(tokens):
    """
    Builds a lambda function from the token list that evaluates to True/False
    for a given record.
    Supports only binary comparisons and AND/OR logical operators.
    """
    def parse_expression(index):
        # Parse a simple comparison: IDENT COMPARISON VALUE
        kind, left = tokens[index]
        if kind != 'IDENT':
            raise ValueError(f"Expected field name, got {left}")
        comp_kind, comp = tokens[index + 1]
        if comp_kind != 'COMPARISON':
            raise ValueError(f"Expected comparison operator, got {comp}")
        kind2, right = tokens[index + 2]
        if kind2 not in ('NUMBER', 'STRING'):
            raise ValueError(f"Expected literal value, got {right}")
        # Build the comparison function
        comp_func = _COMPARISONS[comp]
        def cmp(record):
            return comp_func(record.get(left), right)
        index += 3
        # Handle parentheses or logical operators recursively
        while index < len(tokens):
            kind_next, val = tokens[index]
            if kind_next == 'ANDOR':
                op_func = _LOGICALS[val]
                index += 1
                right_cmp, index = parse_expression(index)
                prev_cmp = cmp
                cmp = lambda record, p=prev_cmp, r=right_cmp, o=op_func: o(p(record), r(record))
            elif kind_next == 'RPAREN':
                index += 1
                break
            else:
                break
        return cmp, index

    condition_func, _ = parse_expression(0)
    return condition_func


def run_sql_query(records: list[dict], command: str) -> list[dict]:
    """
    Execute a simplified SQL-like query on a list of record dictionaries.
    Supported syntax:
        SELECT <fields> FROM <table> [WHERE <condition>] [ORDER BY <field> ASC|DESC]
    Example:
        SELECT name, age FROM users WHERE age >= 30 AND city = 'NYC' ORDER BY age DESC
    """
    if not isinstance(records, list) or not all(isinstance(r, dict) for r in records):
        raise ValueError("records must be a list of dictionaries")

    # Basic parsing
    pattern = re.compile(
        r"SELECT\s+(?P<fields>[\w\*, ]+)\s+FROM\s+\w+"
        r"(?:\s+WHERE\s+(?P<where>.+?))?"
        r"(?:\s+ORDER\s+BY\s+(?P<order>\w+)(?:\s+(?P<dir>ASC|DESC))?)?$",
        re.IGNORECASE | re.DOTALL
    )
    match = pattern.match(command.strip())
    if not match:
        raise ValueError("Invalid query format")

    fields_str = match.group('fields').strip()
    where_clause = match.group('where')
    order_field = match.group('order')
    order_dir = match.group('dir')

    # Determine selected fields
    if fields_str == '*':
        selected_fields = None  # all fields
    else:
        selected_fields = [f.strip() for f in fields_str.split(',')]
        # Validate field names
        for f in selected_fields:
            if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', f):
                raise ValueError(f"Invalid field name: {f}")

    # Filter records
    filtered = records
    if where_clause:
        tokens = _tokenize_where(where_clause)
        condition_func = _build_condition(tokens)
        try:
            filtered = [rec for rec in records if condition_func(rec)]
        except Exception as e:
            raise ValueError(f"Error evaluating WHERE clause: {e}")

    # Order records
    if order_field:
        reverse = (order_dir or 'ASC').upper() == 'DESC'
        try:
            filtered.sort(key=lambda r: r.get(order_field), reverse=reverse)
        except Exception as e:
            raise ValueError(f"Error ordering by {order_field}: {e}")

    # Project fields
    if selected_fields is not None:
        result = [{k: rec.get(k) for k in selected_fields} for rec in filtered]
    else:
        result = [dict(rec) for rec in filtered]

    return result