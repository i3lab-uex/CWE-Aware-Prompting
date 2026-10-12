import re
import operator
from functools import reduce

def submit_user_query(records, sql_statement):
    """
    Execute a simple SQL‑like query on an in‑memory list of dictionaries.

    Supported syntax:
        SELECT <field1>,<field2>,... FROM <table> [WHERE <condition>] [ORDER BY <field> ASC|DESC]

    Conditions support:
        - equality:   field = value
        - inequality: field != value
        - comparison: field <, <=, >, >= value
      Values may be numeric or quoted strings (single or double quotes).

    Parameters
    ----------
    records : list[dict]
        The data set to query.
    sql_statement : str
        The SQL‑like statement.

    Returns
    -------
    list[dict]
        Query result set.

    Raises
    ------
    ValueError
        If the statement cannot be parsed or execution fails.
    """
    # ------------------------------------------------------------------
    # 1. Normalise and validate statement
    # ------------------------------------------------------------------
    stmt = sql_statement.strip()
    if not stmt.upper().startswith("SELECT "):
        raise ValueError("Only SELECT statements are supported")

    # Regex to capture parts
    pattern = re.compile(
        r"""
        ^SELECT\s+(?P<select>[^FROM]+?)\s+          # SELECT fields
        FROM\s+(?P<table>\w+)\s*                   # FROM table name (ignored)
        (?:WHERE\s+(?P<where>.+?)\s*)?             # optional WHERE
        (?:ORDER\s+BY\s+(?P<order>\w+)\s*(?P<dir>ASC|DESC)?)?$  # optional ORDER BY
        """,
        re.IGNORECASE | re.VERBOSE,
    )
    m = pattern.match(stmt)
    if not m:
        raise ValueError("Malformed query")

    select_fields = [f.strip() for f in m.group('select').split(',')]
    where_clause = m.group('where')
    order_field = m.group('order')
    order_dir = m.group('dir') or 'ASC'

    # ------------------------------------------------------------------
    # 2. Prepare WHERE condition
    # ------------------------------------------------------------------
    def parse_value(val):
        """Parse a literal value: number or quoted string."""
        val = val.strip()
        if (val.startswith("'") and val.endswith("'")) or \
           (val.startswith('"') and val.endswith('"')):
            return val[1:-1]
        # Try numeric conversion
        try:
            if '.' in val:
                return float(val)
            return int(val)
        except ValueError:
            raise ValueError(f"Unsupported literal: {val}")

    # Supported operators mapping
    ops_map = {
        '=': operator.eq,
        '!=': operator.ne,
        '<': operator.lt,
        '<=': operator.le,
        '>': operator.gt,
        '>=': operator.ge,
    }

    def build_condition(cond_str):
        """Return a function that evaluates the condition on a record."""
        # Simple split: field op value
        for op_sym in sorted(ops_map, key=len, reverse=True):
            if op_sym in cond_str:
                parts = cond_str.split(op_sym)
                if len(parts) != 2:
                    raise ValueError(f"Invalid condition: {cond_str}")
                field = parts[0].strip()
                value = parse_value(parts[1])
                op_func = ops_map[op_sym]
                return lambda rec, f=field, v=value, op=op_func: op(rec.get(f), v)
        raise ValueError(f"Unsupported operator in condition: {cond_str}")

    # Combine multiple conditions with AND (no OR supported)
    if where_clause:
        cond_parts = [c.strip() for c in re.split(r'\bAND\b', where_clause, flags=re.IGNORECASE)]
        condition_funcs = [build_condition(p) for p in cond_parts]
        def where_predicate(rec):
            return all(f(rec) for f in condition_funcs)
    else:
        where_predicate = lambda rec: True

    # ------------------------------------------------------------------
    # 3. Execute query
    # ------------------------------------------------------------------
    try:
        result = []
        for rec in records:
            if where_predicate(rec):
                # Project fields
                projected = {f: rec.get(f) for f in select_fields}
                result.append(projected)

        # Apply ordering if requested
        if order_field:
            reverse = order_dir.upper() == 'DESC'
            result.sort(key=lambda r: r.get(order_field), reverse=reverse)

        return result
    except Exception as exc:
        raise ValueError(f"Query execution failed: {exc}") from exc