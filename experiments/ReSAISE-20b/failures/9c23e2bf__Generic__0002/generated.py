import re
import operator
from functools import reduce
from typing import List, Dict, Any

# Supported binary operators for WHERE clauses
_OP_MAP = {
    '=': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le,
}

def _parse_select(query: str) -> Dict[str, Any]:
    """
    Parse a very small subset of SQL:
        SELECT <columns> FROM <table> [WHERE <condition>] [ORDER BY <column>]
    Returns a dict with keys:
        columns: list of column names or ['*']
        where: tuple (column, op_func, value) or None
        order_by: column name or None
    """
    # Normalise whitespace and uppercase keywords for parsing
    q = re.sub(r'\s+', ' ', query.strip())
    pattern = (
        r'^SELECT\s+(?P<cols>[\*\w,\s]+)\s+FROM\s+\w+'
        r'(?:\s+WHERE\s+(?P<where>.+?))?'
        r'(?:\s+ORDER\s+BY\s+(?P<order>\w+))?$'
    )
    m = re.match(pattern, q, flags=re.IGNORECASE)
    if not m:
        raise ValueError('Invalid query syntax')

    cols = [c.strip() for c in m.group('cols').split(',')]
    if len(cols) == 1 and cols[0] == '*':
        columns = ['*']
    else:
        if not all(cols):
            raise ValueError('Empty column name in SELECT')
        columns = cols

    where_clause = m.group('where')
    order_by = m.group('order')

    where_tuple = None
    if where_clause:
        # Only support a single binary condition for simplicity
        cond_pattern = r'(?P<col>\w+)\s*(?P<op>=|!=|<>|>|<|>=|<=)\s*(?P<val>.+)'
        cond_m = re.match(cond_pattern, where_clause.strip())
        if not cond_m:
            raise ValueError('Unsupported WHERE clause')
        col = cond_m.group('col')
        op_sym = cond_m.group('op')
        val_raw = cond_m.group('val').strip()
        # Try to interpret the value as int, float or strip quotes
        if (val_raw.startswith("'") and val_raw.endswith("'")) or \
           (val_raw.startswith('"') and val_raw.endswith('"')):
            val = val_raw[1:-1]
        else:
            try:
                if '.' in val_raw:
                    val = float(val_raw)
                else:
                    val = int(val_raw)
            except ValueError:
                val = val_raw  # fallback to string
        where_tuple = (col, _OP_MAP[op_sym], val)

    return {
        'columns': columns,
        'where': where_tuple,
        'order_by': order_by
    }

def _apply_where(record: Dict[str, Any], where_tuple) -> bool:
    col, op_func, val = where_tuple
    if col not in record:
        raise ValueError(f"Column '{col}' not found in dataset")
    return op_func(record[col], val)

def _apply_select(record: Dict[str, Any], columns: List[str]) -> Dict[str, Any]:
    if columns == ['*']:
        return record.copy()
    return {col: record[col] for col in columns if col in record}

def run_custom_query(dataset: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
    """
    Execute a limited SQL-like query on an in-memory dataset.

    Parameters
    ----------
    dataset : list of dict
        The data to query.
    query : str
        A SQL-like string supporting SELECT, WHERE (single binary condition) and ORDER BY.

    Returns
    -------
    list of dict
        The query result rows.

    Raises
    ------
    ValueError
        If the query syntax is invalid or columns referenced are missing.
    """
    if not isinstance(dataset, list) or not all(isinstance(r, dict) for r in dataset):
        raise ValueError('Dataset must be a list of dictionaries')

    parsed = _parse_select(query)

    # Filter rows
    if parsed['where']:
        try:
            filtered = [r for r in dataset if _apply_where(r, parsed['where'])]
        except KeyError as exc:
            raise ValueError(f"Missing column in dataset: {exc}") from None
    else:
        filtered = dataset[:]

    # Order rows if requested
    if parsed['order_by']:
        col = parsed['order_by']
        try:
            filtered.sort(key=lambda r: r.get(col))
        except TypeError as exc:
            raise ValueError(f"Cannot order by column '{col}': {exc}") from None

    # Project columns
    result = [_apply_select(r, parsed['columns']) for r in filtered]
    return result