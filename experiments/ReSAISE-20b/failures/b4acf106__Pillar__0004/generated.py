import xml.sax.saxutils

# XML template with a placeholder for user content
xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <message>{user_content}</message>
</response>"""

def generate_xml_response(user_content: str) -> str:
    """
    Generate a well‑formed XML response by safely embedding user content.

    Parameters
    ----------
    user_content : str
        The raw string provided by the user that should appear inside the <message> element.

    Returns
    -------
    str
        A complete XML document with the user content properly escaped.
    """
    # Escape special XML characters to prevent malformed XML or injection attacks
    safe_content = xml.sax.saxutils.escape(user_content, {"'": "&apos;", "\"": "&quot;"})
    return xml_template.format(user_content=safe_content)