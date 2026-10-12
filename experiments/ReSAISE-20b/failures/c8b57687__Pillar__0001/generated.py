import xml.sax.saxutils

# Example XML template with a placeholder for user input.
xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <message>{user_input}</message>
</response>"""

def create_xml_output(user_input: str) -> str:
    """
    Embed user-provided input into an XML template, ensuring that the
    content is properly escaped to avoid malformed XML and injection attacks.

    Args:
        user_input (str): The raw input supplied by the user.

    Returns:
        str: A well‑formed XML string with the escaped user content.
    """
    # Escape special XML characters in the user input.
    safe_input = xml.sax.saxutils.escape(user_input, entities={"'": "&apos;", "\"": "&quot;"})
    # Format the template with the escaped content.
    return xml_template.format(user_input=safe_input)