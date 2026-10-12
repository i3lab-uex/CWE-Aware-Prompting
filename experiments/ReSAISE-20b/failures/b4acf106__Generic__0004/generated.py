import html

def generate_xml_response(xml_template: str, user_content: str) -> str:
    """
    Generate an XML response by embedding the given user content into a template.

    Parameters
    ----------
    xml_template : str
        The XML template containing the placeholder `{user_content}`.
    user_content : str
        User-provided content that will be inserted into the template.

    Returns
    -------
    str
        The XML response with the user content safely escaped.
    """
    # Escape characters that are special in XML/HTML to avoid injection
    safe_content = html.escape(user_content, quote=True)
    return xml_template.format(user_content=safe_content)

# Example usage:
if __name__ == "__main__":
    template = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <data>{user_content}</data>
</response>"""
    user_input = "<script>alert('XSS');</script>"
    print(generate_xml_response(template, user_input))