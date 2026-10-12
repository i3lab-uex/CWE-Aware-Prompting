import re
import operator
import functools
from typing import List, Dict, Any
import ast

# Supported binary operators for WHERE clauses
OPERATORS = {
    "=": operator.eq,
    "!=": operator.ne,
    "<>": operator.ne,
    ">": operator.gt,
    ">=": operator.ge,
    "<": operator.lt,
    "<=": operator.le,
}

def _parse_value(token: str) -> Any:
    """Convert a token into an appropriate Python value."""
    try:
        # Try to parse as literal (int, float, bool, string)
        return ast.literal_eval(token)
    except Exception:
        # If parsing fails, treat as string
        return token

def _evaluate_condition(record: Dict[str, Any], field: str,
                        op_func, value) -> bool:
    """Evaluate a simple binary condition on a record."""
    if field not in record:
        return False
    try:
        return op_func(record[field], value)
    except Exception:
        # Incompatible types
        return False

def run_custom_query(dataset: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
    """
    Execute a very small subset of SQL-like queries on an in-memory dataset.

    Supported syntax:
        SELECT <columns|*>
        [WHERE <field> <op> <value>]
        [ORDER BY <field> [ASC|DESC]]

    Examples:
        SELECT name, age WHERE age > 30 ORDER BY name DESC
        SELECT * WHERE city = "New York"

    Parameters
    ----------
    dataset : List[Dict[str, Any]]
        The data to query.
    query : str
        The SQL-like statement.

    Returns
    -------
    List[Dict[str, Any]]
        Query result rows as dictionaries.

    Raises
    ------
    ValueError
        If the query is malformed or cannot be processed.
    """
    if not isinstance(dataset, list):
        raise ValueError("dataset must be a list of dictionaries")
    if not isinstance(query, str):
        raise ValueError("query must be a string")

    # Basic tokenization
    tokens = re.sub(r"\s+", " ", query.strip()).split(" ")

    if len(tokens) < 2 or tokens[0].upper() != "SELECT":
        raise ValueError("Query must start with SELECT")

    # Parse selected columns
    try:
        select_index = 1
        where_index = tokens.index("WHERE") if "WHERE" in tokens else len(tokens)
        order_by_index = tokens.index("ORDER") if "ORDER" in tokens else len(tokens)

        select_clause_tokens = tokens[select_index:where_index]
    except ValueError as e:
        raise ValueError("Malformed SELECT clause") from e

    select_clause = " ".join(select_clause_tokens)
    if select_clause.strip() == "*":
        selected_fields = None  # All fields
    else:
        selected_fields = [f.strip() for f in select_clause.split(",")]
        if not all(selected_fields):
            raise ValueError("Invalid column names in SELECT clause")

    # Parse WHERE
    where_condition = None
    if "WHERE" in tokens:
        try:
            where_start = tokens.index("WHERE") + 1
            # Find end of condition (either ORDER or end)
            where_end = tokens.index("ORDER") if "ORDER" in tokens else len(tokens)
            cond_tokens = tokens[where_start:where_end]
            if len(cond_tokens) != 3:
                raise ValueError("Only simple single-condition WHERE supported")
            field, op_token, value_token = cond_tokens
            if op_token not in OPERATORS:
                raise ValueError(f"Unsupported operator {op_token}")
            op_func = OPERATORS[op_token]
            value = _parse_value(value_token)
            where_condition = (field, op_func, value)
        except Exception as e:
            raise ValueError("Malformed WHERE clause") from e

    # Parse ORDER BY
    order_field = None
    reverse_order = False
    if "ORDER" in tokens:
        try:
            order_start = tokens.index("ORDER") + 1
            if tokens[order_start].upper() != "BY":
                raise ValueError("ORDER BY syntax error")
            order_field = tokens[order_start + 1]
            # Optional ASC/DESC
            if len(tokens) > order_start + 2:
                direction = tokens[order_start + 2].upper()
                if direction == "DESC":
                    reverse_order = True
                elif direction != "ASC":
                    raise ValueError("ORDER BY direction must be ASC or DESC")
        except Exception as e:
            raise ValueError("Malformed ORDER BY clause") from e

    # Filter dataset
    result = []
    for record in dataset:
        if not isinstance(record, dict):
            continue  # skip invalid rows
        if where_condition:
            field, op_func, value = where_condition
            if not _evaluate_condition(record, field, op_func, value):
                continue
        # Build projected row
        if selected_fields is None:
            proj = dict(record)
        else:
            proj = {k: record.get(k) for k in selected_fields}
        result.append(proj)

    # Sort if needed
    if order_field:
        try:
            result.sort(key=lambda r: r.get(order_field), reverse=reverse_order)
        except Exception as e:
            raise ValueError(f"Failed to sort by {order_field}") from e

    return result