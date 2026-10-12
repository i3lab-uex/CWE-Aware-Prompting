import re

def process_user_input(user_input: str) -> list:
    """
    Split a user-provided string into individual words.

    Parameters
    ----------
    user_input : str
        The raw input string from the user.

    Returns
    -------
    list
        A list of words extracted from ``user_input``.

    Raises
    ------
    ValueError
        If the input is not a string or if an error occurs during processing.
    """
    # Validate that we received a string
    if not isinstance(user_input, str):
        raise ValueError("Input must be a string")

    try:
        # Use a simple regex that matches word characters.
        words = re.findall(r"\b\w+\b", user_input)
    except Exception as exc:  # pragma: no cover
        # Any exception from re is wrapped in a ValueError to keep the API stable.
        raise ValueError(f"Failed to process input: {exc}") from exc

    return words