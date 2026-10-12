import xml.sax.saxutils

def build_xml_reply(user_text: str, xml_template: str) -> str:
    """
    Safely embed `user_text` into an XML template.

    Parameters
    ----------
    user_text : str
        The raw text supplied by the user.  It will be escaped to prevent XML injection.
    xml_template : str
        A string containing the placeholder `{user_text}` where the escaped user text should be inserted.

    Returns
    -------
    str
        A fully formed XML string with the user content safely inserted.

    Notes
    -----
    - The function uses :func:`xml.sax.saxutils.escape` to neutralize any characters that could break
      XML structure or allow injection.
    - No exceptions are raised by this function; it simply returns the escaped string.  If `xml_template`
      does not contain `{user_text}` a ``KeyError`` will be raised during formatting, which is the
      standard Python behaviour and signals misuse of the API.
    """
    # Escape user-provided text to avoid breaking XML structure or enabling injection
    escaped_text = xml.sax.saxutils.escape(user_text, entities={"'": "&apos;", "\"": "&quot;"})

    # Insert the escaped text into the template
    return xml_template.format(user_text=escaped_text)