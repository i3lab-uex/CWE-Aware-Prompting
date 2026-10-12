import re
import operator
from functools import reduce

# Mapping of supported comparison operators to functions
COMPARATORS = {
    "==": operator.eq,
    "=":  operator.eq,
    "!=": operator.ne,
    "<>": operator.ne,
    ">=": operator.ge,
    "<=": operator.le,
    ">":  operator.gt,
    "<":  operator.lt
}

# Supported logical operators (case‑insensitive)
LOGICAL_OPS = {"AND", "OR"}


def _parse_select_clause(sql: str):
    """Parse the SELECT clause and return a list of column names (or ['*'])."""
    m = re.search(r"SELECT\s+(?P<cols>[\*\w,\s]+)\b", sql, re.IGNORECASE)
    if not m:
        raise ValueError("Missing or malformed SELECT clause.")
    cols = [c.strip() for c in m.group("cols").split(",")]
    if len(cols) == 1 and cols[0] == "*":
        return ["*"]
    if not all(cols):
        raise ValueError("Empty column name in SELECT clause.")
    return cols


def _parse_where_clause(sql: str):
    """Parse the WHERE clause into a list of condition tokens."""
    m = re.search(r"WHERE\s+(?P<cond>.+?)\bORDER BY\b|$",
                  sql, re.IGNORECASE | re.DOTALL)
    if not m:
        return None  # No WHERE clause
    cond_str = m.group("cond").strip()
    if not cond_str:
        return None
    # Split by AND/OR while preserving operators
    tokens = re.split(r"\b(AND|OR)\b", cond_str, flags=re.IGNORECASE)
    tokens = [t.strip() for t in tokens if t.strip()]
    return tokens


def _parse_order_by_clause(sql: str):
    """Parse the ORDER BY clause and return (column, direction)."""
    m = re.search(r"ORDER\s+BY\s+(?P<col>\w+)\s*(?P<dir>ASC|DESC)?\b",
                  sql, re.IGNORECASE)
    if not m:
        return None
    col = m.group("col")
    dir_ = m.group("dir") or "ASC"
    return col, dir_.upper()


def _evaluate_condition(record: dict, token: str):
    """Evaluate a single condition token against a record."""
    # Find comparator
    for comp_str in sorted(COMPARATORS.keys(), key=len, reverse=True):
        if comp_str in token:
            left, right = map(str.strip, token.split(comp_str, 1))
            # Resolve left side
            if left not in record:
                raise ValueError(f"Field '{left}' does not exist.")
            lhs = record[left]
            # Resolve right side
            if (right.startswith("'") and right.endswith("'")) or \
               (right.startswith('"') and right.endswith('"')):
                rhs = right[1:-1]
            else:
                # Try int, float or leave as string
                try:
                    rhs = int(right)
                except ValueError:
                    try:
                        rhs = float(right)
                    except ValueError:
                        rhs = right
            comp_func = COMPARATORS[comp_str]
            return comp_func(lhs, rhs)
    raise ValueError(f"Unsupported condition: {token}")


def _apply_where(records, tokens):
    """Filter records based on WHERE clause tokens."""
    if not tokens:
        return records

    # Build a function that evaluates the entire condition
    def record_match(rec):
        result = None
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token.upper() in LOGICAL_OPS:
                i += 1
                continue
            cond_res = _evaluate_condition(rec, token)
            if result is None:
                result = cond_res
            else:
                op = tokens[i - 1].upper()
                if op == "AND":
                    result = result and cond_res
                elif op == "OR":
                    result = result or cond_res
            i += 1
        return result

    try:
        return [rec for rec in records if record_match(rec)]
    except Exception as exc:
        raise ValueError(f"Failed to evaluate WHERE clause: {exc}") from exc


def _apply_order_by(records, order):
    """Sort records based on ORDER BY clause."""
    if not order:
        return records
    col, dir_ = order
    try:
        return sorted(records,
                      key=lambda r: r.get(col),
                      reverse=(dir_ == "DESC"))
    except Exception as exc:
        raise ValueError(f"Failed to apply ORDER BY: {exc}") from exc


def _apply_select(records, columns):
    """Project records to requested columns."""
    if columns == ["*"]:
        return records
    result = []
    for rec in records:
        try:
            projected = {col: rec[col] for col in columns}
        except KeyError as exc:
            raise ValueError(f"Field {exc.args[0]} not found in record.") from exc
        result.append(projected)
    return result


def handle_sql_query(records, sql_command):
    """
    Execute a simple SQL‑like query on an in‑memory list of dictionaries.

    Parameters
    ----------
    records : list[dict]
        The dataset to query.
    sql_command : str
        A SQL‑like command such as:
            SELECT name, age WHERE age > 20 ORDER BY age DESC

    Returns
    -------
    list[dict]
        The query result.

    Raises
    ------
    ValueError
        If the command is malformed or execution fails.
    """
    if not isinstance(records, list) or not all(isinstance(r, dict) for r in records):
        raise ValueError("records must be a list of dictionaries")

    if not isinstance(sql_command, str):
        raise ValueError("sql_command must be a string")

    # Normalize whitespace
    sql = re.sub(r"\s+", " ", sql_command.strip())

    try:
        select_cols = _parse_select_clause(sql)
        where_tokens = _parse_where_clause(sql)
        order_by = _parse_order_by_clause(sql)

        filtered = _apply_where(records, where_tokens)
        ordered = _apply_order_by(filtered, order_by)
        projected = _apply_select(ordered, select_cols)

        return projected
    except Exception as exc:
        raise ValueError(f"Failed to execute query: {exc}") from exc