import html

def generate_xml_response(user_content: str) -> str:
    """
    Generate an XML response by embedding user-provided content into a template.
    
    Args:
        user_content (str): The content supplied by the user to be inserted into
                            the XML response.
    
    Returns:
        str: A well‑formed XML string containing the escaped user content.
    
    Notes:
        - The function escapes all special XML characters to prevent injection
          attacks (CWE‑74).
        - The template is defined within the function for clarity; in a real
          application it might be loaded from an external source.
    """
    # Define the XML template with a placeholder for user content
    xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <message>{user_content}</message>
</response>"""

    # Escape user content to neutralize special XML characters
    safe_content = html.escape(user_content, quote=True)

    # Insert the escaped content into the template
    return xml_template.format(user_content=safe_content)