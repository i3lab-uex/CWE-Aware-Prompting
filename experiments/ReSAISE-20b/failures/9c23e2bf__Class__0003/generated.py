import re
import operator
from functools import reduce
from typing import List, Dict, Any

# Supported binary operators mapping to python functions
OPERATORS = {
    '=': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,
    '>': operator.gt,
    '>=': operator.ge,
    '<': operator.lt,
    '<=': operator.le,
}

# Token patterns for parsing
TOKEN_PATTERNS = {
    'SELECT': r'SELECT\s+(?P<fields>[\*\w,\s]+)\s+',
    'FROM': r'FROM\s+\w+\s*',  # dataset name is ignored
    'WHERE': r'WHERE\s+(?P<condition>.+?)\s*(ORDER|$)',
    'ORDER_BY': r'ORDER\s+BY\s+(?P<order_field>\w+)\s*(ASC|DESC)?',
    'FIELD_LIST': r'(?P<field>\w+)\s*(,|$)',
}

def _parse_query(query: str) -> Dict[str, Any]:
    """Parse the SQL-like query into components."""
    q = query.strip().upper()
    # SELECT
    m = re.search(TOKEN_PATTERNS['SELECT'], q, re.IGNORECASE)
    if not m:
        raise ValueError("Query must start with SELECT")
    fields = [f.strip() for f in m.group('fields').split(',')]
    if fields == ['*']:
        fields = None  # means all fields

    # FROM is optional for this simple engine
    # WHERE
    where_clause = None
    m_where = re.search(TOKEN_PATTERNS['WHERE'], q, re.IGNORECASE)
    if m_where:
        where_clause = m_where.group('condition').strip()

    # ORDER BY
    order_by = None
    order_dir = 'ASC'
    m_order = re.search(TOKEN_PATTERNS['ORDER_BY'], q, re.IGNORECASE)
    if m_order:
        order_by = m_order.group('order_field')
        dir_match = re.search(r'\b(ASC|DESC)\b', q, re.IGNORECASE)
        if dir_match:
            order_dir = dir_match.group(1).upper()

    return {
        'fields': fields,
        'where': where_clause,
        'order_by': order_by,
        'order_dir': order_dir
    }

def _build_where_func(condition: str):
    """Build a function that evaluates the where condition."""
    # Simple parser for conditions of form: field OP value
    # Supports AND, OR with short-circuit evaluation
    tokens = re.split(r'\s+(AND|OR)\s+', condition, flags=re.IGNORECASE)
    ops = [tok.strip().upper() for tok in tokens[1::2]]
    exprs = tokens[0::2]

    # Compile each expression
    def parse_expr(expr):
        m = re.match(r'(\w+)\s*(=|!=|<>|>|>=|<|<=)\s*(.+)', expr.strip())
        if not m:
            raise ValueError(f"Invalid condition expression: {expr}")
        field, op_sym, value = m.groups()
        op_func = OPERATORS[op_sym]
        # Try to interpret the value
        try:
            val = int(value)
        except ValueError:
            try:
                val = float(value)
            except ValueError:
                val = value.strip("'\"")  # strip quotes
        def _inner(row):
            return op_func(row.get(field), val)
        return _inner

    expr_funcs = [parse_expr(e) for e in exprs]

    def where_func(row):
        result = expr_funcs[0](row)
        for op, func in zip(ops, expr_funcs[1:]):
            if op == 'AND':
                result = result and func(row)
            else:  # OR
                result = result or func(row)
        return result

    return where_func

def run_custom_query(dataset: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
    """
    Execute a basic SQL-like SELECT query on an in-memory dataset.

    Parameters
    ----------
    dataset : List[Dict[str, Any]]
        The data to query.
    query : str
        A simple SQL-like statement. Supports SELECT, WHERE, ORDER BY.

    Returns
    -------
    List[Dict[str, Any]]
        The result of the query.

    Raises
    ------
    ValueError
        If the query format is invalid or cannot be processed.
    """
    if not isinstance(dataset, list) or any(not isinstance(r, dict) for r in dataset):
        raise ValueError("Dataset must be a list of dictionaries")

    try:
        parsed = _parse_query(query)
    except Exception as e:
        raise ValueError(f"Failed to parse query: {e}")

    # Filter
    if parsed['where']:
        try:
            where_func = _build_where_func(parsed['where'])
        except Exception as e:
            raise ValueError(f"Invalid WHERE clause: {e}")
        filtered = list(filter(where_func, dataset))
    else:
        filtered = dataset.copy()

    # Order
    if parsed['order_by']:
        reverse = parsed['order_dir'] == 'DESC'
        try:
            filtered.sort(key=lambda r: r.get(parsed['order_by']), reverse=reverse)
        except TypeError as e:
            raise ValueError(f"Cannot order by field '{parsed['order_by']}': {e}")

    # Project fields
    if parsed['fields'] is not None:
        result = [{k: v for k, v in r.items() if k in parsed['fields']} for r in filtered]
    else:
        result = [r.copy() for r in filtered]

    return result