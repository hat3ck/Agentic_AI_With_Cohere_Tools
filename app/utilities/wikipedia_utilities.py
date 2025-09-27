import requests


async def fetch_wikipedia_search_results(query: str) -> str:
    try:
        url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
        }
        headers = {
            "User-Agent": "CohereAssessment/1.0 (localhost)"
        }
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        # convert the search results to a readable string format
        search_results = data.get("query", {}).get("search", [])
        formatted_results = ""
        for result in search_results:
            title = result.get("title", "No Title")
            snippet = result.get("snippet", "No Snippet").replace("<span class=\"searchmatch\">", "").replace("</span>", "")
            page_url = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
            formatted_results += f"Title: {title}\nSnippet: {snippet}\nPage URL: {page_url}\n\n"
        return formatted_results
    except requests.RequestException as e:
        raise Exception(f"Error fetching Wikipedia search results: {str(e)}; location kWSB1wekaS")