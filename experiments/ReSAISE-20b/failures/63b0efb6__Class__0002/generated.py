import re
import operator
from functools import partial
from typing import Any, Callable, Dict, List

# Mapping of comparison operators to the corresponding function in `operator`
COMPARISONS: Dict[str, Callable[[Any, Any], bool]] = {
    "=": operator.eq,
    "!=": operator.ne,
    "<>": operator.ne,  # SQL alternative for not equal
    ">": operator.gt,
    "<": operator.lt,
    ">=": operator.ge,
    "<=": operator.le,
}

# Regular expression patterns for parsing the SQL‑like statement
SELECT_RE = re.compile(
    r"^\s*SELECT\s+(?P<cols>[\*\w,\s]+)\s*(WHERE\s+(?P<where>[^;]+?))?"
    r"(ORDER\s+BY\s+(?P<order>\w+)(\s+(ASC|DESC))?)?\s*;$",
    re.IGNORECASE,
)

# Pattern to parse a simple condition: column operator value
COND_RE = re.compile(
    r"^\s*(?P<col>\w+)\s*"
    r"(?P<op>=|!=|<>|<=|>=|<|>)\s*"
    r"(?P<val>.+?)\s*$",
    re.IGNORECASE,
)

# Pattern to parse a literal value: quoted string or number
LITERAL_RE = re.compile(
    r"""^\s*
        (?:
            '([^']*)' |          # single quoted string
            "([^"]*)" |          # double quoted string
            (\d+\.\d+|\d+)       # integer or float
        )
    \s*$""",
    re.VERBOSE,
)


def _parse_value(val_str: str) -> Any:
    """Convert a string literal into its Python value."""
    match = LITERAL_RE.match(val_str)
    if not match:
        raise ValueError(f"Invalid literal value: {val_str!r}")
    # The regex captures three groups, only one will be non‑None
    string_val = match.group(1) or match.group(2)
    if string_val is not None:
        return string_val
    numeric_str = match.group(3)
    if "." in numeric_str:
        return float(numeric_str)
    return int(numeric_str)


def _build_condition(cond_str: str) -> Callable[[Dict[str, Any]], bool]:
    """Create a predicate function from a simple condition string."""
    match = COND_RE.match(cond_str)
    if not match:
        raise ValueError(f"Invalid WHERE clause: {cond_str!r}")
    col = match.group("col")
    op_symbol = match.group("op")
    val_str = match.group("val")

    comp_func = COMPARISONS.get(op_symbol)
    if not comp_func:
        raise ValueError(f"Unsupported operator: {op_symbol!r}")

    value = _parse_value(val_str)

    def predicate(record: Dict[str, Any]) -> bool:
        # Missing keys are treated as None
        record_val = record.get(col)
        try:
            return comp_func(record_val, value)
        except TypeError:
            # Incomparable types
            return False

    return predicate


def run_sql_query(records: List[Dict[str, Any]], command: str) -> List[Dict[str, Any]]:
    """
    Execute a very small subset of SQL on an in‑memory list of dictionaries.

    Parameters
    ----------
    records : List[Dict[str, Any]]
        The data set to query.
    command : str
        A SQL‑like statement ending with a semicolon. Supported syntax:

            SELECT <columns> [WHERE <condition>] [ORDER BY <column> [ASC|DESC]];

        * `<columns>` is a comma‑separated list of keys or `*` to select all.
        * `<condition>` is a single comparison: ``column operator value``.
          Operators supported are =, !=, <>, >, <, >=, <=.
        * `<column>` in ORDER BY must be a key present in the records.

    Returns
    -------
    List[Dict[str, Any]]
        The result set after applying the query.

    Raises
    ------
    ValueError
        If the command syntax is invalid or unsupported.
    """
    if not isinstance(records, list):
        raise ValueError("records must be a list of dictionaries")

    # Validate that each record is a dict
    for r in records:
        if not isinstance(r, dict):
            raise ValueError("All items in records must be dictionaries")

    match = SELECT_RE.match(command)
    if not match:
        raise ValueError("Invalid SQL-like command format")

    # Parse selected columns
    cols_raw = match.group("cols").strip()
    if cols_raw == "*":
        selected_cols = None  # Means all columns
    else:
        selected_cols = [c.strip() for c in cols_raw.split(",")]
        if not all(selected_cols):
            raise ValueError("Column names cannot be empty")

    # Build WHERE predicate if present
    where_clause = match.group("where")
    predicate: Callable[[Dict[str, Any]], bool] | None = None
    if where_clause:
        predicate = _build_condition(where_clause)

    # ORDER BY handling
    order_col = match.group("order")
    order_desc = False
    if order_col:
        # Determine ASC/DESC by inspecting the matched part after ORDER BY
        order_match = re.search(r"\bORDER\s+BY\b\s+" + re.escape(order_col) + r"(\s+(ASC|DESC))?", command, re.IGNORECASE)
        if order_match:
            order_desc = bool(order_match.group(2) and order_match.group(2).upper() == "DESC")
        else:
            raise ValueError("Could not parse ORDER BY clause")

    # Filter records
    if predicate:
        filtered = [rec for rec in records if predicate(rec)]
    else:
        filtered = list(records)

    # Order records
    if order_col:
        try:
            filtered.sort(key=lambda r: r.get(order_col), reverse=order_desc)
        except TypeError as exc:
            raise ValueError(f"Cannot order by column '{order_col}': {exc}") from exc

    # Project columns
    if selected_cols is None:
        result = [dict(rec) for rec in filtered]
    else:
        result = [{col: rec.get(col) for col in selected_cols} for rec in filtered]

    return result