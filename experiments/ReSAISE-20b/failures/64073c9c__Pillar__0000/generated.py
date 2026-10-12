import xml.sax.saxutils as saxutils

# Pre‑defined XML template with a placeholder for user content.
xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <message>{content_insert}</message>
</response>"""

def generate_xml_message(content_insert: str) -> str:
    """
    Construct an XML response by inserting the supplied content into a
    predefined template. The content is safely escaped to prevent XML
    injection or malformed documents.

    Args:
        content_insert (str): User supplied text to embed in the XML.

    Returns:
        str: A well‑formed XML string containing the escaped user content.
    """
    # Escape special XML characters in the user supplied content
    safe_content = saxutils.escape(content_insert, entities={"'": "&apos;", '"': "&quot;"})

    # Format the template with the escaped content
    return xml_template.format(content_insert=safe_content)