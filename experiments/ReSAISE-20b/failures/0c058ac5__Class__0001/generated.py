import re
import operator
from functools import reduce

# Mapping of textual operators to actual functions
OPERATORS = {
    '=': operator.eq,
    '==': operator.eq,
    '<>': operator.ne,
    '!=': operator.ne,
    '>': operator.gt,
    '>=': operator.ge,
    '<': operator.lt,
    '<=': operator.le,
}

# Regular expressions for parsing the query
SELECT_RE = re.compile(r'\s*SELECT\s+(?P<fields>[\w\*,\s]+)\s+FROM\s+\w+', re.IGNORECASE)
WHERE_RE = re.compile(r'\s*WHERE\s+(?P<condition>.+)', re.IGNORECASE)
ORDER_BY_RE = re.compile(r'\s*ORDER\s+BY\s+(?P<field>\w+)(\s+(ASC|DESC))?', re.IGNORECASE)

def _parse_condition(cond_str):
    """
    Parse a simple condition of the form <field> <operator> <value>.
    Supports multiple conditions combined with AND/OR (left‑to‑right evaluation).
    """
    tokens = re.split(r'\s+(AND|OR)\s+', cond_str.strip(), flags=re.IGNORECASE)
    if not tokens:
        raise ValueError("Invalid WHERE clause")
    # Build a list of (field, op_func, value) tuples and connectors
    parts = []
    i = 0
    while i < len(tokens):
        if tokens[i].upper() in ('AND', 'OR'):
            parts.append(tokens[i].upper())
            i += 1
            continue
        # Parse a single condition
        m = re.match(r'(?P<field>\w+)\s*(?P<op>[=!<>]{1,2})\s*(?P<value>.+)', tokens[i])
        if not m:
            raise ValueError(f"Invalid condition: {tokens[i]}")
        field = m.group('field')
        op_str = m.group('op')
        value_raw = m.group('value').strip()
        # Remove surrounding quotes if present
        if (value_raw.startswith("'") and value_raw.endswith("'")) or \
           (value_raw.startswith('"') and value_raw.endswith('"')):
            value = value_raw[1:-1]
        else:
            # Try to interpret as number
            try:
                value = int(value_raw)
            except ValueError:
                try:
                    value = float(value_raw)
                except ValueError:
                    value = value_raw
        op_func = OPERATORS.get(op_str)
        if not op_func:
            raise ValueError(f"Unsupported operator: {op_str}")
        parts.append((field, op_func, value))
        i += 1
    return parts

def _evaluate_condition(record, parts):
    """
    Evaluate the parsed condition against a single record.
    Supports left‑to‑right evaluation of AND/OR without precedence.
    """
    if not parts:
        return True
    # Start with first condition
    field, op_func, value = parts[0]
    result = op_func(record.get(field), value)
    idx = 1
    while idx < len(parts):
        connector = parts[idx]
        field, op_func, value = parts[idx + 1]
        next_val = op_func(record.get(field), value)
        if connector == 'AND':
            result = result and next_val
        else:  # OR
            result = result or next_val
        idx += 2
    return result

def submit_user_query(records, sql_statement):
    """
    Execute a very small subset of SQL on an in‑memory list of dictionaries.
    
    Parameters
    ----------
    records : list[dict]
        The dataset to query.
    sql_statement : str
        SQL‑like statement containing SELECT, optional WHERE and ORDER BY.
    
    Returns
    -------
    list[dict]
        The query result.

    Raises
    ------
    ValueError
        If the statement is malformed or an error occurs during execution.
    """
    if not isinstance(records, list) or not all(isinstance(r, dict) for r in records):
        raise ValueError("records must be a list of dictionaries")

    # 1. Parse SELECT clause
    select_match = SELECT_RE.search(sql_statement)
    if not select_match:
        raise ValueError("Invalid or missing SELECT clause")
    fields_str = select_match.group('fields').strip()
    if fields_str == '*':
        selected_fields = None  # all fields
    else:
        selected_fields = [f.strip() for f in fields_str.split(',')]
        if not all(selected_fields):
            raise ValueError("Invalid field list in SELECT")

    # 2. Parse WHERE clause (optional)
    where_match = WHERE_RE.search(sql_statement)
    condition_parts = []
    if where_match:
        try:
            condition_parts = _parse_condition(where_match.group('condition'))
        except Exception as e:
            raise ValueError(f"WHERE clause error: {e}")

    # 3. Parse ORDER BY clause (optional)
    order_match = ORDER_BY_RE.search(sql_statement)
    order_field = None
    reverse = False
    if order_match:
        order_field = order_match.group('field')
        direction = order_match.group(3)
        if direction and direction.upper() == 'DESC':
            reverse = True

    # 4. Apply filtering
    try:
        filtered = [rec for rec in records if _evaluate_condition(rec, condition_parts)]
    except Exception as e:
        raise ValueError(f"Error evaluating WHERE clause: {e}")

    # 5. Apply ordering
    if order_field:
        try:
            filtered.sort(key=lambda r: r.get(order_field), reverse=reverse)
        except Exception as e:
            raise ValueError(f"Error in ORDER BY: {e}")

    # 6. Apply projection
    if selected_fields is not None:
        result = [{k: rec[k] for k in selected_fields if k in rec} for rec in filtered]
    else:
        result = [rec.copy() for rec in filtered]

    return result