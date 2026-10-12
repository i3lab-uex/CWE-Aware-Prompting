import xml.sax.saxutils

def build_xml_response(content_to_add: str) -> str:
    """
    Build an XML response by inserting the user-supplied content into a
    predefined template. The content is escaped to prevent XML injection.
    
    Args:
        content_to_add: Text supplied by the user that will be inserted
                        into the XML structure.
    
    Returns:
        A string containing the fully constructed, well‑formed XML document.
    """
    # Predefined XML template with a placeholder for the user content
    xml_template = (
        "<response>\n"
        "  <status>success</status>\n"
        "  <data>{content_to_add}</data>\n"
        "</response>"
    )
    
    # Escape the user content to avoid malformed XML and injection
    safe_content = xml.sax.saxutils.escape(content_to_add, {"'": "&apos;", "\"": "&quot;"})
    
    # Insert the escaped content into the template
    return xml_template.format(content_to_add=safe_content)