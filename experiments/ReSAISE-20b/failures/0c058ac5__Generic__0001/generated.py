import re
import operator
from functools import reduce

# Mapping of string operators to actual Python functions
OPERATORS = {
    '=': operator.eq,
    '==': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,
    '>=': operator.ge,
    '<=': operator.le,
    '>': operator.gt,
    '<': operator.lt
}

def _parse_value(token: str):
    """Parse a token into int, float or stripped string."""
    # Try integer
    try:
        return int(token)
    except ValueError:
        pass
    # Try float
    try:
        return float(token)
    except ValueError:
        pass
    # Strip quotes if present
    if (token.startswith('"') and token.endswith('"')) or (
        token.startswith("'") and token.endswith("'")
    ):
        return token[1:-1]
    # Return as-is
    return token

def _evaluate_condition(record: dict, key: str, op_str: str, value):
    """Evaluate a simple binary condition."""
    if key not in record:
        raise ValueError(f"Column '{key}' not found in records.")
    op_func = OPERATORS.get(op_str)
    if op_func is None:
        raise ValueError(f"Unsupported operator '{op_str}'.")
    return op_func(record[key], value)

def submit_user_query(records, sql_statement):
    """
    Execute a simple SQL-like query on a list of dictionaries.

    Supported syntax:
        SELECT <cols> [WHERE <key> <op> <value>] [ORDER BY <col> [ASC|DESC]]
    """
    if not isinstance(records, list):
        raise ValueError("records must be a list of dictionaries.")
    if not isinstance(sql_statement, str):
        raise ValueError("sql_statement must be a string.")

    # Basic pattern
    pattern = r"""
        ^\s*SELECT\s+(?P<cols>[\*\w,\s]+)          # columns
        (?:\s+WHERE\s+(?P<where>[^ORDER]+))?     # optional where
        (?:\s+ORDER\s+BY\s+(?P<order>\w+)(?:\s+(?P<dir>ASC|DESC))?)?  # optional order
        \s*$
    """
    match = re.match(pattern, sql_statement, re.IGNORECASE | re.VERBOSE)
    if not match:
        raise ValueError("Invalid query syntax.")

    cols_str = match.group('cols').strip()
    where_clause = match.group('where')
    order_col = match.group('order')
    order_dir = match.group('dir')

    # Determine selected columns
    if cols_str == '*':
        selected_cols = None  # means all columns
    else:
        selected_cols = [c.strip() for c in cols_str.split(',')]
        if not all(selected_cols):
            raise ValueError("Empty column name in SELECT clause.")

    # Parse WHERE condition (single binary condition)
    def filter_func(rec):
        if not where_clause:
            return True
        # Simple regex for key op value
        cond_pat = r'^\s*(?P<key>\w+)\s*(?P<op>==|!=|<>|>=|<=|>|<|=)\s*(?P<val>.+?)\s*$'
        cond_match = re.match(cond_pat, where_clause.strip())
        if not cond_match:
            raise ValueError("Invalid WHERE clause.")
        key = cond_match.group('key')
        op_str = cond_match.group('op')
        val_token = cond_match.group('val').strip()
        val = _parse_value(val_token)
        return _evaluate_condition(rec, key, op_str, val)

    # Apply filtering
    try:
        filtered = list(filter(filter_func, records))
    except Exception as e:
        raise ValueError(f"Error during WHERE evaluation: {e}")

    # Apply ordering
    if order_col:
        reverse = (order_dir and order_dir.upper() == 'DESC')
        try:
            filtered.sort(key=lambda r: r.get(order_col), reverse=reverse)
        except Exception as e:
            raise ValueError(f"Error during ORDER BY: {e}")

    # Build result with selected columns
    if selected_cols is None:
        return filtered

    result = []
    for rec in filtered:
        new_rec = {}
        for col in selected_cols:
            if col not in rec:
                raise ValueError(f"Column '{col}' not found in records.")
            new_rec[col] = rec[col]
        result.append(new_rec)

    return result