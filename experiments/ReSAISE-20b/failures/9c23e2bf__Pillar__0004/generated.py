import re
import operator
from functools import reduce

# Mapping of supported comparison operators to their functions
_OP_MAP = {
    '=': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le,
}

# Regular expressions for parsing the query
_QUERY_RE = re.compile(
    r"""
    ^\s*SELECT\s+(?P<select>[\*\w, ]+)\s*
    (?:WHERE\s+(?P<where>.+?)\s*)?
    (?:ORDER\s+BY\s+(?P<order>\w+)(?:\s+(?P<dir>ASC|DESC))?\s*)?
    ;?\s*$
    """,
    re.IGNORECASE | re.VERBOSE,
)

# Regular expression for parsing individual WHERE conditions
_COND_RE = re.compile(
    r"""
    (?P<field>\w+)\s*
    (?P<op>=|!=|<>|>|<|>=|<=)\s*
    (?P<value>'[^']*'|"[^"]*"|\d+(\.\d+)?)
    """,
    re.IGNORECASE | re.VERBOSE,
)

def _parse_value(raw: str):
    """Convert a string value from the query into an appropriate Python type."""
    if raw.startswith(("'", '"')) and raw.endswith(("'", '"')):
        return raw[1:-1]
    try:
        if '.' in raw:
            return float(raw)
        return int(raw)
    except ValueError:
        raise ValueError(f"Unsupported value format: {raw}")

def _evaluate_condition(record, field, op_str, value):
    """Evaluate a single condition against one record."""
    if field not in record:
        raise ValueError(f"Field '{field}' does not exist in the dataset")
    op_func = _OP_MAP[op_str]
    return op_func(record[field], value)

def run_custom_query(dataset, query):
    """
    Execute a very small subset of SQL on an in‑memory list of dictionaries.

    Parameters
    ----------
    dataset : list[dict]
        The data to query.
    query : str
        A SQL‑like statement (e.g. "SELECT name, age FROM data WHERE age >= 18 ORDER BY name DESC").

    Returns
    -------
    list[dict]
        The query result.

    Raises
    ------
    ValueError
        If the query is malformed or contains unsupported constructs.
    """
    if not isinstance(dataset, list) or any(not isinstance(r, dict) for r in dataset):
        raise ValueError("Dataset must be a list of dictionaries")

    match = _QUERY_RE.match(query)
    if not match:
        raise ValueError("Query format is invalid or unsupported")

    # Parse SELECT clause
    select_part = match.group('select').strip()
    if select_part == '*':
        selected_fields = None  # means all fields
    else:
        selected_fields = [f.strip() for f in select_part.split(',')]
        if not all(re.fullmatch(r'\w+', f) for f in selected_fields):
            raise ValueError("SELECT fields must be simple identifiers")

    # Parse WHERE clause
    where_part = match.group('where')
    conditions = []
    if where_part:
        for cond_match in _COND_RE.finditer(where_part):
            field = cond_match.group('field')
            op_str = cond_match.group('op')
            raw_value = cond_match.group('value')
            value = _parse_value(raw_value)
            conditions.append((field, op_str, value))
        # Ensure the entire WHERE clause was consumed
        combined = ' '.join(m.group(0) for m in _COND_RE.finditer(where_part))
        if combined.replace(' ', '') != where_part.replace(' ', ''):
            raise ValueError("WHERE clause contains unsupported syntax")

    # Apply filtering
    def record_matches(rec):
        return all(_evaluate_condition(rec, f, op, v) for f, op, v in conditions)

    filtered = [rec for rec in dataset if record_matches(rec)]

    # Apply ORDER BY
    order_field = match.group('order')
    if order_field:
        if order_field not in dataset[0]:
            raise ValueError(f"ORDER BY field '{order_field}' does not exist")
        reverse = (match.group('dir') or 'ASC').upper() == 'DESC'
        try:
            filtered.sort(key=lambda r: r[order_field], reverse=reverse)
        except TypeError as exc:
            raise ValueError("Cannot order by field with mixed or incomparable types") from exc

    # Apply SELECT projection
    if selected_fields is not None:
        projected = [{k: rec[k] for k in selected_fields if k in rec} for rec in filtered]
    else:
        projected = [rec.copy() for rec in filtered]

    return projected