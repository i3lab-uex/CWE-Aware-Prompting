import xml.sax.saxutils

# XML template with a placeholder for user content
xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <content>{user_content}</content>
</response>"""

def generate_xml_response(user_content: str) -> str:
    """
    Generate an XML response by safely embedding user-provided content into a template.

    Args:
        user_content: The raw string supplied by the user to be inserted into the XML.

    Returns:
        A well‑formed XML string with the user content escaped to prevent injection.
    """
    # Escape characters that have special meaning in XML
    safe_content = xml.sax.saxutils.escape(user_content, entities={"'": "&apos;", "\"": "&quot;"})
    return xml_template.format(user_content=safe_content)