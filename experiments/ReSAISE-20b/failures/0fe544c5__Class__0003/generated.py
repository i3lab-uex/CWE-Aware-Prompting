import re
import operator
from functools import reduce
from typing import List, Dict, Any

# Mapping of supported operators to Python functions
OPERATORS = {
    '=': operator.eq,
    '!=': operator.ne,
    '<': operator.lt,
    '<=': operator.le,
    '>': operator.gt,
    '>=': operator.ge
}

# Supported logical operators
LOGICAL_OPERATORS = {'AND', 'OR'}

def _parse_select_clause(clause: str) -> List[str]:
    """Parse the SELECT clause and return list of column names or ['*']. """
    columns = [c.strip() for c in clause.split(',')]
    if len(columns) == 1 and columns[0] == '*':
        return ['*']
    if any(not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', c) for c in columns):
        raise ValueError(f"Invalid column name(s) in SELECT: {columns}")
    return columns

def _parse_order_by_clause(clause: str) -> (str, bool):
    """Parse ORDER BY clause returning column name and reverse flag."""
    parts = clause.split()
    if len(parts) == 0:
        raise ValueError("ORDER BY clause cannot be empty")
    col = parts[0]
    if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', col):
        raise ValueError(f"Invalid column name in ORDER BY: {col}")
    reverse = False
    if len(parts) > 1:
        dir_part = parts[1].upper()
        if dir_part == 'DESC':
            reverse = True
        elif dir_part != 'ASC':
            raise ValueError(f"Unsupported ORDER BY direction: {dir_part}")
    return col, reverse

def _tokenize_where(condition: str) -> List[str]:
    """Tokenise a WHERE condition into identifiers, operators, values and logical ops."""
    token_spec = [
        ('NUMBER',   r'\b\d+(\.\d*)?\b'),
        ('STRING',   r"'([^'\\]|\\.)*'"),
        ('ID',       r'[A-Za-z_][A-Za-z0-9_]*'),
        ('OP',       r'<=|>=|!=|=|<|>'),
        ('ANDOR',    r'\b(?:AND|OR)\b'),
        ('SKIP',     r'[ \t]+'),
        ('MISMATCH', r'.')
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_spec)
    tokens = []
    for mo in re.finditer(tok_regex, condition):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise ValueError(f"Unexpected token in WHERE clause: {value}")
        tokens.append((kind, value))
    return tokens

def _build_condition_func(tokens: List[Any]):
    """Build a function that evaluates the condition against a record."""
    def parse_atom(i):
        if i >= len(tokens):
            raise ValueError("Incomplete condition in WHERE clause")
        kind, val = tokens[i]
        if kind == 'ID':
            # Expect an operator and a value next
            if i + 2 >= len(tokens):
                raise ValueError("Expected operator and value after column name")
            op_kind, op_val = tokens[i+1]
            if op_kind != 'OP':
                raise ValueError(f"Expected comparison operator after column name, got {op_val}")
            val_kind, val_val = tokens[i+2]
            if val_kind == 'NUMBER':
                comp_value = float(val_val) if '.' in val_val else int(val_val)
            elif val_kind == 'STRING':
                comp_value = bytes(val_val[1:-1], "utf-8").decode("unicode_escape")
            else:
                raise ValueError(f"Unsupported value type in WHERE clause: {val_val}")
            op_func = OPERATORS[op_val]
            column_name = val
            def atom(record, i=[i]):
                try:
                    return op_func(record[column_name], comp_value)
                except KeyError:
                    raise ValueError(f"Column {column_name} not found in record")
            return atom, i+3
        else:
            raise ValueError(f"Unexpected token {val} in WHERE clause")

    def parse_expression(i=0):
        left_func, i = parse_atom(i)
        while i < len(tokens) and tokens[i][0] == 'ANDOR':
            logic_op = tokens[i][1].upper()
            right_func, i = parse_atom(i+1)
            if logic_op == 'AND':
                prev_left_func = left_func
                left_func = lambda rec, lf=prev_left_func, rf=right_func: lf(rec) and rf(rec)
            elif logic_op == 'OR':
                prev_left_func = left_func
                left_func = lambda rec, lf=prev_left_func, rf=right_func: lf(rec) or rf(rec)
            else:
                raise ValueError(f"Unsupported logical operator {logic_op}")
        return left_func

    return parse_expression()

def handle_sql_query(records: List[Dict[str, Any]], sql_command: str) -> List[Dict[str, Any]]:
    """
    Execute a simple SQL-like query on a list of record dictionaries.
    Supports SELECT, WHERE, ORDER BY clauses.
    """
    if not isinstance(records, list) or any(not isinstance(r, dict) for r in records):
        raise ValueError("records must be a list of dictionaries")
    if not isinstance(sql_command, str):
        raise ValueError("sql_command must be a string")

    # Normalize whitespace and remove leading/trailing spaces
    cmd = sql_command.strip()
    # Regex to capture clauses (case-insensitive)
    pattern = re.compile(
        r'''
        ^\s*SELECT\s+(?P<select>.+?)\s+
        (WHERE\s+(?P<where>.+?))?
        (ORDER\s+BY\s+(?P<orderby>.+?))?
        \s*;?\s*$''',
        re.IGNORECASE | re.VERBOSE
    )
    match = pattern.match(cmd)
    if not match:
        raise ValueError("Query is not correctly formed")

    select_clause = match.group('select')
    where_clause = match.group('where')
    orderby_clause = match.group('orderby')

    # SELECT
    selected_columns = _parse_select_clause(select_clause)

    # WHERE
    if where_clause:
        tokens = _tokenize_where(where_clause)
        condition_func = _build_condition_func(tokens)
    else:
        # If no WHERE, all records pass
        condition_func = lambda rec: True

    # Filter records
    try:
        filtered_records = [rec for rec in records if condition_func(rec)]
    except Exception as e:
        raise ValueError(f"Error evaluating WHERE clause: {e}") from e

    # SELECT projection
    if selected_columns == ['*']:
        projected = filtered_records
    else:
        projected = []
        for rec in filtered_records:
            new_rec = {}
            for col in selected_columns:
                if col not in rec:
                    raise ValueError(f"Column {col} not found in record")
                new_rec[col] = rec[col]
            projected.append(new_rec)

    # ORDER BY
    if orderby_clause:
        col, reverse = _parse_order_by_clause(orderby_clause)
        try:
            projected.sort(key=lambda r: r[col], reverse=reverse)
        except KeyError as e:
            raise ValueError(f"Column {col} not found for ORDER BY") from e
        except TypeError as e:
            raise ValueError(f"Cannot order by column {col}: {e}") from e

    return projected