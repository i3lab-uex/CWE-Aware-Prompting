import xml.sax.saxutils

def build_xml_reply(user_text: str, xml_template: str) -> str:
    """
    Safely embed user-provided text into an XML template.

    Parameters
    ----------
    user_text : str
        The raw text supplied by the user.
    xml_template : str
        An XML string containing a single placeholder `{user_text}` where the
        user content should be inserted.

    Returns
    -------
    str
        A complete XML string with the user text safely escaped.
    """
    # Escape special XML characters to prevent injection
    safe_text = xml.sax.saxutils.escape(user_text, entities={
        '"': '&quot;',   # escape double quotes if they appear
        "'": '&apos;'    # escape single quotes for completeness
    })

    # Insert the escaped text into the template
    return xml_template.format(user_text=safe_text)