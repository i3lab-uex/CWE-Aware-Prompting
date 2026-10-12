import re
import operator
from functools import reduce

# Supported operators mapping for WHERE clause
OPERATORS = {
    '=': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,          # SQL alternative for NOT EQUAL
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le
}

# Helper to safely parse a single condition (e.g., "age >= 30")
def _parse_condition(cond_str):
    # Regex to capture column, operator, value
    pattern = r'^\s*(?P<col>\w+)\s*'
    for op in sorted(OPERATORS.keys(), key=len, reverse=True):
        pattern += f'(?P<operator>{re.escape(op)})\s*'
    pattern += r'(?P<value>.+?)\s*$'
    match = re.match(pattern, cond_str)
    if not match:
        raise ValueError(f"Invalid condition: {cond_str!r}")

    col = match.group('col')
    op_token = match.group('operator')
    val_raw = match.group('value').strip()

    # Try to interpret value as int or float, otherwise strip quotes
    try:
        val = int(val_raw)
    except ValueError:
        try:
            val = float(val_raw)
        except ValueError:
            # Strip surrounding single/double quotes if present
            if (val_raw.startswith("'") and val_raw.endswith("'")) or \
               (val_raw.startswith('"') and val_raw.endswith('"')):
                val = val_raw[1:-1]
            else:
                val = val_raw  # treat as string without quotes

    return col, OPERATORS[op_token], val


# Evaluate a compound WHERE expression
def _evaluate_where(record, where_clause):
    # Split by AND/OR respecting precedence (AND before OR)
    tokens = re.split(r'\s+(AND|OR)\s+', where_clause, flags=re.IGNORECASE)
    if not tokens:
        return True

    # Build a list of (condition_func, operator) tuples
    funcs = []
    ops = []

    # First token is a condition
    col, op_func, val = _parse_condition(tokens[0])
    funcs.append(lambda rec: op_func(rec.get(col), val))

    # Process remaining tokens
    i = 1
    while i < len(tokens):
        logic_op = tokens[i].upper()
        ops.append(logic_op)
        i += 1
        col, op_func, val = _parse_condition(tokens[i])
        funcs.append(lambda rec: op_func(rec.get(col), val))
        i += 1

    # Evaluate with precedence: AND before OR
    # First resolve all ANDs
    def eval_and(idx):
        result = funcs[idx](record)
        while idx < len(ops) and ops[idx] == 'AND':
            result = result and funcs[idx + 1](record)
            idx += 2
        return result, idx

    # Now combine with ORs
    res, pos = eval_and(0)
    while pos < len(ops):
        if ops[pos] == 'OR':
            res = res or funcs[pos + 1](record)
        pos += 2
    return res


def run_sql_query(dataset, sql_query):
    """
    Execute a very small subset of SQL against an in‑memory list of dictionaries.
    Supported syntax:
        SELECT <columns> [WHERE <condition>] [ORDER BY <column> ASC|DESC]
    Columns can be "*" to select all.
    Conditions support =, !=, <>, >, <, >=, <= and logical AND/OR.
    Order by is simple (single column) with optional ASC/DESC.
    """
    if not isinstance(dataset, list):
        raise ValueError("Dataset must be a list of dictionaries")
    if not isinstance(sql_query, str):
        raise ValueError("Query must be a string")

    # Basic pattern extraction
    query = sql_query.strip()
    select_pat = r'^SELECT\s+(?P<select>[\*\w, ]+)\s+FROM\s+\w+'  # dataset name ignored
    where_pat = r'\sWHERE\s+(?P<where>.+?)\bORDER\b|\s$'
    order_pat = r'\sORDER\s+BY\s+(?P<order>\w+)(\s+(?P<dir>ASC|DESC))?\b'

    # Extract SELECT
    m = re.match(r'^SELECT\s+(?P<select>[\*\w, ]+)', query, flags=re.IGNORECASE)
    if not m:
        raise ValueError("Missing or malformed SELECT clause")
    select_cols = [c.strip() for c in m.group('select').split(',')]
    if len(select_cols) == 1 and select_cols[0] == '*':
        select_all = True
    else:
        select_all = False

    # Extract WHERE if present
    where_clause = None
    m_where = re.search(where_pat, query, flags=re.IGNORECASE)
    if m_where:
        where_clause = m_where.group('where').strip()

    # Extract ORDER BY if present
    order_col = None
    order_dir = 'ASC'
    m_order = re.search(order_pat, query, flags=re.IGNORECASE)
    if m_order:
        order_col = m_order.group('order')
        dir_val = m_order.group('dir')
        if dir_val:
            order_dir = dir_val.upper()

    # Process dataset
    results = []
    for rec in dataset:
        if where_clause and not _evaluate_where(rec, where_clause):
            continue
        # Select columns
        if select_all:
            out_rec = rec.copy()
        else:
            out_rec = {col: rec.get(col) for col in select_cols}
        results.append(out_rec)

    # Order if requested
    if order_col:
        try:
            results.sort(key=lambda r: r.get(order_col), reverse=(order_dir == 'DESC'))
        except TypeError:
            raise ValueError(f"Cannot order by column {order_col!r} due to incomparable types")

    return results