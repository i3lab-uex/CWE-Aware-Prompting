import html

def create_html_output(input_content: str) -> str:
    """
    Injects user-provided content into an HTML template, ensuring that the
    content is properly escaped to prevent injection attacks.

    Parameters:
        input_content (str): The dynamic user content to be inserted into the template.

    Returns:
        str: A fully-formed HTML string with the escaped user content.
    """
    # Define a simple template where `{user_content}` is the placeholder
    html_template = (
        "<!DOCTYPE html>\n"
        "<html lang=\"en\">\n"
        "  <head>\n"
        "    <meta charset=\"UTF-8\">\n"
        "    <title>User Content</title>\n"
        "  </head>\n"
        "  <body>\n"
        "    <div class=\"content\">\n"
        "      {user_content}\n"
        "    </div>\n"
        "  </body>\n"
        "</html>"
    )

    # Escape the user content to neutralize any HTML special characters
    escaped_content = html.escape(input_content, quote=True)

    # Safely insert the escaped content into the template
    final_html = html_template.replace("{user_content}", escaped_content)

    return final_html