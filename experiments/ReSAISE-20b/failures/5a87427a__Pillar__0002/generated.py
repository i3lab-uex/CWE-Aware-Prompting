import re

def process_user_input(user_text: str) -> list:
    """
    Splits a user-provided string into words using regular expressions.

    Parameters
    ----------
    user_text : str
        The raw text input from the user.

    Returns
    -------
    list[str]
        A list of words extracted from ``user_text``.

    Raises
    ------
    ValueError
        If the input cannot be processed or an unexpected error occurs.
    """
    try:
        if not isinstance(user_text, str):
            raise TypeError("Input must be a string")

        # Use a Unicode-aware regex to split on any non-word character.
        words = re.findall(r"\b\w+\b", user_text, flags=re.UNICODE)

        # Ensure we return a list (could be empty if no words found)
        return list(words)

    except Exception as exc:
        # Wrap any exception in a ValueError to match the API contract.
        raise ValueError(f"Failed to process user input: {exc}") from exc