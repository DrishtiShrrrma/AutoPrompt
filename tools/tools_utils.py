from langchain_core.tools import tool
from typing import Optional
from .browser import SimpleTextBrowser
from .cookies import COOKIES_LIST, COOKIES


# Initialize the browser instance
browser = SimpleTextBrowser()

@tool(name="navigate_to_address", description="Navigate to a given address in the browser")
def navigate_to_address_tool(address: str, filter_year: Optional[int] = None) -> str:
    """Navigate to a given web address in the browser."""
    browser.set_address(address, filter_year)
    return browser.viewport

@tool(name="find_text_on_page", description="Find text on the current web page")
def find_text_on_page_tool(query: str) -> Optional[str]:
    """Find a specific query on the current web page."""
    return browser.find_on_page(query)

@tool(name="page_down", description="Move to the next page in the browser viewport")
def page_down_tool() -> str:
    """Move to the next page in the browser."""
    browser.page_down()
    return browser.viewport

@tool(name="page_up", description="Move to the previous page in the browser viewport")
def page_up_tool() -> str:
    """Move to the previous page in the browser."""
    browser.page_up()
    return browser.viewport


# tools from cookies.py

@tool(name="get_cookies_list", description="Get the list of stored cookies")
def get_cookies_list_tool() -> list:
    """Returns the list of all cookies stored."""
    return COOKIES_LIST

@tool(name="get_cookie_by_name", description="Get a specific cookie by its name")
def get_cookie_by_name_tool(cookie_name: str) -> Optional[dict]:
    """Returns a cookie by its name if it exists in the cookie list."""
    for cookie in COOKIES_LIST:
        if cookie['name'] == cookie_name:
            return cookie
    return None

@tool(name="add_cookie", description="Add a cookie to the cookie jar")
def add_cookie_tool(cookie: dict) -> str:
    """Adds a cookie to the cookie jar."""
    try:
        COOKIES.set(
            cookie['name'], cookie['value'], domain=cookie['domain'], path=cookie['path']
        )
        return f"Cookie {cookie['name']} added successfully."
    except KeyError:
        return "Invalid cookie format. Please ensure the cookie contains 'name', 'value', 'domain', and 'path'."

@tool(name="list_all_cookies", description="List all cookies in the cookie jar")
def list_all_cookies_tool() -> list:
    """Lists all cookies currently in the RequestsCookieJar."""
    return [{c.name: c.value} for c in COOKIES]
