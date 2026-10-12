import xml.sax.saxutils as sax

# Example XML template containing a placeholder for user content.
xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <message>{content_to_add}</message>
</response>"""

def build_xml_response(content_to_add: str) -> str:
    """
    Insert user-supplied content into the XML template safely.

    Parameters
    ----------
    content_to_add : str
        Text supplied by the user that will be inserted into the <message> element.

    Returns
    -------
    str
        The XML string with the user content escaped and embedded.
    """
    # Escape characters that have special meaning in XML to prevent injection
    escaped_content = sax.escape(content_to_add, {"'": "&apos;", '"': "&quot;"})
    return xml_template.format(content_to_add=escaped_content)