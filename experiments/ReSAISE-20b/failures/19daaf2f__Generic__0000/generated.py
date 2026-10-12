import re
import operator
from functools import reduce

# ----------------------------------------------------------------------
# Safe expression evaluator for WHERE clauses
# ----------------------------------------------------------------------
def _eval_expr(expr, record):
    """
    Evaluate a simple boolean expression against a single record.
    Supports:
        - comparisons: ==, !=, <, <=, >, >=
        - logical ops: and, or, not
        - parentheses
    """
    # Tokenize expression into literals and operators
    tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_]*|\d+\.?\d*|==|!=|<=|>=|<|>|and\b|or\b|not\b|\(|\)", expr)
    # Convert tokens to a Python expression using record values
    python_tokens = []
    for tok in tokens:
        if re.match(r"\d+\.?\d*$", tok):  # numeric literal
            python_tokens.append(tok)
        elif tok in ("and", "or", "not"):
            python_tokens.append(tok)
        elif tok in ("==", "!=", "<=", ">=", "<", ">"):
            python_tokens.append(tok)
        elif tok in ("(", ")"):
            python_tokens.append(tok)
        else:  # variable name
            if tok not in record:
                raise ValueError(f"Unknown field '{tok}' in WHERE clause")
            # Convert to a string that will be evaluated as the value
            val = record[tok]
            if isinstance(val, str):
                python_tokens.append(repr(val))
            else:
                python_tokens.append(str(val))

    safe_expr = " ".join(python_tokens)
    try:
        return eval(safe_expr, {"__builtins__": None}, {})
    except Exception as e:
        raise ValueError(f"Failed to evaluate WHERE expression: {e}")

# ----------------------------------------------------------------------
# Main query executor
# ----------------------------------------------------------------------
def run_sql_query(dataset, sql_query):
    """
    Execute a simplified SQL-like query on a list of dictionaries.

    Supported syntax:
        SELECT <columns> [WHERE <condition>] [ORDER BY <column> ASC|DESC]

    Examples:
        SELECT * FROM data
        SELECT name, age WHERE age>30 ORDER BY name DESC

    Parameters:
        dataset (list[dict]): The data to query.
        sql_query (str): The SQL-like query string.

    Returns:
        list[dict]: Query results.
    """
    if not isinstance(dataset, list) or not all(isinstance(r, dict) for r in dataset):
        raise ValueError("dataset must be a list of dictionaries")

    # Basic regex to parse the query
    pattern = re.compile(
        r"""
        ^\s*SELECT\s+(?P<select>[\*\w,\s]+)\s*
        (?:FROM\s+\w+\s*)?                  # optional FROM clause
        (?:WHERE\s+(?P<where>[^;]+?)\s*)?
        (?:ORDER\s+BY\s+(?P<orderby>\w+)\s*(?P<order_dir>ASC|DESC)?\s*)?
        $""",
        re.IGNORECASE | re.VERBOSE,
    )
    match = pattern.match(sql_query)
    if not match:
        raise ValueError("Invalid SQL query format")

    select_part = match.group("select")
    where_part = match.group("where")
    orderby_col = match.group("orderby")
    order_dir = match.group("order_dir") or "ASC"

    # Determine selected columns
    if select_part.strip() == "*":
        selected_cols = None  # all columns
    else:
        selected_cols = [col.strip() for col in select_part.split(",") if col.strip()]
        # Validate column names
        all_keys = set().union(*(r.keys() for r in dataset))
        for col in selected_cols:
            if col not in all_keys:
                raise ValueError(f"Column '{col}' does not exist in dataset")

    # Filter rows
    if where_part:
        filtered = [row for row in dataset if _eval_expr(where_part, row)]
    else:
        filtered = list(dataset)

    # Order rows
    if orderby_col:
        try:
            reverse = order_dir.upper() == "DESC"
            filtered.sort(key=lambda r: r.get(orderby_col), reverse=reverse)
        except Exception as e:
            raise ValueError(f"Failed to sort by column '{orderby_col}': {e}")

    # Project columns
    if selected_cols is not None:
        result = [{k: v for k, v in row.items() if k in selected_cols} for row in filtered]
    else:
        result = [dict(row) for row in filtered]

    return result