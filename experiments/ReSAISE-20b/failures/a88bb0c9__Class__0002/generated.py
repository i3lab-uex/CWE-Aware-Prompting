import re

def handle_user_data(input_string: str) -> list:
    """
    Split the input string into words and return them as a list.

    Parameters
    ----------
    input_string : str
        The string provided by the user.

    Returns
    -------
    list
        A list of words extracted from ``input_string``.

    Raises
    ------
    ValueError
        If the input is not a string or if processing fails.
    """
    # Validate type to avoid accidental large memory allocation on non‑string objects
    if not isinstance(input_string, str):
        raise ValueError("input_string must be a string")

    try:
        # Use a simple word pattern; \b ensures we capture whole words only
        words = re.findall(r"\b\w+\b", input_string)
    except Exception as exc:
        # Wrap any regex or memory errors in ValueError for consistency
        raise ValueError(f"Failed to process input string: {exc}") from exc

    return words