import html

def build_html_page(page_content: str) -> str:
    """
    Injects user-supplied content into an HTML template safely by escaping
    special characters to prevent XSS attacks.

    Parameters:
        page_content (str): Dynamic content provided by the user.

    Returns:
        str: The final HTML string with escaped user content.
    """
    # Define the base template with a placeholder for dynamic content
    html_template = (
        "<!DOCTYPE html>\n"
        "<html lang=\"en\">\n"
        "<head><meta charset=\"UTF-8\"><title>Page</title></head>\n"
        "<body>{user_content}</body>\n"
        "</html>"
    )

    # Escape the user content to neutralise any HTML/JS injection
    escaped_content = html.escape(page_content, quote=True)

    # Format the template with the escaped content
    return html_template.format(user_content=escaped_content)