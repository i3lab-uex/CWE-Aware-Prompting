import xml.sax.saxutils

def build_xml_reply(user_text: str, xml_template: str) -> str:
    """
    Build an XML reply by safely inserting user_text into xml_template.

    Parameters
    ----------
    user_text : str
        Input provided by the user that will be embedded in the XML structure.
    xml_template : str
        The XML template string containing a single placeholder `{user_text}`.

    Returns
    -------
    str
        A fully-formed XML string with the user content safely escaped.

    Notes
    -----
    The function uses `xml.sax.saxutils.escape` to neutralize characters that
    have special meaning in XML (e.g., &, <, >, ", '), preventing injection
    attacks such as CWE-74.  It assumes that the template contains exactly one
    `{user_text}` placeholder; if multiple placeholders exist, only the first
    will be replaced.  If the placeholder is missing, the original template
    is returned unchanged.
    """
    # Escape user input to prevent XML injection
    safe_user_text = xml.sax.saxutils.escape(user_text, {"'": "&apos;", '"': "&quot;"})
    # Replace the placeholder with escaped content
    return xml_template.replace("{user_text}", safe_user_text, 1)