import re

# Maximum number of words allowed to prevent uncontrolled resource consumption (CWE-400)
MAX_WORDS = 10000

def process_user_input(user_input: str) -> list:
    """
    Splits the given user input into a list of words.

    Parameters
    ----------
    user_input : str
        The string containing user input to be processed.

    Returns
    -------
    list[str]
        A list of words extracted from the input string.

    Raises
    ------
    ValueError
        If `user_input` is not a string, or if an error occurs during processing,
        or if the number of extracted words exceeds `MAX_WORDS`.
    """
    if not isinstance(user_input, str):
        raise ValueError("Input must be a string")

    try:
        # Extract words using a simple word boundary regex
        words = re.findall(r"\b\w+\b", user_input)

        # Enforce a hard limit on the number of words to mitigate resource exhaustion
        if len(words) > MAX_WORDS:
            raise ValueError(f"Input contains too many words ({len(words)}); maximum allowed is {MAX_WORDS}")

        return words

    except re.error as exc:
        # re.compile or findall can raise a regex error
        raise ValueError(f"Regex processing failed: {exc}") from exc

    except Exception as exc:
        # Catch any other unforeseen exception and wrap it in ValueError
        raise ValueError(f"Unexpected error during input processing: {exc}") from exc