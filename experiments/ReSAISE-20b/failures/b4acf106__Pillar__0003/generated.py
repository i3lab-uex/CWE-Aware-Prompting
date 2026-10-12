import xml.sax.saxutils

# XML template with a placeholder for user content.
xml_template = """
<response>
    <content>{user_content}</content>
</response>
"""

def generate_xml_response(user_content: str) -> str:
    """
    Generate an XML response by embedding the given user content into a template.
    
    Parameters
    ----------
    user_content : str
        The user-provided content to be embedded into the XML response.
    
    Returns
    -------
    str
        The generated XML response incorporating the user-provided content.
    
    Notes
    -----
    - The function escapes special XML characters in `user_content` to prevent
      malformed XML or injection attacks.
    - It does not raise exceptions explicitly; however, if `user_content` is
      ``None`` or not a string, a TypeError will be raised by `escape`.
    """
    # Ensure the content is a string and escape XML special characters.
    escaped_content = xml.sax.saxutils.escape(str(user_content))
    
    # Safely substitute the placeholder in the template.
    return xml_template.format(user_content=escaped_content)