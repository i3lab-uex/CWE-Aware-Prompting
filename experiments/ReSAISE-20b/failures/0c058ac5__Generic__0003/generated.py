import re
import operator
from functools import reduce

# Supported binary operators mapping
_OP_MAP = {
    '=': operator.eq,
    '==': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le
}

def _parse_select(statement):
    """
    Parse the SELECT part of the statement.
    Returns a list of column names or ['*'] for all columns.
    """
    m = re.search(r'^\s*SELECT\s+(.+?)\s+WHERE', statement, re.IGNORECASE | re.DOTALL)
    if not m:
        # No WHERE clause; match SELECT ... (possibly without ORDER BY)
        m = re.search(r'^\s*SELECT\s+(.+?)(?:\s+(ORDER|LIMIT|OFFSET)\b|$)', statement, re.IGNORECASE | re.DOTALL)
        if not m:
            raise ValueError("Invalid SELECT syntax")
    cols = [c.strip() for c in m.group(1).split(',')]
    if len(cols) == 1 and cols[0] == '*':
        return ['*']
    return cols

def _parse_where(statement):
    """
    Parse the WHERE clause.
    Supports simple conditions joined by AND only (no OR).
    Returns a list of tuples: (column, operator_func, value)
    """
    m = re.search(r'\bWHERE\b\s+(.+?)(?:\s+ORDER BY\b|$)', statement, re.IGNORECASE | re.DOTALL)
    if not m:
        return []  # No WHERE clause
    cond_str = m.group(1).strip()
    if not cond_str:
        return []

    # Split by AND (case-insensitive)
    parts = re.split(r'\bAND\b', cond_str, flags=re.IGNORECASE)

    conditions = []
    for part in parts:
        part = part.strip()
        # Find operator
        op_match = re.search(r'(<=|>=|<>|!=|=|<|>)', part)
        if not op_match:
            raise ValueError(f"Unsupported or missing operator in condition: '{part}'")
        op_str = op_match.group(1)
        col, val = part.split(op_str, 1)
        column = col.strip()
        value_raw = val.strip()

        # Try to interpret the value (int, float, or string)
        if re.match(r'^-?\d+(\.\d+)?$', value_raw):
            # Numeric literal
            if '.' in value_raw:
                value = float(value_raw)
            else:
                value = int(value_raw)
        elif re.match(r"^'(.*)'$", value_raw, re.DOTALL):
            # Quoted string
            value = re.match(r"^'(.*)'$", value_raw, re.DOTALL).group(1)
        else:
            # Treat as string without quotes
            value = value_raw

        op_func = _OP_MAP.get(op_str)
        if not op_func:
            raise ValueError(f"Unsupported operator: {op_str}")

        conditions.append((column, op_func, value))
    return conditions

def _parse_order_by(statement):
    """
    Parse ORDER BY clause.
    Returns a tuple: (column, ascending: bool)
    """
    m = re.search(r'\bORDER\s+BY\b\s+(\w+)(?:\s+(ASC|DESC))?', statement, re.IGNORECASE)
    if not m:
        return None
    column = m.group(1).strip()
    direction = m.group(2)
    ascending = True if (direction is None or direction.upper() == 'ASC') else False
    return column, ascending

def _apply_conditions(record, conditions):
    """
    Evaluate all conditions against a single record.
    All must be True (AND logic).
    """
    for column, op_func, value in conditions:
        if column not in record:
            return False
        try:
            if not op_func(record[column], value):
                return False
        except Exception:
            return False
    return True

def submit_user_query(records, sql_statement):
    """
    Execute a simple SQL-like query on the provided list of dictionaries.

    Parameters
    ----------
    records : List[Dict]
        The dataset to query.
    sql_statement : str
        A SQL-like string containing SELECT, WHERE and ORDER BY clauses.

    Returns
    -------
    List[Dict]
        The filtered and ordered result set, with only the selected columns.

    Raises
    ------
    ValueError
        If the query syntax is invalid or execution fails.
    """
    if not isinstance(records, list):
        raise ValueError("records must be a list of dictionaries")
    if not isinstance(sql_statement, str):
        raise ValueError("sql_statement must be a string")

    # Normalize whitespace
    stmt = re.sub(r'\s+', ' ', sql_statement.strip())

    try:
        select_cols = _parse_select(stmt)
        where_conditions = _parse_where(stmt)
        order_info = _parse_order_by(stmt)

        # Filter records
        filtered = [rec for rec in records if _apply_conditions(rec, where_conditions)]

        # Order
        if order_info:
            col, asc = order_info
            try:
                filtered.sort(key=lambda r: r.get(col), reverse=not asc)
            except Exception as e:
                raise ValueError(f"Failed to order by column '{col}': {e}")

        # Project columns
        if select_cols == ['*']:
            result = filtered
        else:
            result = []
            for rec in filtered:
                projected = {}
                for col in select_cols:
                    if col not in rec:
                        raise ValueError(f"Column '{col}' does not exist in record")
                    projected[col] = rec[col]
                result.append(projected)

        return result

    except re.error as e:
        raise ValueError(f"Invalid query syntax: {e}") from None
    except Exception as e:
        raise ValueError(f"Query execution error: {e}") from None