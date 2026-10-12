import html

def build_html_output(client_message: str, html_template: str) -> str:
    """
    Create an HTML response by safely inserting user-provided content into a
    template that contains the placeholder `{user_content}`.

    Parameters:
        client_message (str): The content supplied by the user.
        html_template (str): An HTML string that contains `{user_content}` where
                             the user content should be inserted.

    Returns:
        str: The resulting HTML with the user's content embedded safely.
    """
    # Escape user input to prevent XSS or other HTML injection attacks
    safe_content = html.escape(client_message, quote=True)

    # Replace the placeholder with the escaped content
    return html_template.replace("{user_content}", safe_content)