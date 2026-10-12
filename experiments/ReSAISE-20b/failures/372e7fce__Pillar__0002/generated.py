import re
import operator
from functools import reduce

# Mapping of supported operators in WHERE clause
_OPERATOR_MAP = {
    '=': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le,
}

def _parse_select(sql):
    """Parse SELECT part and return list of columns."""
    m = re.search(r'SELECT\s+(.*?)\s+WHERE|ORDER BY|$', sql, re.IGNORECASE | re.DOTALL)
    if not m:
        raise ValueError("Invalid SELECT clause")
    cols = [c.strip() for c in m.group(1).split(',')]
    if len(cols) == 1 and cols[0] == '*':
        return None  # means all columns
    return cols

def _parse_where(sql):
    """Parse WHERE part and return list of (column, op, value) tuples."""
    m = re.search(r'WHERE\s+(.*?)(ORDER BY|$)', sql, re.IGNORECASE | re.DOTALL)
    if not m:
        return []  # no where clause
    condition_str = m.group(1).strip()
    if not condition_str:
        return []

    # split by AND/OR, only support AND for simplicity
    parts = re.split(r'\s+AND\s+', condition_str, flags=re.IGNORECASE)
    conditions = []
    for part in parts:
        m_cond = re.match(r'(\w+)\s*(=|!=|<>|>=|<=|>|<)\s*(.+)', part)
        if not m_cond:
            raise ValueError(f"Invalid WHERE condition: {part}")
        col, op_sym, val = m_cond.groups()
        # strip quotes if present
        val = val.strip()
        if (val.startswith("'") and val.endswith("'")) or \
           (val.startswith('"') and val.endswith('"')):
            val = val[1:-1]
        else:
            # try to interpret as int or float
            if re.fullmatch(r'-?\d+\.\d+', val):
                val = float(val)
            elif re.fullmatch(r'-?\d+', val):
                val = int(val)
        conditions.append((col, _OPERATOR_MAP[op_sym], val))
    return conditions

def _parse_order_by(sql):
    """Parse ORDER BY part and return (column, ascending)."""
    m = re.search(r'ORDER\s+BY\s+(\w+)(?:\s+(ASC|DESC))?$', sql, re.IGNORECASE)
    if not m:
        return None
    col = m.group(1)
    asc = True if (m.group(2) or 'ASC').upper() == 'ASC' else False
    return col, asc

def _evaluate_where(record, conditions):
    """Return True if record satisfies all conditions."""
    for col, op_func, val in conditions:
        if col not in record:
            return False
        try:
            if not op_func(record[col], val):
                return False
        except Exception:
            return False
    return True

def execute_query_cmd(dataset_list, sql_query):
    """
    Execute a simple SQL-like query on a list of dictionaries.

    Supported syntax:
        SELECT <columns|*> [WHERE <condition> [AND ...]] [ORDER BY <column> [ASC|DESC]]

    Conditions support operators: =, !=, <>, >, <, >=, <=.
    Only logical AND is supported between conditions.
    """
    if not isinstance(dataset_list, list):
        raise ValueError("dataset_list must be a list")
    if not isinstance(sql_query, str):
        raise ValueError("sql_query must be a string")

    # Normalize query: strip leading/trailing spaces
    sql = sql_query.strip()

    try:
        select_cols = _parse_select(sql)
        where_conditions = _parse_where(sql)
        order_by = _parse_order_by(sql)

        # Filter records
        filtered = [rec for rec in dataset_list if _evaluate_where(rec, where_conditions)]

        # Order records
        if order_by:
            col, asc = order_by
            try:
                filtered.sort(key=lambda r: r.get(col), reverse=not asc)
            except TypeError:
                raise ValueError(f"Cannot order by column '{col}' due to incomparable types")

        # Project columns
        if select_cols is None:
            result = [dict(rec) for rec in filtered]
        else:
            result = [{c: rec.get(c) for c in select_cols} for rec in filtered]

        return result

    except Exception as e:
        # Wrap any exception as ValueError for consistency
        raise ValueError(f"Query processing error: {e}") from e

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     data = [
#         {"id": 1, "name": "Alice", "age": 30},
#         {"id": 2, "name": "Bob", "age": 25},
#         {"id": 3, "name": "Charlie", "age": 35}
#     ]
#     q = "SELECT id, name WHERE age >= 30 ORDER BY name DESC"
#     print(execute_query_cmd(data, q))