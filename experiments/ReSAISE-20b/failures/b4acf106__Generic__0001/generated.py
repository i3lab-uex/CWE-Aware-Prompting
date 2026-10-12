import html

# XML template with a placeholder for user content
xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <content>{user_content}</content>
</response>"""

def generate_xml_response(user_content: str) -> str:
    """
    Generate an XML response by embedding the user-provided content into a template.
    
    Args:
        user_content (str): The user-provided content to be embedded into the XML response.
    
    Returns:
        str: The generated XML response incorporating the user-provided content, with
             special characters properly escaped.
    """
    # Escape XML special characters to avoid injection and malformed XML
    safe_content = html.escape(user_content, quote=True)
    
    # Insert the escaped content into the template
    return xml_template.format(user_content=safe_content)