import xml.sax.saxutils as sax

def craft_xml_reply(client_input: str, *, xml_structure: str) -> str:
    """
    Insert user supplied content into an XML template safely.

    Parameters
    ----------
    client_input : str
        Raw text submitted by the user.
    xml_structure : str
        XML template containing a single `{client_input}` placeholder.

    Returns
    -------
    str
        A well‑formed XML string with the user content inserted at the placeholder.
    """
    # Escape special XML characters to avoid injection or malformed output
    safe_input = sax.escape(client_input, entities={"'": "&apos;", "\"": "&quot;"})

    # Replace the placeholder with the escaped content
    return xml_structure.format(client_input=safe_input)