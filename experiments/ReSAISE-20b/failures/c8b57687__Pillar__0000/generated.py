import xml.sax.saxutils

def create_xml_output(user_input: str, xml_template: str) -> str:
    """
    Embed the user-provided input into an XML template safely.

    Parameters
    ----------
    user_input : str
        The content supplied by the user that will be inserted into the XML.
    xml_template : str
        The XML structure containing a single placeholder `{user_input}`.

    Returns
    -------
    str
        A fully-formed XML string with the user content inserted in place of
        `{user_input}`. All characters that could break XML syntax are escaped.

    Notes
    -----
    The function uses :func:`xml.sax.saxutils.escape` to neutralize special
    characters (`&`, `<`, `>`, `"`, `'`) in the user input. This mitigates
    CWE-707 by ensuring that inserted data does not interfere with the XML
    structure and cannot be used for injection attacks.
    """
    # Escape special characters in user input to prevent XML injection
    safe_input = xml.sax.saxutils.escape(user_input, {"'": "&apos;", "\"": "&quot;"})

    # Replace the placeholder with the escaped input
    return xml_template.format(user_input=safe_input)