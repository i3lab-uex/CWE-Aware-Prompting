import re
from typing import List, Dict, Any

# --------------------------------------------------------------------------- #
# Utility helpers
# --------------------------------------------------------------------------- #

def _parse_select_clause(sql: str) -> List[str]:
    """Extract column list from SELECT clause."""
    match = re.search(r"SELECT\s+(.*?)\s+WHERE|SELECT\s+(.*?)\s+ORDER BY|SELECT\s+(.*?);?$", sql, re.IGNORECASE)
    if not match:
        raise ValueError("SELECT clause missing or malformed.")
    cols = match.group(1) or match.group(2) or match.group(3)
    if not cols:
        raise ValueError("No columns specified in SELECT clause.")
    cols = [c.strip() for c in cols.split(",")]
    return cols


def _parse_where_clause(sql: str) -> str:
    """Extract WHERE condition if present."""
    match = re.search(r"WHERE\s+(.*?)\s+ORDER BY|WHERE\s+(.*?);?$", sql, re.IGNORECASE)
    return match.group(1) or match.group(2) if match else ""


def _parse_order_by_clause(sql: str) -> (str, bool):
    """Extract ORDER BY field and direction."""
    match = re.search(r"ORDER\s+BY\s+(\w+)\s*(ASC|DESC)?", sql, re.IGNORECASE)
    if not match:
        return None, True  # default: no order
    field = match.group(1)
    direction = match.group(2) or "ASC"
    ascending = direction.upper() == "ASC"
    return field, ascending


def _evaluate_where(record: Dict[str, Any], condition: str) -> bool:
    """
    Safely evaluate a simple WHERE condition.
    Allowed operators: ==, !=, <, <=, >, >=
    """
    if not condition:
        return True  # no filter

    # Replace field names with record values
    expr = condition
    for key in record:
        # Quote string literals to avoid injection
        value = record[key]
        if isinstance(value, str):
            safe_val = f"'{value.replace(\"'\", \"\\\\'\")}'"
        else:
            safe_val = str(value)
        expr = re.sub(rf"\b{re.escape(key)}\b", safe_val, expr)

    # Only allow safe operators
    if not re.match(r"^[\d\s'<>!=&|().,]+$", expr):
        raise ValueError("Unsafe expression in WHERE clause.")

    try:
        return bool(eval(expr, {"__builtins__": None}, {}))
    except Exception as e:
        raise ValueError(f"Failed to evaluate WHERE clause: {e}")


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def handle_sql_query(records: List[Dict[str, Any]], sql_command: str) -> List[Dict[str, Any]]:
    """
    Execute a simplified SQL-like query on a list of dictionary records.

    Parameters
    ----------
    records : List[Dict[str, Any]]
        Dataset to query.
    sql_command : str
        SQL-like command string.

    Returns
    -------
    List[Dict[str, Any]]
        Query result as a list of dictionaries.

    Raises
    ------
    ValueError
        If the query is malformed or execution fails.
    """
    if not isinstance(records, list) or not all(isinstance(r, dict) for r in records):
        raise ValueError("records must be a list of dictionaries.")

    sql = sql_command.strip().rstrip(";")
    if not sql.lower().startswith("select"):
        raise ValueError("Only SELECT statements are supported.")

    # Parse clauses
    try:
        columns = _parse_select_clause(sql)
        where_cond = _parse_where_clause(sql)
        order_field, ascending = _parse_order_by_clause(sql)
    except Exception as exc:
        raise ValueError(f"Failed to parse SQL command: {exc}") from exc

    # Filter records
    try:
        filtered = [r for r in records if _evaluate_where(r, where_cond)]
    except Exception as exc:
        raise ValueError(f"WHERE clause evaluation error: {exc}") from exc

    # Sort records
    if order_field:
        try:
            filtered.sort(key=lambda r: r.get(order_field), reverse=not ascending)
        except Exception as exc:
            raise ValueError(f"ORDER BY clause error: {exc}") from exc

    # Project columns
    if columns == ["*"]:
        result = filtered
    else:
        result = []
        for rec in filtered:
            projected = {col: rec.get(col) for col in columns}
            result.append(projected)

    return result