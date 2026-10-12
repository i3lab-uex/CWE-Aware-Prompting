import xml.sax.saxutils

# Predefined XML template with a placeholder for user content.
xml_pattern = """
<response>
    <message>{user_text}</message>
</response>
"""

def create_xml_reply(user_text: str) -> str:
    """
    Insert the provided user text into a predefined XML template, ensuring
    that any characters which could break XML structure are properly escaped.

    Parameters:
        user_text (str): The raw text supplied by the user.

    Returns:
        str: A well‑formed XML string containing the escaped user content.
    """
    # Escape characters that have special meaning in XML
    safe_text = xml.sax.saxutils.escape(user_text, entities={"'": "&apos;", '"': "&quot;"})
    # Format the template with the escaped text
    return xml_pattern.format(user_text=safe_text)