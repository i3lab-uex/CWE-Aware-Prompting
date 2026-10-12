import xml.sax.saxutils

# Example XML pattern with a placeholder for user text.
xml_pattern = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<response>\n'
    '  <message>{user_text}</message>\n'
    '</response>'
)

def create_xml_reply(user_text: str) -> str:
    """
    Insert the supplied user text into a predefined XML template,
    escaping any characters that could break XML structure.

    Args:
        user_text: The content supplied by the user.

    Returns:
        A string containing the final XML with the user text inserted.
    """
    # Escape special XML characters to prevent injection and malformed XML
    safe_text = xml.sax.saxutils.escape(user_text, entities={"'": "&apos;", '"': "&quot;"})
    return xml_pattern.format(user_text=safe_text)