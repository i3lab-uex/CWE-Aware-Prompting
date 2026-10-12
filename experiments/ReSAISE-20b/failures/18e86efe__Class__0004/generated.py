import re
import operator
from functools import partial
from typing import List, Dict

# Mapping of supported operators in WHERE clauses
_OP_MAP = {
    '=': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le,
}

def _parse_select(query: str) -> List[str]:
    """Extract the list of columns to select."""
    m = re.search(r"SELECT\s+(.+?)\s+WHERE", query, re.IGNORECASE | re.DOTALL)
    if not m:
        raise ValueError("Missing or malformed SELECT clause")
    cols = [c.strip() for c in m.group(1).split(",")]
    if not all(cols):
        raise ValueError("Empty column name in SELECT clause")
    return cols

def _parse_where(query: str) -> List[Dict]:
    """Parse simple WHERE conditions (AND only)."""
    where_part = re.search(r"WHERE\s+(.+?)(?:\s+ORDER BY|$)", query, re.IGNORECASE | re.DOTALL)
    if not where_part:
        return []  # No WHERE clause
    conditions_str = where_part.group(1).strip()
    if not conditions_str:
        return []

    # Split on AND (case-insensitive)
    cond_tokens = re.split(r"\s+AND\s+", conditions_str, flags=re.IGNORECASE)
    conditions = []
    for token in cond_tokens:
        # Find operator
        op_match = None
        for op_sym in sorted(_OP_MAP.keys(), key=len, reverse=True):
            if f" {op_sym} " in token:
                op_match = op_sym
                break
        if not op_match:
            raise ValueError(f"Unsupported or missing operator in condition: '{token}'")
        left, right = token.split(op_match)
        left = left.strip()
        right = right.strip().strip('\'"')  # simple literal handling
        if left not in _OP_MAP:
            raise ValueError(f"Invalid column name '{left}' in WHERE clause")
        conditions.append({"col": left, "op": _OP_MAP[op_match], "val": right})
    return conditions

def _parse_order_by(query: str) -> List[str]:
    """Parse ORDER BY columns."""
    m = re.search(r"ORDER\s+BY\s+(.+)$", query, re.IGNORECASE | re.DOTALL)
    if not m:
        return []  # No ORDER BY
    cols = [c.strip() for c in m.group(1).split(",")]
    if not all(cols):
        raise ValueError("Empty column name in ORDER BY clause")
    return cols

def run_user_query(dataset: List[Dict], sql_query: str) -> List[Dict]:
    """
    Execute a simplified SQL-like query on an in-memory dataset.

    Parameters
    ----------
    dataset : list[dict]
        The data to query.
    sql_query : str
        A string containing a SELECT … WHERE … ORDER BY ... query.

    Returns
    -------
    list[dict]
        The filtered and sorted result set.

    Raises
    ------
    ValueError
        If the query is malformed or execution fails.
    """
    if not isinstance(dataset, list) or not all(isinstance(r, dict) for r in dataset):
        raise ValueError("Dataset must be a list of dictionaries")

    query = sql_query.strip()
    if not query.upper().startswith("SELECT "):
        raise ValueError("Query must start with SELECT")

    # Parse clauses
    try:
        select_cols = _parse_select(query)
        where_conditions = _parse_where(query)
        order_by_cols = _parse_order_by(query)
    except Exception as exc:
        raise ValueError(f"Failed to parse query: {exc}") from exc

    # Validate that selected columns exist in records
    for col in select_cols:
        if not any(col in rec for rec in dataset):
            raise ValueError(f"Selected column '{col}' not found in any record")

    # Apply WHERE filtering
    def _matches(record):
        for cond in where_conditions:
            if cond["col"] not in record:
                return False
            try:
                # Attempt numeric comparison if both sides look like numbers
                val = cond["val"]
                rec_val = record[cond["col"]]
                if isinstance(rec_val, (int, float)) and re.fullmatch(r"-?\d+(\.\d+)?", val):
                    val = float(val) if "." in val else int(val)
                if not cond["op"](rec_val, val):
                    return False
            except Exception:
                return False
        return True

    filtered = [rec for rec in dataset if _matches(rec)]

    # Apply ORDER BY sorting
    if order_by_cols:
        def sort_key(record):
            return tuple(record.get(col) for col in order_by_cols)
        filtered.sort(key=sort_key)

    # Project selected columns
    result = [{col: rec.get(col) for col in select_cols} for rec in filtered]
    return result