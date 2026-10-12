import re
import operator
from functools import reduce
from typing import List, Dict, Any

# Mapping of string operators to actual operator functions
COMPARISON_OPERATORS = {
    "=": operator.eq,
    "!=": operator.ne,
    "<>": operator.ne,
    ">": operator.gt,
    "<": operator.lt,
    ">=": operator.ge,
    "<=": operator.le,
}

LOGICAL_OPERATORS = {
    "AND": lambda a, b: a and b,
    "OR": lambda a, b: a or b,
}

def _parse_select_clause(clause: str) -> List[str]:
    """Parse SELECT clause and return list of fields (or ['*'])."""
    fields = [f.strip() for f in clause.split(",")]
    if len(fields) == 1 and fields[0] == "*":
        return ["*"]
    if any(f.upper() in LOGICAL_OPERATORS for f in fields):
        raise ValueError("Invalid field name in SELECT clause")
    return fields

def _eval_condition(record: Dict[str, Any], token: str) -> bool:
    """Evaluate a simple comparison like 'age >= 30'."""
    # Regex to capture left operand, operator, right operand
    match = re.match(r"(\w+)\s*(=|!=|<>|>=|<=|>|<)\s*(['\"]?)(.+?)\3$", token)
    if not match:
        raise ValueError(f"Invalid condition: {token}")
    field, op_str, _, value = match.groups()
    if field not in record:
        raise ValueError(f"Field '{field}' not found in record")
    comp_op = COMPARISON_OPERATORS[op_str]
    # Try to cast value to int/float if possible
    try:
        value_cast = int(value)
    except ValueError:
        try:
            value_cast = float(value)
        except ValueError:
            value_cast = value  # keep as string
    return comp_op(record[field], value_cast)

def _parse_where_clause(clause: str) -> List[str]:
    """Split WHERE clause into tokens respecting parentheses."""
    # Tokenize by space but keep parentheses as separate tokens
    tokens = re.findall(r"\(|\)|AND|OR|[^\s()]+", clause, flags=re.IGNORECASE)
    # Normalize logical operators to uppercase
    return [t.upper() if t.upper() in LOGICAL_OPERATORS else t for t in tokens]

def _eval_where_tokens(record: Dict[str, Any], tokens: List[str]) -> bool:
    """Evaluate token list using shunting-yard algorithm for logical ops."""
    output_stack = []
    operator_stack = []

    def apply_operator():
        op_token = operator_stack.pop()
        right = output_stack.pop()
        left = output_stack.pop()
        op_func = LOGICAL_OPERATORS[op_token]
        output_stack.append(op_func(left, right))

    for token in tokens:
        if token == "(":
            operator_stack.append(token)
        elif token == ")":
            while operator_stack and operator_stack[-1] != "(":
                apply_operator()
            if not operator_stack or operator_stack[-1] != "(":
                raise ValueError("Mismatched parentheses in WHERE clause")
            operator_stack.pop()  # pop '('
        elif token in LOGICAL_OPERATORS:
            while (operator_stack and operator_stack[-1] in LOGICAL_OPERATORS):
                apply_operator()
            operator_stack.append(token)
        else:
            # token is a condition
            output_stack.append(_eval_condition(record, token))

    while operator_stack:
        apply_operator()

    if len(output_stack) != 1:
        raise ValueError("Failed to evaluate WHERE clause")
    return output_stack[0]

def _parse_order_by_clause(clause: str) -> (str, bool):
    """Parse ORDER BY clause returning field and ascending flag."""
    parts = [p.strip() for p in clause.split()]
    if not parts:
        raise ValueError("ORDER BY clause is empty")
    field = parts[0]
    ascending = True
    if len(parts) > 1:
        dir_token = parts[1].upper()
        if dir_token == "DESC":
            ascending = False
        elif dir_token != "ASC":
            raise ValueError("ORDER BY direction must be ASC or DESC")
    return field, ascending

def process_sql_request(dataset_records: List[Dict[str, Any]], sql_statement: str) -> List[Dict[str, Any]]:
    """
    Execute a simple SQL-like query on a list of dictionaries.

    Supports:
        SELECT <fields> | *
        WHERE <condition>
        ORDER BY <field> [ASC|DESC]

    Example:
        SELECT name, age FROM data WHERE age >= 30 ORDER BY name DESC
    """
    if not isinstance(dataset_records, list):
        raise ValueError("dataset_records must be a list of dictionaries")
    if not isinstance(sql_statement, str):
        raise ValueError("sql_statement must be a string")

    # Normalize whitespace and upper-case keywords for parsing
    sql = re.sub(r"\s+", " ", sql_statement.strip())
    # Regex to capture clauses
    pattern = re.compile(
        r"SELECT\s+(?P<select>.+?)\s+FROM\s+\w+"          # SELECT clause
        r"(?:\s+WHERE\s+(?P<where>.+?))?"                # optional WHERE
        r"(?:\s+ORDER\s+BY\s+(?P<order>.+))?$",          # optional ORDER BY
        re.IGNORECASE)
    match = pattern.match(sql)
    if not match:
        raise ValueError("Query is not correctly formed")

    select_clause = match.group('select')
    where_clause = match.group('where')
    order_by_clause = match.group('order')

    # Parse SELECT fields
    selected_fields = _parse_select_clause(select_clause)

    # Filter records if WHERE clause present
    filtered_records = dataset_records
    if where_clause:
        tokens = _parse_where_clause(where_clause)
        filtered_records = [
            rec for rec in dataset_records if _eval_where_tokens(rec, tokens)
        ]

    # Order records if ORDER BY present
    if order_by_clause:
        field, ascending = _parse_order_by_clause(order_by_clause)
        try:
            filtered_records.sort(key=lambda r: r[field], reverse=not ascending)
        except KeyError:
            raise ValueError(f"Field '{field}' not found for ORDER BY")

    # Project selected fields
    if selected_fields == ["*"]:
        result = [dict(rec) for rec in filtered_records]
    else:
        result = []
        for rec in filtered_records:
            projected = {}
            for field in selected_fields:
                if field not in rec:
                    raise ValueError(f"Field '{field}' not found in record")
                projected[field] = rec[field]
            result.append(projected)

    return result