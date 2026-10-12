import xml.sax.saxutils

def create_xml_output(user_input: str, xml_template: str) -> str:
    """
    Generate a well‑formed XML response by safely embedding user input into
    the provided template.

    Parameters:
        user_input (str): The raw string supplied by a user.
        xml_template (str): An XML template containing the placeholder
                            `{user_input}` where the escaped content should be inserted.

    Returns:
        str: The fully formed XML string with user input safely escaped.
    """
    # Escape special XML characters to prevent injection and malformed documents
    safe_input = xml.sax.saxutils.escape(user_input, entities={"'": "&apos;", "\"": "&quot;"})
    # Insert the escaped content into the template
    return xml_template.format(user_input=safe_input)