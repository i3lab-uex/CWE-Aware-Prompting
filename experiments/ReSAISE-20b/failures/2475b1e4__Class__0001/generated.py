import xml.sax.saxutils as saxutils

# Pre‑defined XML template with a placeholder for user content.
xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <data>{content_to_add}</data>
</response>"""

def build_xml_response(content_to_add: str) -> str:
    """
    Build an XML response by inserting user supplied content into a
    pre‑defined template. The function escapes any XML special
    characters to prevent injection (CWE‑74).

    Parameters
    ----------
    content_to_add : str
        Text supplied by the user to be inserted into the XML structure.

    Returns
    -------
    str
        The constructed XML response with user content safely escaped.
    """
    # Escape &, <, >, " and ' characters for XML safety
    safe_content = saxutils.escape(content_to_add, {"'": "&apos;", '"': "&quot;"})
    return xml_template.format(content_to_add=safe_content)