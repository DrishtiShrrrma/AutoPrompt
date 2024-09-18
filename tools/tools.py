# tools.py

from langchain.tools import Tool
from sibyl import Sibyl

# Initializing an instance of Sibyl
sibyl_instance = Sibyl()

# Wrapping Sibyl's methods into LangChain-compatible tools

browser_state_tool = Tool(
    func=sibyl_instance.browser_state,
    name="BrowserState",
    description="Provides the current state of the browser, including address, title, and viewport."
)

informational_web_search_tool = Tool(
    func=sibyl_instance.informational_web_search,
    name="InformationalWebSearch",
    description="Executes an informational web search and returns the state and content of the page."
)

navigational_web_search_tool = Tool(
    func=sibyl_instance.navigational_web_search,
    name="NavigationalWebSearch",
    description="Conducts a navigational web search and visits the first extracted link, providing the final page content."
)

visit_page_tool = Tool(
    func=sibyl_instance.visit_page,
    name="VisitPage",
    description="Visits a specified URL using the browser and returns the state and content of the page."
)

page_up_tool = Tool(
    func=sibyl_instance.page_up,
    name="PageUp",
    description="Scrolls the browser page up and provides the updated viewport information."
)

page_down_tool = Tool(
    func=sibyl_instance.page_down,
    name="PageDown",
    description="Scrolls the browser page down and provides the updated viewport information."
)

download_file_tool = Tool(
    func=sibyl_instance.download_file,
    name="DownloadFile",
    description="Downloads a file from the specified URL and returns the state of the page."
)

find_on_page_tool = Tool(
    func=sibyl_instance.find_on_page_ctrl_f,
    name="FindOnPage",
    description="Searches for a string on the current page and returns the search result along with the page content."
)

find_next_tool = Tool(
    func=sibyl_instance.find_next,
    name="FindNext",
    description="Finds the next occurrence of the previously searched string on the current page."
)

computer_terminal_tool = Tool(
    func=sibyl_instance.computer_terminal,
    name="ComputerTerminal",
    description="Executes code in a terminal-like environment and returns the status code and output."
)

ask_tool = Tool(
    func=sibyl_instance.ask,
    name="AskQuestion",
    description="Handles a question, determines the necessary steps and tools to answer it, and returns the final answer."
)

# List of all tools
all_tools = [
    browser_state_tool,
    informational_web_search_tool,
    navigational_web_search_tool,
    visit_page_tool,
    page_up_tool,
    page_down_tool,
    download_file_tool,
    find_on_page_tool,
    find_next_tool,
    computer_terminal_tool,
    ask_tool
]
