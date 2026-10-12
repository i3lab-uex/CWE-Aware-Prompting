import xml.sax.saxutils

def create_xml_output(input_content: str) -> str:
    """
    Create an XML response by inserting user-supplied content into a pre-defined template.

    Parameters
    ----------
    input_content : str
        The text supplied by the user to be inserted into the XML structure.

    Returns
    -------
    str
        The constructed XML response that integrates the escaped input from the user.
    """
    xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <content>{input_content}</content>
</response>"""

    # Escape characters that are special in XML to prevent injection or malformed output
    safe_content = xml.sax.saxutils.escape(input_content, entities={"'": "&apos;", '"': "&quot;"})

    return xml_template.format(input_content=safe_content)