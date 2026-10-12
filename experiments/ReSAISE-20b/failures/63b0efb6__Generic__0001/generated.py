import re
import operator

def run_sql_query(records, command):
    """
    Execute a very small subset of SQL against an in‑memory list of dictionaries.
    
    Supported syntax:
        SELECT <columns|*> [WHERE <column> <op> <value>] [ORDER BY <column> [ASC|DESC]]
    
    * <columns> are comma separated column names (no spaces required).
    * <op> is one of =, !=, <, <=, >, >=.
    * <value> may be an integer/float or a quoted string ('...' or "...").
    """
    if not isinstance(records, list):
        raise ValueError("records must be a list of dictionaries")
    if not isinstance(command, str):
        raise ValueError("command must be a string")

    cmd = command.strip()
    if not cmd.lower().startswith("select "):
        raise ValueError("Command must start with SELECT")

    # Split into SELECT part, optional WHERE, and optional ORDER BY
    rest = cmd[6:].strip()          # everything after SELECT

    where_part = None
    order_part = None
    select_part = rest

    # Handle WHERE
    where_match = re.search(r"\s+where\s+", rest, flags=re.IGNORECASE)
    if where_match:
        select_part = rest[:where_match.start()].strip()
        rest_after_where = rest[where_match.end():].strip()

        # Handle ORDER BY after WHERE
        order_match = re.search(r"\s+order\s+by\s+", rest_after_where, flags=re.IGNORECASE)
        if order_match:
            where_part = rest_after_where[:order_match.start()].strip()
            order_part = rest_after_where[order_match.end():].strip()
        else:
            where_part = rest_after_where
    else:
        # No WHERE, maybe ORDER BY
        order_match = re.search(r"\s+order\s+by\s+", rest, flags=re.IGNORECASE)
        if order_match:
            select_part = rest[:order_match.start()].strip()
            order_part = rest[order_match.end():].strip()

    # Parse SELECT columns
    fields = [f.strip() for f in select_part.split(",")]
    if len(fields) == 1 and fields[0] == "*":
        selected_fields = None
    else:
        selected_fields = fields

    # Validate column names against the dataset
    all_keys = {k for r in records if isinstance(r, dict) for k in r.keys()}
    if selected_fields:
        missing = [f for f in selected_fields if f not in all_keys]
        if missing:
            raise ValueError(f"Unknown column(s) in SELECT: {', '.join(missing)}")

    # Apply WHERE filter
    filtered = records
    if where_part:
        m = re.match(r"(\w+)\s*(=|!=|<=|>=|<|>)\s*(.+)", where_part)
        if not m:
            raise ValueError("Invalid WHERE clause")
        col, op_str, val_raw = m.groups()

        if col not in all_keys:
            raise ValueError(f"Unknown column in WHERE: {col}")

        # Parse value
        if (val_raw.startswith("'") and val_raw.endswith("'")) or \
           (val_raw.startswith('"') and val_raw.endswith('"')):
            val = val_raw[1:-1]
        else:
            try:
                val = int(val_raw)
            except ValueError:
                try:
                    val = float(val_raw)
                except ValueError:
                    raise ValueError(f"Unable to parse value in WHERE: {val_raw}")

        ops = {
            "=": operator.eq,
            "!=": operator.ne,
            "<": operator.lt,
            ">": operator.gt,
            "<=": operator.le,
            ">=": operator.ge
        }
        op_func = ops[op_str]

        def matches(r):
            if col not in r:
                return False
            try:
                return op_func(r[col], val)
            except Exception:
                return False

        filtered = [r for r in records if matches(r)]

    # Apply ORDER BY
    if order_part:
        parts = order_part.split()
        col = parts[0]
        direction = "ASC"
        if len(parts) > 1:
            direction = parts[1].upper()
        reverse = direction == "DESC"

        if col not in all_keys:
            raise ValueError(f"Unknown column in ORDER BY: {col}")

        try:
            filtered = sorted(filtered, key=lambda r: r.get(col), reverse=reverse)
        except TypeError as exc:
            raise ValueError("Unable to order by column with mixed types") from exc

    # Project selected fields
    if selected_fields is None:
        result = filtered
    else:
        result = [{k: r.get(k) for k in selected_fields} for r in filtered]

    return result