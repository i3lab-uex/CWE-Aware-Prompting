import re
from typing import List, Dict, Any

def run_sql_query(dataset: List[Dict[str, Any]], sql_query: str) -> List[Dict[str, Any]]:
    """
    Execute a very small subset of SQL on an in‑memory list of dictionaries.
    Supports SELECT, WHERE and ORDER BY clauses.

    Parameters
    ----------
    dataset : list[dict]
        Each dictionary represents a record.
    sql_query : str
        A SQL‑like query. Example:
            "SELECT name, age FROM data WHERE age > 30 ORDER BY age DESC"

    Returns
    -------
    list[dict]
        The query result as a list of dictionaries.

    Raises
    ------
    ValueError
        If the query is malformed or evaluation fails.
    """
    # Basic normalization and removal of semicolons
    query = sql_query.strip().rstrip(';')
    if not query.lower().startswith('select '):
        raise ValueError("Only SELECT queries are supported")

    # Split into parts
    select_part, rest = re.split(r'\bfrom\b', query, flags=re.I)[0], query
    # Extract SELECT columns
    m = re.search(r'\bselect\b\s+(.*?)\s+where', rest, flags=re.I | re.S)
    if m:
        select_cols = [c.strip() for c in m.group(1).split(',')]
    else:
        # No WHERE; try ORDER BY or end
        m = re.search(r'\bselect\b\s+(.*?)\s+order by', rest, flags=re.I | re.S)
        if m:
            select_cols = [c.strip() for c in m.group(1).split(',')]
        else:
            # No WHERE or ORDER BY
            m = re.search(r'\bselect\b\s+(.*)', rest, flags=re.I | re.S)
            if not m:
                raise ValueError("SELECT clause could not be parsed")
            select_cols = [c.strip() for c in m.group(1).split(',')]

    if len(select_cols) == 1 and select_cols[0] == '*':
        select_cols = None  # All columns

    # Parse WHERE clause if present
    where_expr = None
    m = re.search(r'\bwhere\b\s+(.*?)(?:\s+order by|\s*$)', rest, flags=re.I | re.S)
    if m:
        where_expr = m.group(1).strip()

    # Parse ORDER BY clause if present
    order_col = None
    order_desc = False
    m = re.search(r'\border by\b\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(asc|desc)?', rest, flags=re.I)
    if m:
        order_col = m.group(1)
        if m.group(2) and m.group(2).lower() == 'desc':
            order_desc = True

    # Helper to evaluate WHERE expression safely
    def matches_where(record: Dict[str, Any]) -> bool:
        if not where_expr:
            return True
        # Identify identifiers in the expression that are column names
        tokens = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', where_expr)
        local_vars = {tok: record.get(tok) for tok in tokens if tok in record}
        try:
            # Only allow builtins that are safe
            return bool(eval(where_expr, {"__builtins__": None}, local_vars))
        except Exception as e:
            raise ValueError(f"Failed to evaluate WHERE clause: {e}")

    # Filter dataset
    filtered = [r for r in dataset if matches_where(r)]

    # Sort if needed
    if order_col:
        try:
            filtered.sort(key=lambda r: r.get(order_col), reverse=order_desc)
        except Exception as e:
            raise ValueError(f"Failed to sort by '{order_col}': {e}")

    # Project columns
    if select_cols is None:
        result = filtered
    else:
        result = [{k: r.get(k) for k in select_cols} for r in filtered]

    return result