import re
import operator
from functools import reduce
from typing import List, Dict, Any

# Mapping of string operators to actual functions
OPERATORS = {
    '=': operator.eq,
    '!=': operator.ne,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le
}

# Regular expression patterns for parsing the query
SELECT_PATTERN = re.compile(
    r'\s*SELECT\s+(?P<select>[\*\w,\s]+)\s+FROM\s+\w+', re.IGNORECASE)
WHERE_PATTERN = re.compile(
    r'\s+WHERE\s+(?P<where>.+?)\s*(ORDER\s+BY|$)', re.IGNORECASE)
ORDER_BY_PATTERN = re.compile(
    r'\s+ORDER\s+BY\s+(?P<order>\w+)(?:\s+(ASC|DESC))?\s*$', re.IGNORECASE)
# Simple condition pattern: column op value
COND_PATTERN = re.compile(
    r'(?P<col>\w+)\s*(?P<op>=|!=|>|<|>=|<=)\s*(?P<val>.+)', re.IGNORECASE)

def _parse_select_clause(clause: str) -> List[str]:
    clause = clause.strip()
    if clause == '*':
        return ['*']
    cols = [c.strip() for c in clause.split(',')]
    if not all(cols):
        raise ValueError("Invalid SELECT clause")
    return cols

def _parse_where_clause(clause: str):
    # For simplicity, support only a single condition
    match = COND_PATTERN.fullmatch(clause.strip())
    if not match:
        raise ValueError("Unsupported WHERE clause")
    col = match.group('col')
    op_str = match.group('op')
    val_raw = match.group('val').strip()
    # Try to interpret value as int, float or keep string
    try:
        val = int(val_raw)
    except ValueError:
        try:
            val = float(val_raw)
        except ValueError:
            # strip quotes if present
            val = val_raw.strip('\'"')
    op_func = OPERATORS[op_str]
    return lambda record: op_func(record.get(col), val)

def _parse_order_by_clause(clause: str):
    match = ORDER_BY_PATTERN.search('ORDER BY ' + clause)
    if not match:
        raise ValueError("Invalid ORDER BY clause")
    col = match.group('order')
    direction = match.group(2)
    reverse = direction and direction.upper() == 'DESC'
    return col, reverse

def process_sql_request(dataset_records: List[Dict[str, Any]],
                        sql_statement: str) -> List[Dict[str, Any]]:
    """
    Execute a simple SQL-like query on an in-memory list of dictionaries.

    Supports:
        SELECT <columns or *>
        FROM <table>  (table name is ignored)
        WHERE <simple condition>
        ORDER BY <column> [ASC|DESC]

    Parameters
    ----------
    dataset_records : List[Dict[str, Any]]
        The data to query.
    sql_statement : str
        The SQL-like statement.

    Returns
    -------
    List[Dict[str, Any]]
        Query result as a list of dictionaries.

    Raises
    ------
    ValueError
        If the query is malformed or cannot be executed.
    """
    if not isinstance(dataset_records, list):
        raise ValueError("dataset_records must be a list of dicts")
    if not isinstance(sql_statement, str):
        raise ValueError("sql_statement must be a string")

    # ---------- SELECT ----------
    select_match = SELECT_PATTERN.search(sql_statement)
    if not select_match:
        raise ValueError("Missing or malformed SELECT clause")
    selected_cols = _parse_select_clause(select_match.group('select'))

    # ---------- WHERE ----------
    where_func = None
    where_match = WHERE_PATTERN.search(sql_statement)
    if where_match:
        where_clause = where_match.group('where')
        where_func = _parse_where_clause(where_clause)

    # ---------- ORDER BY ----------
    order_by_col, reverse_order = None, False
    order_match = ORDER_BY_PATTERN.search(sql_statement)
    if order_match:
        order_by_col, reverse_order = _parse_order_by_clause(order_match.group('order'))

    # ---------- FILTER ----------
    if where_func:
        filtered = [rec for rec in dataset_records if where_func(rec)]
    else:
        filtered = list(dataset_records)

    # ---------- SORT ----------
    if order_by_col:
        try:
            filtered.sort(key=lambda r: r.get(order_by_col), reverse=reverse_order)
        except TypeError:
            raise ValueError(f"Cannot order by column '{order_by_col}'")

    # ---------- SELECT COLUMNS ----------
    if selected_cols == ['*']:
        result = filtered
    else:
        result = []
        for rec in filtered:
            new_rec = {}
            for col in selected_cols:
                if col not in rec:
                    raise ValueError(f"Column '{col}' does not exist")
                new_rec[col] = rec[col]
            result.append(new_rec)

    return result