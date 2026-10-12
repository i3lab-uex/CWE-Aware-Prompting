import re
from xml.sax.saxutils import escape

# Pre‑defined XML template containing a single placeholder.
XML_TEMPLATE = """
<response>
    <status>OK</status>
    <data>{content_to_add}</data>
</response>
"""

def build_xml_response(content_to_add: str) -> str:
    """
    Build a well‑formed XML response by safely inserting user content into
    the pre‑defined template.

    Parameters:
        content_to_add (str): User supplied text to be embedded in the XML.

    Returns:
        str: The constructed XML string.
    """
    # Ensure that the placeholder exists in the template
    if "{content_to_add}" not in XML_TEMPLATE:
        raise ValueError("Template missing required placeholder.")

    # Escape special XML characters to prevent malformed documents
    safe_content = escape(content_to_add, entities={"'": "&apos;", "\"": "&quot;"})

    # Insert the escaped content into the template
    xml_response = XML_TEMPLATE.format(content_to_add=safe_content)

    # Quick sanity check: the resulting string should be parseable by ElementTree
    try:
        import xml.etree.ElementTree as ET
        ET.fromstring(xml_response)
    except ET.ParseError as exc:
        raise ValueError("Generated XML is not well‑formed.") from exc

    return xml_response.strip()