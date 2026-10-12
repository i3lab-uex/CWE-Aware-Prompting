import xml.sax.saxutils

def create_xml_output(input_content: str) -> str:
    """
    Construct an XML response by inserting user-supplied content into a
    predefined template while ensuring the content is properly escaped.

    Args:
        input_content: Text supplied by the user to be inserted into the XML.

    Returns:
        A string containing the well‑formed XML with the escaped content.
    """
    # Predefined template with a placeholder for the user input
    xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <content>{input_content}</content>
</response>"""

    # Escape special XML characters to prevent injection and malformed XML
    safe_content = xml.sax.saxutils.escape(input_content, {"'": "&apos;", '"': "&quot;"})

    # Format the template with the escaped content
    return xml_template.format(input_content=safe_content)