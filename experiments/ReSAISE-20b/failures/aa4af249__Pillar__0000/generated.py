import re
import operator
from functools import reduce
from typing import List, Dict, Any

# Mapping of string operators to actual Python functions
OPERATORS = {
    "=": operator.eq,
    "!=": operator.ne,
    "<>": operator.ne,
    ">": operator.gt,
    ">=": operator.ge,
    "<": operator.lt,
    "<=": operator.le,
}

# Logical operators
LOGICAL_OPERATORS = {
    "AND": lambda a, b: a and b,
    "OR": lambda a, b: a or b,
}

def _parse_where_clause(where_str: str):
    """
    Very small parser for WHERE clauses.
    Supports expressions like:
        field = value AND other_field > 5 OR flag != 'yes'
    Values are either numeric literals or quoted strings.
    """
    # Tokenize
    token_pattern = r"""
        (?P<field>\w+)
        \s*
        (?P<op>=|!=|<>|<=|>=|<|>)
        \s*
        (?P<value>
            '(?:\\'|[^'])*' |    # single quoted string
            "(?:\\"|[^"])*" |    # double quoted string
            \d+(\.\d+)?          # number
        )
        |(?P<logical>AND|OR)
    """
    tokens = re.finditer(token_pattern, where_str, re.VERBOSE | re.IGNORECASE)

    def _convert_value(val: str) -> Any:
        val = val.strip()
        if (val.startswith("'") and val.endswith("'")) or (val.startswith('"') and val.endswith('"')):
            return val[1:-1].replace("\\'", "'").replace('\\"', '"')
        try:
            if '.' in val:
                return float(val)
            return int(val)
        except ValueError:
            raise ValueError(f"Unsupported value format: {val}")

    # Build a list of functions that evaluate each condition
    conditions = []
    logicals = []

    for m in tokens:
        if m.group('field'):
            field = m.group('field')
            op_str = m.group('op')
            value = _convert_value(m.group('value'))
            if op_str not in OPERATORS:
                raise ValueError(f"Unsupported operator: {op_str}")
            op_func = OPERATORS[op_str]
            # Each condition is a lambda that takes a record and returns bool
            conditions.append(lambda rec, f=field, v=value, op=op_func: op(rec.get(f), v))
        elif m.group('logical'):
            logicals.append(m.group('logical').upper())

    # Combine conditions with logical operators
    def combined_condition(rec):
        if not conditions:
            return True  # No WHERE clause
        result = conditions[0](rec)
        for i, logic in enumerate(logicals):
            next_cond = conditions[i + 1](rec)
            result = LOGICAL_OPERATORS[logic](result, next_cond)
        return result

    return combined_condition


def process_sql_request(dataset_records: List[Dict[str, Any]], sql_statement: str) -> List[Dict[str, Any]]:
    """
    Execute a simple SQL-like query on an in-memory dataset.

    Supported syntax:
        SELECT <columns> FROM data WHERE <conditions> ORDER BY <column> [ASC|DESC];

    - SELECT * selects all columns.
    - WHERE supports =, !=, <>, >, >=, <, <= with AND/OR.
    - ORDER BY sorts by a single column; direction defaults to ASC.

    Parameters
    ----------
    dataset_records : list[dict]
        The data to query.
    sql_statement : str
        Query string.

    Returns
    -------
    list[dict]
        Resulting rows after applying SELECT, WHERE and ORDER BY.

    Raises
    ------
    ValueError
        If the query cannot be parsed or executed.
    """
    # Basic validation and normalization
    if not isinstance(dataset_records, list):
        raise ValueError("dataset_records must be a list of dictionaries")
    if not isinstance(sql_statement, str):
        raise ValueError("sql_statement must be a string")

    # Remove trailing semicolon and strip whitespace
    sql = sql_statement.strip().rstrip(';')
    if not sql.upper().startswith("SELECT"):
        raise ValueError("Only SELECT statements are supported")

    # Regex to split into parts
    pattern = re.compile(
        r"""
        SELECT\s+(?P<select>[\w\*,\s]+)
        \s+FROM\s+\w+
        (\s+WHERE\s+(?P<where>.+?))?
        (\s+ORDER\s+BY\s+(?P<order>\w+)(\s+(?P<dir>ASC|DESC))?)?
        """,
        re.IGNORECASE | re.VERBOSE,
    )
    match = pattern.fullmatch(sql)
    if not match:
        raise ValueError("Could not parse the SQL statement")

    select_cols = [col.strip() for col in match.group('select').split(',')]
    where_clause = match.group('where')
    order_col = match.group('order')
    dir_flag = match.group('dir')

    # Process WHERE
    if where_clause:
        condition_func = _parse_where_clause(where_clause)
        filtered_records = [rec for rec in dataset_records if condition_func(rec)]
    else:
        filtered_records = list(dataset_records)

    # Process ORDER BY
    if order_col:
        reverse = dir_flag and dir_flag.upper() == "DESC"
        try:
            filtered_records.sort(key=lambda r: r.get(order_col), reverse=reverse)
        except TypeError as exc:
            raise ValueError(f"Cannot order by column '{order_col}': {exc}") from exc

    # Process SELECT
    if select_cols == ["*"]:
        result = filtered_records
    else:
        # Ensure columns exist; if not, set to None
        result = [
            {col: rec.get(col) for col in select_cols}
            for rec in filtered_records
        ]

    return result

# Example usage (uncomment to test)
# data = [
#     {"id": 1, "name": "Alice", "age": 30},
#     {"id": 2, "name": "Bob", "age": 25},
#     {"id": 3, "name": "Charlie", "age": 35}
# ]
# query = "SELECT id, name FROM data WHERE age > 28 ORDER BY name DESC;"
# print(process_sql_request(data, query))