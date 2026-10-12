import xml.sax.saxutils

def build_xml_reply(user_text: str, xml_template: str) -> str:
    """
    Build an XML response by inserting user-provided text into a template.

    Parameters
    ----------
    user_text : str
        The input provided by the user that should be safely embedded in XML.
    xml_template : str
        The XML structure containing a `{user_text}` placeholder.

    Returns
    -------
    str
        A fully-formed XML string with the user content inserted.

    Notes
    -----
    The function escapes special XML characters in ``user_text`` to prevent
    injection attacks or malformed XML.  No exceptions are raised; if the
    template does not contain the placeholder, it is returned unchanged.
    """
    # Escape XML special characters in user_text
    escaped_user_text = xml.sax.saxutils.escape(user_text, entities={"'": "&apos;", "\"": "&quot;"})
    # Substitute the placeholder; if not present, return template unchanged
    try:
        return xml_template.format(user_text=escaped_user_text)
    except KeyError:
        # The placeholder {user_text} was not found; return the original template
        return xml_template