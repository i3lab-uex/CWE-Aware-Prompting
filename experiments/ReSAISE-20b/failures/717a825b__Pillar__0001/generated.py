import re
import operator
from functools import reduce
from typing import List, Dict, Any

# Mapping of supported comparison operators to their functions
_COMPARISONS = {
    "=": operator.eq,
    "!=": operator.ne,
    "<>": operator.ne,
    ">": operator.gt,
    ">=": operator.ge,
    "<": operator.lt,
    "<=": operator.le,
}

# Mapping of supported logical operators to their functions
_LOGICALS = {
    "AND": operator.and_,
    "OR": operator.or_,
}

def _parse_condition(cond_str: str):
    """
    Parse a simple condition string into a callable that evaluates the
    condition on a record dictionary.
    Supported format: <field> <op> <value>
    Example: age >= 30
    """
    # Split into tokens, handling quoted strings
    tokens = re.findall(r"(?P<field>\w+)\s*(?P<op>[=!<>]{1,2})\s*(?P<value>.+)", cond_str)
    if not tokens:
        raise ValueError(f"Invalid condition: {cond_str}")
    field, op_symbol, value_raw = tokens[0]
    if op_symbol not in _COMPARISONS:
        raise ValueError(f"Unsupported operator: {op_symbol}")

    # Strip quotes from string values
    value = value_raw.strip()
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        value = value[1:-1]
    else:
        # Try to convert numeric values
        try:
            if "." in value:
                value = float(value)
            else:
                value = int(value)
        except ValueError:
            pass  # keep as string

    cmp_func = _COMPARISONS[op_symbol]

    def condition(record: Dict[str, Any]):
        if field not in record:
            return False
        try:
            return cmp_func(record[field], value)
        except Exception:
            return False

    return condition


def _parse_where_clause(where_str: str):
    """
    Parse a WHERE clause that may contain multiple conditions combined with AND/OR.
    Example: age >= 30 AND name = "Alice"
    """
    # Tokenize by logical operators
    parts = re.split(r"\s+(AND|OR)\s+", where_str, flags=re.IGNORECASE)
    if not parts:
        return lambda record: True

    # Build a list of (condition, logical_op) tuples
    conditions = []
    i = 0
    while i < len(parts):
        cond_str = parts[i]
        condition = _parse_condition(cond_str)
        conditions.append((condition, None))
        i += 1
        if i < len(parts):
            logical_op = parts[i].upper()
            if logical_op not in _LOGICALS:
                raise ValueError(f"Unsupported logical operator: {logical_op}")
            # Attach the logical operator to the previous condition
            conditions[-1] = (condition, logical_op)
            i += 1

    # Build a combined predicate
    def combined(record: Dict[str, Any]):
        result = None
        for cond_func, log_op in conditions:
            current = cond_func(record)
            if result is None:
                result = current
            else:
                # Apply the logical operator between result and current
                if log_op == "AND":
                    result = result and current
                elif log_op == "OR":
                    result = result or current
        return result if result is not None else True

    return combined


def _parse_order_by(order_str: str):
    """
    Parse an ORDER BY clause. Supports optional ASC/DESC.
    Example: age DESC
    """
    tokens = order_str.strip().split()
    if not tokens:
        raise ValueError("ORDER BY clause is empty")
    field = tokens[0]
    direction = "ASC"
    if len(tokens) > 1:
        dir_token = tokens[1].upper()
        if dir_token in ("ASC", "DESC"):
            direction = dir_token
    reverse = direction == "DESC"
    return field, reverse


def execute_custom_query(data: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
    """
    Execute a simple SQL‑like query on a list of dictionaries.

    Supported syntax:
        SELECT <col1>, <col2> [WHERE <condition>] [ORDER BY <field> [ASC|DESC]]

    Parameters
    ----------
    data : list[dict]
        The dataset to query.
    query : str
        The SQL‑like query string.

    Returns
    -------
    list[dict]
        The result of the query.

    Raises
    ------
    ValueError
        If the query is malformed or unsupported.
    """
    if not isinstance(data, list) or any(not isinstance(r, dict) for r in data):
        raise ValueError("data must be a list of dictionaries")

    # Basic regex to capture SELECT, optional WHERE and ORDER BY
    pattern = re.compile(
        r"^\s*SELECT\s+(?P<select>.+?)"
        r"(?:\s+WHERE\s+(?P<where>.+?))?"
        r"(?:\s+ORDER\s+BY\s+(?P<order>.+?))?\s*$",
        re.IGNORECASE,
    )
    match = pattern.match(query)
    if not match:
        raise ValueError("Query does not match expected syntax")

    select_part = match.group("select")
    where_part = match.group("where")
    order_part = match.group("order")

    # Parse selected columns
    select_cols = [col.strip() for col in select_part.split(",")]
    if not all(select_cols):
        raise ValueError("SELECT clause contains empty column names")

    # Build where predicate
    if where_part:
        where_predicate = _parse_where_clause(where_part)
    else:
        where_predicate = lambda record: True

    # Filter data
    filtered = list(filter(where_predicate, data))

    # Build result with selected columns
    result = []
    for rec in filtered:
        res_rec = {}
        for col in select_cols:
            if col == "*":
                # Include all columns
                res_rec.update(rec)
            else:
                if col not in rec:
                    raise ValueError(f"Column '{col}' does not exist in record")
                res_rec[col] = rec[col]
        result.append(res_rec)

    # Order if requested
    if order_part:
        field, reverse = _parse_order_by(order_part)
        # Ensure all records have the ordering field
        for r in result:
            if field not in r:
                raise ValueError(f"Ordering field '{field}' missing from result")
        try:
            result.sort(key=lambda r: r[field], reverse=reverse)
        except TypeError as exc:
            raise ValueError(f"Cannot order by field '{field}': {exc}") from exc

    return result