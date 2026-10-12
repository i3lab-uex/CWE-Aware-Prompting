import re
import operator
from functools import reduce

# --------------------------------------------------------------------------- #
# Helper functions for parsing and evaluating WHERE conditions                #
# --------------------------------------------------------------------------- #

OPERATORS = {
    '=': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,
    '>=': operator.ge,
    '<=': operator.le,
    '>': operator.gt,
    '<': operator.lt,
}

LOGICAL_OPERATORS = {
    'AND': lambda a, b: a and b,
    'OR':  lambda a, b: a or b,
}

def _tokenize_where(where_clause):
    """
    Tokenize the WHERE clause into a list of (column, op, value) tuples
    and logical operators. Handles simple expressions without parentheses.
    """
    # Remove leading/trailing whitespace
    clause = where_clause.strip()
    if not clause:
        return []

    # Regex to split on AND/OR (case-insensitive)
    parts = re.split(r'\b(AND|OR)\b', clause, flags=re.IGNORECASE)
    tokens = []
    i = 0
    while i < len(parts):
        part = parts[i].strip()
        if part.upper() in LOGICAL_OPERATORS:
            tokens.append(part.upper())
            i += 1
        else:
            # Parse comparison expression: column op value
            match = re.match(r'(?P<col>[\w\.]+)\s*(?P<op>=|!=|<>|<=|>=|<|>)\s*(?P<val>.+)', part)
            if not match:
                raise ValueError(f"Invalid WHERE expression: '{part}'")
            col = match.group('col')
            op = match.group('op')
            val_raw = match.group('val').strip()
            # Convert value to int/float if possible, else strip quotes
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
                    # Treat as string if cannot parse numeric
                    val = val_raw
            tokens.append((col, op, val))
            i += 1
    return tokens

def _evaluate_where(row, tokens):
    """
    Evaluate the list of tokens against a single row.
    """
    if not tokens:
        return True

    def eval_atom(atom):
        col, op, val = atom
        if col not in row:
            raise ValueError(f"Column '{col}' does not exist in dataset")
        return OPERATORS[op](row[col], val)

    # Convert tokens into a list of boolean values and logical operators
    eval_stack = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if isinstance(token, tuple):  # comparison
            eval_stack.append(eval_atom(token))
        else:  # logical operator
            op_func = LOGICAL_OPERATORS[token]
            # Apply to last two boolean results
            if len(eval_stack) < 2:
                raise ValueError("Malformed WHERE clause")
            b2 = eval_stack.pop()
            b1 = eval_stack.pop()
            eval_stack.append(op_func(b1, b2))
        i += 1

    if len(eval_stack) != 1:
        raise ValueError("Malformed WHERE clause")
    return eval_stack[0]

# --------------------------------------------------------------------------- #
# Main function                                                         #
# --------------------------------------------------------------------------- #

def run_sql_query(dataset, sql_query):
    """
    Execute a very small subset of SQL on an in-memory dataset.
    
    Supported syntax:
        SELECT <columns> FROM data WHERE <conditions> ORDER BY <column> [ASC|DESC]
    - SELECT * returns all columns
    - WHERE supports =, !=, <>, >, >=, <, <= and logical AND/OR
    - ORDER BY only ascending (ASC) or descending (DESC)
    
    Parameters
    ----------
    dataset : list[dict]
        The data to query.
    sql_query : str
        The SQL-like query string.

    Returns
    -------
    list[dict]
        Query result rows as dictionaries.

    Raises
    ------
    ValueError
        If the query is malformed or execution fails.
    """
    if not isinstance(dataset, list) or any(not isinstance(r, dict) for r in dataset):
        raise ValueError("dataset must be a list of dictionaries")

    query = sql_query.strip()
    if not query.lower().startswith("select"):
        raise ValueError("Only SELECT queries are supported")

    # Split into main clauses
    select_part, rest = re.split(r'\bfrom\b', query, flags=re.IGNORECASE)[0:2]
    rest = rest.strip()
    # SELECT columns
    select_cols_raw = select_part.replace("select", "", 1).strip()
    if not select_cols_raw:
        raise ValueError("SELECT clause missing columns")
    select_columns = [c.strip() for c in select_cols_raw.split(",")]
    if len(select_columns) == 1 and select_columns[0] == '*':
        selected_all = True
    else:
        selected_all = False

    # WHERE and ORDER BY
    where_clause = ""
    order_by_column = None
    order_desc = False

    # Extract WHERE if present
    where_match = re.search(r'\bwhere\b', rest, flags=re.IGNORECASE)
    if where_match:
        before_where = rest[:where_match.start()].strip()
        after_where = rest[where_match.end():].strip()
        where_clause = before_where
        rest = after_where

    # Extract ORDER BY if present
    order_match = re.search(r'\border by\b', rest, flags=re.IGNORECASE)
    if order_match:
        before_order = rest[:order_match.start()].strip()
        after_order = rest[order_match.end():].strip()
        if before_order:
            raise ValueError("Unexpected tokens before ORDER BY")
        order_by_parts = after_order.split()
        if not order_by_parts:
            raise ValueError("ORDER BY column missing")
        order_by_column = order_by_parts[0]
        if len(order_by_parts) > 1:
            dir_token = order_by_parts[1].upper()
            if dir_token == "DESC":
                order_desc = True
            elif dir_token != "ASC":
                raise ValueError("ORDER BY direction must be ASC or DESC")
    else:
        if rest.strip():
            raise ValueError("Unexpected tokens after WHERE clause")

    # Process dataset
    try:
        where_tokens = _tokenize_where(where_clause) if where_clause else []
    except Exception as e:
        raise ValueError(f"Failed to parse WHERE clause: {e}") from e

    result_rows = []
    for row in dataset:
        try:
            if _evaluate_where(row, where_tokens):
                # Project selected columns
                if selected_all:
                    projected = dict(row)
                else:
                    projected = {col: row.get(col) for col in select_columns}
                result_rows.append(projected)
        except Exception as e:
            raise ValueError(f"Error evaluating row {row}: {e}") from e

    # Order the result
    if order_by_column:
        try:
            result_rows.sort(key=lambda r: r.get(order_by_column), reverse=order_desc)
        except Exception as e:
            raise ValueError(f"Failed to order by column '{order_by_column}': {e}") from e

    return result_rows