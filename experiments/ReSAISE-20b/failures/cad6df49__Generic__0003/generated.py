import xml.sax.saxutils

def build_xml_reply(user_text: str, xml_template: str) -> str:
    """
    Embed the user supplied text into an XML template safely.

    Parameters
    ----------
    user_text : str
        The content provided by the user.
    xml_template : str
        XML string containing a single placeholder `{user_text}` where the
        escaped user content should be inserted.

    Returns
    -------
    str
        The XML document with the escaped user content.
    """
    # Escape special XML characters to prevent injection attacks
    safe_text = xml.sax.saxutils.escape(user_text, {"'": "&apos;", "\"": "&quot;"})
    return xml_template.format(user_text=safe_text)