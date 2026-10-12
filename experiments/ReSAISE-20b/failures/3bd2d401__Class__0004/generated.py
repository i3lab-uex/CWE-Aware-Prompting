import xml.sax.saxutils

# Predefined XML template with a placeholder for user input.
xml_design = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <message>{input_data}</message>
</response>"""

def process_xml_reply(input_data: str) -> str:
    """
    Return an XML string with the user-supplied content safely inserted.

    Parameters
    ----------
    input_data : str
        The raw user-provided content that will be inserted into the XML template.

    Returns
    -------
    str
        The fully formed XML document with the escaped user content in place.
    """
    # Escape characters that have special meaning in XML to prevent injection
    safe_content = xml.sax.saxutils.escape(input_data, {"'": "&apos;", '"': "&quot;"})
    # Insert the escaped content into the template
    return xml_design.format(input_data=safe_content)