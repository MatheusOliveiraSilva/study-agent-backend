from langchain_tavily import TavilySearch
from app.settings import TAVILY_API_KEY

web_search_tool = TavilySearch(
    tavily_api_key=TAVILY_API_KEY,
    max_results=5,
    topic="general",
    # include_answer=False,
    # include_raw_content=False,
    # include_images=False,
    # include_image_descriptions=False,
    # search_depth="basic",
    # time_range="day",
    # include_domains=None,
    # exclude_domains=None
)

def web_search(query: str) -> str:
    """
    Use tavily for smart and optimized web search.

    Return is like: 
        {
            "query": "euro 2024 host nation", 
            "follow_up_questions": null, 
            "answer": null, 
            "images": [], 
            "results": [
                {
                    "title": "UEFA Euro 2024 - Wikipedia", 
                    "url": "https://en.wikipedia.org/wiki/UEFA_Euro_2024", 
                    "content": "Tournament details Host country Germany Dates 14 June...
                } ...
            ]
        }

    We want to extract the "results" field and return as a big string called "web_search_context".
    In this string we will format including source and title too.

    Return format:
        Here are the web search results for the query: <query>
        ---
        <result 1>
        <result 2>
        ...
        <result n>

    Args:
        query (str): The query to search the web for.

    Returns:
        str: The web search results.
    """
    search_result = web_search_tool.invoke(query)

    web_search_context = "Here are the web search results for the query: " + query + "\n---\n"
    for result in search_result["results"]:
        web_search_context += f"Source: {result['url']}\nTitle: {result['title']}\nContent: {result['content']}\n---\n"

    return web_search_context
