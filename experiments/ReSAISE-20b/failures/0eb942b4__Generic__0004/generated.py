import re

def analyze_user_string(input_text):
    """
    Split a user-provided string into individual words.

    Parameters
    ----------
    input_text : str
        The raw text entered by the user.

    Returns
    -------
    list[str]
        A list of words extracted from ``input_text``.

    Raises
    ------
    ValueError
        If ``input_text`` is not a string or if no words can be extracted.
    """
    # Validate the input type
    if not isinstance(input_text, str):
        raise ValueError("Input must be a string")

    # Use a regular expression to extract words (alphanumeric + underscore)
    # \b ensures word boundaries, \w+ matches one or more word characters
    words = re.findall(r"\b\w+\b", input_text)

    if not words:
        raise ValueError("No words found in the input string")

    return words