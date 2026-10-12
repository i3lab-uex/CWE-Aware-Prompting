import re
import operator
from functools import reduce
from typing import List, Dict, Any

# Mapping of string operators to actual Python functions
_COMPARISONS = {
    '=': operator.eq,
    '!=': operator.ne,
    '<': operator.lt,
    '<=': operator.le,
    '>': operator.gt,
    '>=': operator.ge
}

_LOGICAL = {
    'AND': lambda a, b: a and b,
    'OR': lambda a, b: a or b
}


def _tokenize_where(condition: str) -> List[str]:
    """
    Split a WHERE condition into tokens. Tokens are field names, operators,
    literals (numbers or quoted strings), and logical connectors.
    """
    token_pattern = r"""
        (?P<SPACE>\s+) |
        (?P<ANDOR>AND|OR) |
        (?P<OP>=|!=|<=|>=|<|>) |
        (?P<STRING>'[^']*'|"[^"]*") |
        (?P<NUMBER>\d+(\.\d+)?) |
        (?P<ID>[A-Za-z_][A-Za-z0-9_]*) |
        (?P<UNKNOWN>.)
    """
    tokens = []
    for match in re.finditer(token_pattern, condition, re.VERBOSE | re.IGNORECASE):
        kind = match.lastgroup
        value = match.group(kind)
        if kind == 'SPACE':
            continue
        if kind == 'UNKNOWN':
            raise ValueError(f"Unknown token in WHERE clause: {value}")
        tokens.append(value)
    return tokens


def _build_condition_func(tokens: List[str]):
    """
    Convert a list of tokens from the WHERE clause into a function that
    evaluates a single record.
    """
    # We parse tokens left-to-right assuming no parentheses and that
    # logical operators have lower precedence than comparison operators.
    # This is a very simplistic parser suitable for the demo.
    def parse_expr(i: int):
        # Expect field
        if i >= len(tokens):
            raise ValueError("Incomplete WHERE clause")
        field = tokens[i]
        i += 1
        if i >= len(tokens):
            raise ValueError("Incomplete WHERE clause")
        op_token = tokens[i]
        if op_token.upper() not in _COMPARISONS:
            raise ValueError(f"Unsupported operator '{op_token}'")
        op_func = _COMPARISONS[op_token.upper()]
        i += 1
        if i >= len(tokens):
            raise ValueError("Incomplete WHERE clause")
        value_token = tokens[i]
        # Convert literal to int/float/string
        if re.match(r"^'[^']*'$", value_token) or re.match(r'^\"[^\"]*\"$', value_token):
            literal = value_token[1:-1]
        elif re.match(r'^\d+(\.\d+)?$', value_token):
            literal = float(value_token) if '.' in value_token else int(value_token)
        else:
            raise ValueError(f"Unsupported literal '{value_token}'")
        i += 1

        def eval_record(record):
            if field not in record:
                return False
            try:
                return op_func(record[field], literal)
            except Exception:
                return False

        # Handle chained logical operators
        if i < len(tokens):
            next_token = tokens[i].upper()
            if next_token in _LOGICAL:
                i += 1
                right_func, new_i = parse_expr(i)
                combined_func = lambda r: _LOGICAL[next_token](eval_record(r), right_func(r))
                return combined_func, new_i
        return eval_record, i

    func, _ = parse_expr(0)
    return func


def process_sql_request(dataset_records: List[Dict[str, Any]], sql_statement: str) -> List[Dict[str, Any]]:
    """
    Execute a simple SQL-like query against an in-memory list of dictionaries.
    Supported clauses: SELECT, WHERE, ORDER BY.
    """
    if not isinstance(dataset_records, list) or not all(isinstance(r, dict) for r in dataset_records):
        raise ValueError("dataset_records must be a list of dictionaries")

    # Normalize statement
    stmt = sql_statement.strip()
    if not stmt.upper().startswith("SELECT "):
        raise ValueError("Only SELECT statements are supported")

    # Regex to capture SELECT, optional WHERE, optional ORDER BY
    pattern = r"""
        ^SELECT\s+(?P<fields>[\*\w,\s]+)
        (?:\s+WHERE\s+(?P<where>.+?))?
        (?:\s+ORDER\s+BY\s+(?P<order>.+?))?
        \s*;?\s*$
    """
    match = re.match(pattern, stmt, re.IGNORECASE | re.VERBOSE)
    if not match:
        raise ValueError("Malformed SQL statement")

    fields_part = match.group('fields').strip()
    where_part = match.group('where')
    order_part = match.group('order')

    # Parse selected fields
    if fields_part == '*':
        select_fields = None  # all fields
    else:
        select_fields = [f.strip() for f in fields_part.split(',')]
        if not all(select_fields):
            raise ValueError("Invalid field list in SELECT clause")

    # Build where filter function
    if where_part:
        tokens = _tokenize_where(where_part)
        try:
            where_func = _build_condition_func(tokens)
        except Exception as e:
            raise ValueError(f"Error parsing WHERE clause: {e}") from e
    else:
        where_func = lambda r: True

    # Apply filtering
    filtered_records = [rec for rec in dataset_records if where_func(rec)]

    # Apply ordering
    if order_part:
        # Support simple ORDER BY field ASC/DESC, comma-separated
        order_specs = []
        for part in order_part.split(','):
            part = part.strip()
            if not part:
                continue
            tokens = part.split()
            field_name = tokens[0]
            direction = 'ASC'
            if len(tokens) > 1:
                dir_token = tokens[1].upper()
                if dir_token in ('ASC', 'DESC'):
                    direction = dir_token
            order_specs.append((field_name, direction))

        def sort_key(rec):
            return tuple(
                rec.get(field) if dir == 'ASC' else _reverse_value(rec.get(field))
                for field, dir in order_specs
            )

        def _reverse_value(val):
            # For numeric types invert by negative; for others use reverse ordering
            if isinstance(val, (int, float)):
                return -val
            return val  # for strings and others, rely on default ordering

        filtered_records.sort(key=sort_key)
    # Project selected fields
    if select_fields is not None:
        result = [{k: v for k, v in rec.items() if k in select_fields} for rec in filtered_records]
    else:
        result = [rec.copy() for rec in filtered_records]

    return result