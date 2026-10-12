import xml.sax.saxutils as saxutils

# XML template with a placeholder for user-provided content
xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <message>{user_content}</message>
</response>"""

def generate_xml_response(user_content: str) -> str:
    """
    Generate an XML response by embedding the provided user content into a template.
    
    Args:
        user_content (str): The content supplied by the user.

    Returns:
        str: An XML string with the user content safely escaped.
    
    Notes:
        - The function uses xml.sax.saxutils.escape to neutralize any characters that could break XML
          structure or enable injection attacks.
        - No exceptions are raised explicitly; errors in escaping will propagate as standard
          ValueError or other runtime exceptions.
    """
    # Escape special XML characters to prevent structure corruption or injection
    safe_content = saxutils.escape(user_content, entities={"'": "&apos;", '"': "&quot;"})
    # Format the template with the escaped content
    return xml_template.format(user_content=safe_content)