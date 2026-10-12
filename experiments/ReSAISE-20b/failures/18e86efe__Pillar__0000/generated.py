import re
import operator
from functools import reduce
from typing import List, Dict, Any

# Mapping of supported comparison operators to the corresponding functions.
_COMPARISONS = {
    '=': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,  # SQL style
    '>': operator.gt,
    '>=': operator.ge,
    '<': operator.lt,
    '<=': operator.le
}

# Supported logical operators.
_LOGICAL = {
    'AND': lambda a, b: a and b,
    'OR': lambda a, b: a or b
}


def _tokenize_where(where_clause: str) -> List[str]:
    """
    Very simple tokenizer for the WHERE clause.
    Splits on spaces but keeps quoted strings together.
    """
    pattern = r"""(?P<token>
        "(?:\\.|[^"])*" |  # double quoted string
        '(?:\\.|[^'])*' |  # single quoted string
        \S+                 # any non-space sequence
    )"""
    tokens = [m.group('token') for m in re.finditer(pattern, where_clause, re.VERBOSE)]
    return tokens


def _parse_where(tokens: List[str]) -> Any:
    """
    Parses the token list into a nested structure representing
    the logical expression tree.  The grammar is very limited:
    <expr> ::= <term> (OR <term>)*
    <term> ::= <factor> (AND <factor>)*
    <factor> ::= <column> <op> <value>
    """
    def parse_factor(idx):
        if idx + 2 >= len(tokens):
            raise ValueError("Incomplete condition in WHERE clause")
        col, op_sym, val = tokens[idx], tokens[idx + 1], tokens[idx + 2]
        if op_sym not in _COMPARISONS:
            raise ValueError(f"Unsupported operator '{op_sym}'")
        # strip quotes from string literals
        if (val.startswith('"') and val.endswith('"')) or \
           (val.startswith("'") and val.endswith("'")):
            val = val[1:-1]
        else:
            # try to interpret as number
            try:
                if '.' in val:
                    val = float(val)
                else:
                    val = int(val)
            except ValueError:
                pass  # keep as string
        return lambda record: _COMPARISONS[op_sym](record.get(col), val), idx + 3

    def parse_term(idx):
        func, next_idx = parse_factor(idx)
        while next_idx < len(tokens) and tokens[next_idx].upper() == 'AND':
            _, next_next = parse_factor(next_idx + 1)
            prev_func = func
            func = lambda record, a=prev_func, b=_parse_where([tokens[next_idx], tokens[next_idx + 1], tokens[next_idx + 2]]]): _LOGICAL['AND'](a(record), b(record))
            next_idx = next_next
        return func, next_idx

    def parse_expr(idx):
        func, next_idx = parse_term(idx)
        while next_idx < len(tokens) and tokens[next_idx].upper() == 'OR':
            _, next_next = parse_term(next_idx + 1)
            prev_func = func
            func = lambda record, a=prev_func, b=_parse_where([tokens[next_idx], tokens[next_idx + 1], tokens[next_idx + 2]]]): _LOGICAL['OR'](a(record), b(record))
            next_idx = next_next
        return func, next_idx

    func, final_idx = parse_expr(0)
    if final_idx != len(tokens):
        raise ValueError("Failed to parse WHERE clause completely")
    return func


def run_user_query(dataset: List[Dict[str, Any]], sql_query: str) -> List[Dict[str, Any]]:
    """
    Execute a very small subset of SQL against an in-memory list of dicts.

    Supports:
        SELECT <columns> FROM <table_name>
            [WHERE <condition>] [ORDER BY <column> ASC|DESC]

    Parameters
    ----------
    dataset : list[dict]
        The data to query.
    sql_query : str
        SQL-like query string.

    Returns
    -------
    list[dict]
        The result set.

    Raises
    ------
    ValueError
        If the query cannot be parsed or executed.
    """
    # Basic regex to parse the supported clauses.
    pattern = r"""
        ^\s*SELECT\s+(?P<columns>[\*\w,\s]+)\s+
        FROM\s+\w+            # table name ignored
        (?:\s+WHERE\s+(?P<where>.+?))?
        (?:\s+ORDER\s+BY\s+(?P<orderby>\w+)(?:\s+(?P<orderdir>ASC|DESC))?)?
        \s*;?\s*$
    """
    match = re.match(pattern, sql_query, re.IGNORECASE | re.VERBOSE)
    if not match:
        raise ValueError("Query format is invalid")

    columns_str = match.group('columns').strip()
    where_clause = match.group('where')
    orderby_col = match.group('orderby')
    orderdir = match.group('orderdir') or 'ASC'

    # Resolve columns
    if columns_str == '*':
        selected_columns = None  # means all keys
    else:
        selected_columns = [col.strip() for col in columns_str.split(',')]
        if not all(selected_columns):
            raise ValueError("Empty column name in SELECT clause")

    # Apply WHERE filter
    if where_clause:
        tokens = _tokenize_where(where_clause)
        try:
            condition_func = _parse_where(tokens)
        except Exception as e:
            raise ValueError(f"Failed to parse WHERE clause: {e}") from e
        filtered = [rec for rec in dataset if condition_func(rec)]
    else:
        filtered = list(dataset)

    # Apply ORDER BY
    if orderby_col:
        reverse = (orderdir.upper() == 'DESC')
        try:
            filtered.sort(key=lambda r: r.get(orderby_col), reverse=reverse)
        except TypeError as e:
            raise ValueError(f"Cannot order by column '{orderby_col}': {e}") from e

    # Apply SELECT projection
    if selected_columns is not None:
        result = [{k: rec.get(k) for k in selected_columns} for rec in filtered]
    else:
        result = [dict(rec) for rec in filtered]

    return result