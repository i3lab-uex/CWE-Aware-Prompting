import re
import operator
from functools import cmp_to_key
from typing import List, Dict, Any

# Supported operators for the WHERE clause
OPERATORS = {
    '=': operator.eq,
    '!=': operator.ne,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le
}

def _parse_select_clause(command: str) -> List[str]:
    """Parse the SELECT part and return list of field names."""
    match = re.search(r'^SELECT\s+(.+?)\s+(WHERE|ORDER BY|$)', command, re.IGNORECASE)
    if not match:
        raise ValueError("Malformed SELECT clause")
    fields = [f.strip() for f in match.group(1).split(',')]
    if not all(fields):
        raise ValueError("Empty field in SELECT clause")
    return fields

def _parse_where_clause(command: str) -> List[tuple]:
    """Parse the WHERE part into a list of (field, op, value) tuples."""
    where_match = re.search(r'\bWHERE\b\s+(.+?)(\s+ORDER BY|$)', command, re.IGNORECASE)
    if not where_match:
        return []  # No WHERE clause
    condition_str = where_match.group(1).strip()
    # Support simple conditions joined by AND
    conds = [c.strip() for c in re.split(r'\bAND\b', condition_str, flags=re.IGNORECASE)]
    parsed = []
    for cond in conds:
        # Find operator
        op_match = re.search(r'(=|!=|>=|<=|>|<)', cond)
        if not op_match:
            raise ValueError(f"Unsupported condition: {cond}")
        op = op_match.group(1)
        parts = cond.split(op)
        if len(parts) != 2:
            raise ValueError(f"Malformed condition: {cond}")
        field, value = parts[0].strip(), parts[1].strip()
        # Remove surrounding quotes from string values
        if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
            value = value[1:-1]
        else:
            # Try to interpret as int or float
            try:
                if '.' in value:
                    value = float(value)
                else:
                    value = int(value)
            except ValueError:
                pass  # keep as string
        parsed.append((field, op, value))
    return parsed

def _parse_order_by_clause(command: str) -> List[tuple]:
    """Parse ORDER BY clause into list of (field, ascending) tuples."""
    order_match = re.search(r'\bORDER BY\b\s+(.+)', command, re.IGNORECASE)
    if not order_match:
        return []  # No ORDER BY
    parts = [p.strip() for p in order_match.group(1).split(',')]
    parsed = []
    for part in parts:
        tokens = part.split()
        field = tokens[0]
        ascending = True
        if len(tokens) > 1:
            order = tokens[1].lower()
            if order == 'desc':
                ascending = False
            elif order != 'asc':
                raise ValueError(f"Unknown ordering: {tokens[1]}")
        parsed.append((field, ascending))
    return parsed

def _evaluate_condition(record: Dict[str, Any], cond: tuple) -> bool:
    field, op_symbol, value = cond
    if field not in record:
        raise ValueError(f"Field '{field}' not found in records")
    op_func = OPERATORS[op_symbol]
    return op_func(record[field], value)

def run_sql_query(records: List[Dict[str, Any]], command: str) -> List[Dict[str, Any]]:
    """
    Execute a simplified SQL-like query on an in-memory list of dictionaries.

    Supported syntax:
        SELECT <fields> [WHERE <field op value [AND ...] ] [ORDER BY <field [ASC|DESC]> [, ...]]

    Example:
        SELECT name, age WHERE age >= 18 ORDER BY name DESC
    """
    if not isinstance(records, list) or not all(isinstance(r, dict) for r in records):
        raise ValueError("records must be a list of dictionaries")

    # Normalise whitespace
    cmd = re.sub(r'\s+', ' ', command.strip())

    try:
        fields = _parse_select_clause(cmd)
        where_conditions = _parse_where_clause(cmd)
        order_by = _parse_order_by_clause(cmd)
    except ValueError as e:
        raise ValueError(f"Query parsing error: {e}")

    # Apply WHERE filtering
    if where_conditions:
        filtered = [rec for rec in records if all(_evaluate_condition(rec, c) for c in where_conditions)]
    else:
        filtered = records[:]

    # Apply ORDER BY
    if order_by:
        def cmp(a, b):
            for field, asc in order_by:
                if a.get(field) != b.get(field):
                    result = (a[field] > b[field]) - (a[field] < b[field])
                    return result if asc else -result
            return 0
        filtered.sort(key=cmp_to_key(cmp))

    # Apply SELECT projection
    result = []
    for rec in filtered:
        projected = {f: rec.get(f) for f in fields}
        result.append(projected)

    return result