import re
import operator
from functools import reduce

# Supported binary operators mapping to functions
OPERATORS = {
    '=': operator.eq,
    '==': operator.eq,
    '<>': operator.ne,
    '!=': operator.ne,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le
}

def _parse_condition(cond_str):
    """
    Parse a simple condition string like `age >= 30` into
    (field, op_func, value). Supports only one comparison.
    """
    # Regex to capture field, operator and literal (int/float/string)
    pattern = r'^\s*(\w+)\s*(' + '|'.join(map(re.escape, OPERATORS.keys())) + r')\s*(.+)\s*$'
    match = re.match(pattern, cond_str)
    if not match:
        raise ValueError(f"Unsupported condition syntax: {cond_str!r}")
    field, op_sym, value_raw = match.groups()
    # Convert literal to int/float or strip quotes
    if (value_raw.startswith('"') and value_raw.endswith('"')) or \
       (value_raw.startswith("'") and value_raw.endswith("'")):
        value = value_raw[1:-1]
    else:
        try:
            if '.' in value_raw:
                value = float(value_raw)
            else:
                value = int(value_raw)
        except ValueError:
            # Treat as string if conversion fails
            value = value_raw.strip()
    return field, OPERATORS[op_sym], value

def _apply_condition(record, cond):
    """
    Evaluate the condition against a single record.
    """
    field, op_func, value = cond
    if field not in record:
        raise ValueError(f"Field {field!r} not present in record")
    return op_func(record[field], value)

def _parse_order_by(order_str):
    """
    Parse ORDER BY clause: `field [ASC|DESC]`
    Returns (field, reverse_bool)
    """
    parts = order_str.strip().split()
    if not parts:
        raise ValueError("ORDER BY clause cannot be empty")
    field = parts[0]
    reverse = False
    if len(parts) > 1:
        dir_ = parts[1].upper()
        if dir_ == 'DESC':
            reverse = True
        elif dir_.upper() != 'ASC':
            raise ValueError(f"Unknown ORDER BY direction: {parts[1]}")
    return field, reverse

def execute_query_cmd(dataset_list, sql_query):
    """
    Execute a very small subset of SQL on an in‑memory dataset.
    
    Supported syntax:
        SELECT <columns> [WHERE <condition>] [ORDER BY <field> [ASC|DESC]]
    
    - <columns> can be * or a comma separated list of keys.
    - <condition> must contain one comparison between a key and a literal
      (int, float or quoted string). No logical operators.
    - ORDER BY sorts the final result by a key, optionally in descending order.
    
    Parameters
    ----------
    dataset_list : list[dict]
        List of records to query.
    sql_query : str
        The SQL‑like command.
    
    Returns
    -------
    list[dict]
        Resulting records after applying SELECT, WHERE and ORDER BY.
    
    Raises
    ------
    ValueError
        If the query is malformed or references unknown keys.
    """
    if not isinstance(dataset_list, list):
        raise ValueError("dataset_list must be a list")
    if not all(isinstance(rec, dict) for rec in dataset_list):
        raise ValueError("All items in dataset_list must be dictionaries")

    # Normalise whitespace and split into clauses
    sql = re.sub(r'\s+', ' ', sql_query.strip())
    if not sql.upper().startswith('SELECT '):
        raise ValueError("Query must start with SELECT")

    # Regex to extract clauses
    pattern = r'^SELECT\s+(?P<cols>[\*\w,\s]+?)\s*(WHERE\s+(?P<where>.+?))?\s*(ORDER BY\s+(?P<order>.+?))?$'
    m = re.match(pattern, sql, re.IGNORECASE)
    if not m:
        raise ValueError("Query syntax is incorrect")

    cols_str = m.group('cols').strip()
    where_clause = m.group('where')
    order_clause = m.group('order')

    # Parse selected columns
    if cols_str == '*':
        select_cols = None  # keep all fields
    else:
        select_cols = [c.strip() for c in cols_str.split(',')]
        # Validate columns against dataset keys
        sample_keys = set()
        for rec in dataset_list:
            sample_keys.update(rec.keys())
        unknown = [c for c in select_cols if c not in sample_keys]
        if unknown:
            raise ValueError(f"Unknown columns requested: {', '.join(unknown)}")

    # Filter records
    if where_clause:
        condition = _parse_condition(where_clause)
        filtered = [rec for rec in dataset_list if _apply_condition(rec, condition)]
    else:
        filtered = list(dataset_list)

    # Sort records
    if order_clause:
        field, reverse = _parse_order_by(order_clause)
        # Ensure the key exists in all records
        if any(field not in rec for rec in filtered):
            raise ValueError(f"ORDER BY field {field!r} not present in all records")
        filtered.sort(key=lambda r: r[field], reverse=reverse)

    # Project columns
    if select_cols is not None:
        result = [{k: rec[k] for k in select_cols} for rec in filtered]
    else:
        result = [dict(rec) for rec in filtered]

    return result