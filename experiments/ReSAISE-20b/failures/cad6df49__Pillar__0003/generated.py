import xml.sax.saxutils as sax

# Predefined XML template containing a placeholder for user content.
xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <message>{user_text}</message>
</response>"""

def build_xml_reply(user_text: str) -> str:
    """
    Build a well‑formed XML reply by inserting the user supplied text
    into ``xml_template`` after escaping any characters that would break XML.

    Parameters
    ----------
    user_text : str
        The raw text supplied by the user that must be safely embedded in XML.

    Returns
    -------
    str
        A fully formed XML string containing the escaped user content.
    """
    # Escape characters that are significant in XML to avoid injection or
    # malformed documents.
    safe_text = sax.escape(user_text, {"'": "&apos;", "\"": "&quot;"})
    return xml_template.format(user_text=safe_text)