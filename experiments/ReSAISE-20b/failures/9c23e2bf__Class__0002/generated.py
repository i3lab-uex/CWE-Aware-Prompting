import re
import operator
from functools import reduce

# Supported binary operators for WHERE clause
OPERATORS = {
    '=': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le,
}

# Supported logical operators
LOGICAL_OPERATORS = {'AND', 'OR'}

def _parse_select_clause(clause: str):
    """Parse the SELECT part and return a list of fields or ['*']."""
    fields = [f.strip() for f in clause.split(',')]
    if len(fields) == 1 and fields[0] == '*':
        return ['*']
    for f in fields:
        if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', f):
            raise ValueError(f"Invalid field name: {f}")
    return fields

def _parse_where_clause(clause: str):
    """
    Very small parser for simple WHERE expressions.
    Supports conditions like "field = value" combined with AND/OR.
    Values can be numeric or quoted strings.
    """
    tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_]*|!=|<>|>=|<=|=|<|>|\bAND\b|\bOR\b|'[^']*'|\d+(\.\d*)?", clause, flags=re.IGNORECASE)
    if not tokens:
        raise ValueError("Empty WHERE clause")

    # Convert string numbers to int/float
    def _convert(token):
        if token.isdigit():
            return int(token)
        try:
            return float(token)
        except ValueError:
            pass
        if token.startswith("'") and token.endswith("'"):
            return token[1:-1]
        return token

    def _build_condition(tokens):
        if len(tokens) != 3:
            raise ValueError("Unsupported WHERE condition structure")
        field, op, value = tokens
        if op not in OPERATORS:
            raise ValueError(f"Unsupported operator: {op}")
        return lambda record, f=field, op_func=OPERATORS[op], val=_convert(value): op_func(record.get(f), val)

    # Build list of condition functions and logical operators
    cond_funcs = []
    logic_ops = []

    i = 0
    while i < len(tokens):
        # Condition
        cond_func = _build_condition(tokens[i:i+3])
        cond_funcs.append(cond_func)
        i += 3
        if i < len(tokens):
            logic = tokens[i].upper()
            if logic not in LOGICAL_OPERATORS:
                raise ValueError(f"Unsupported logical operator: {logic}")
            logic_ops.append(logic)
            i += 1

    def _combined(record):
        result = cond_funcs[0](record)
        for op, func in zip(logic_ops, cond_funcs[1:]):
            if op == 'AND':
                result = result and func(record)
            else:
                result = result or func(record)
        return result

    return _combined

def _parse_order_by_clause(clause: str):
    """
    Parse ORDER BY clause.
    Supports optional ASC/DESC per field, defaults to ASC.
    """
    parts = [p.strip() for p in clause.split(',')]
    orders = []
    for part in parts:
        m = re.match(r'^([A-Za-z_][A-Za-z0-9_]*)\s*(ASC|DESC)?$', part, flags=re.IGNORECASE)
        if not m:
            raise ValueError(f"Invalid ORDER BY field: {part}")
        field, order = m.group(1), (m.group(2) or 'ASC').upper()
        orders.append((field, order == 'DESC'))
    return orders

def run_custom_query(dataset: list[dict], query: str) -> list[dict]:
    """
    Execute a very small subset of SQL-like queries on an in-memory dataset.
    Supported syntax:
        SELECT <fields> [WHERE <condition>] [ORDER BY <field> [ASC|DESC], ...]
    Example:
        SELECT name, age WHERE age >= 18 AND status = 'active' ORDER BY age DESC
    """
    if not isinstance(dataset, list):
        raise ValueError("Dataset must be a list of dictionaries")
    if not all(isinstance(r, dict) for r in dataset):
        raise ValueError("All items in dataset must be dictionaries")

    # Basic parsing using regex
    pattern = re.compile(
        r"^\s*SELECT\s+(?P<select>[^W]+?)"
        r"(?:\s+WHERE\s+(?P<where>.+?))?"
        r"(?:\s+ORDER\s+BY\s+(?P<order>.+))?\s*$",
        flags=re.IGNORECASE | re.DOTALL
    )
    m = pattern.match(query)
    if not m:
        raise ValueError("Query format is invalid")

    select_clause = m.group('select').strip()
    where_clause = m.group('where')
    order_clause = m.group('order')

    # SELECT
    fields = _parse_select_clause(select_clause)

    # WHERE
    if where_clause:
        filter_func = _parse_where_clause(where_clause)
        filtered_data = list(filter(filter_func, dataset))
    else:
        filtered_data = dataset[:]

    # ORDER BY
    if order_clause:
        orders = _parse_order_by_clause(order_clause)
        def sort_key(record):
            return tuple(
                (record.get(f),) if not desc else (-record.get(f) if isinstance(record.get(f), (int, float)) else record.get(f))
                for f, desc in orders
            )
        filtered_data.sort(key=sort_key)
    # SELECT fields
    if fields == ['*']:
        result = filtered_data
    else:
        result = [{f: r.get(f) for f in fields} for r in filtered_data]
    return result