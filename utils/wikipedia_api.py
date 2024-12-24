import requests

# Base Wikipedia API URL
WIKIPEDIA_API_URL = 'https://en.wikipedia.org/w/api.php'

# Utility function to search Wikipedia
def search_wikipedia(term: str) -> dict:
    """
    Search Wikipedia for the given term.

    Args:
        term (str): The term to search for.

    Returns:
        dict: The first search result, including title, snippet, and URL.
        None: If no results are found or an error occurs.
    """
    # Define the API request parameters
    params = {
        'action': 'query',        # API action to query Wikipedia
        'format': 'json',         # Format of the response
        'list': 'search',         # Specify a search query
        'srsearch': term,         # The search term
        'utf8': 1                # Ensure UTF-8 encoding
    }

    try:
        # Send a GET request to the Wikipedia API
        response = requests.get(WIKIPEDIA_API_URL, params=params)
        response.raise_for_status()  # Raise an error for HTTP issues

        # Parse the JSON response
        data = response.json()
        search_results = data.get('query', {}).get('search', [])

        # Return None if no results are found
        if not search_results:
            return None

        # Extract the first result's title, snippet, and URL
        result = search_results[0]
        title = result['title']
        snippet = result['snippet'].replace('<span class="searchmatch">', '').replace('</span>', '')
        url = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"

        # Fetch the page image if available
        image_params = {
            'action': 'query',
            'format': 'json',
            'prop': 'pageimages',
            'titles': title,
            'pithumbsize': 300
        }
        image_response = requests.get(WIKIPEDIA_API_URL, params=image_params)
        image_response.raise_for_status()
        image_data = image_response.json()
        page = image_data.get('query', {}).get('pages', {})
        image_url = None
        for page in page.values():
            image_url = page.get('thumbnail', {}).get('source')
            break

        return {
            'title': title,
            'snippet': snippet,
            'url': url,
            'image_url': image_url
        }

    except (requests.RequestException, ValueError) as e:
        # Print error message and return None
        print(f"Error fetching data from Wikipedia API: {e}")
        return None

def get_random_article() -> dict:
    """
    Get a random article from Wikipedia.

    Returns:
        dict: The random article's title, URL, and image if available.
        None: If an error occurs.
    """
    params = {
        'action': 'query',
        'format': 'json',
        'generator': 'random',
        'grnnamespace': 0,
        'prop': 'pageimages|info',
        'inprop': 'url',
        'pithumbsize': 500
    }

    try:
        response = requests.get(WIKIPEDIA_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        pages = data.get('query', {}).get('pages', {})
        if not pages:
            return None

        page = next(iter(pages.values()))
        title = page['title']
        url = page['fullurl']
        image_url = page.get('thumbnail', {}).get('source')

        return {
            'title': title,
            'url': url,
            'image': image_url
        }

    except (requests.RequestException, ValueError) as e:
        print(f"Error fetching random article from Wikipedia API: {e}")
        return None

def get_trending_articles() -> list:
    """
    Fetch the most viewed articles currently trending on Wikipedia.

    Returns:
        list: A list of dictionaries, each containing title, URL, and optionally an image.
        None: If an error occurs.
    """
    params = {
        'action': 'query',
        'format': 'json',
        'list': 'mostviewed',  # Correct API parameter for trending articles
        'pvimlimit': 10        # Limit to top 10 articles
    }

    try:
        response = requests.get(WIKIPEDIA_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        # Debug: Print API response to verify structure
        print(data)

        # Access the most viewed articles
        most_viewed = data.get('query', {}).get('mostviewed', [])
        if not isinstance(most_viewed, list):
            print("Unexpected data structure for 'mostviewed':", most_viewed)
            return None

        # Process the articles into a usable format
        articles = []
        for article in most_viewed:
            title = article.get('title', 'No Title')
            url = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
            articles.append({
                'title': title,
                'url': url
            })

        return articles

    except (requests.RequestException, ValueError) as e:
        print(f"Error fetching trending articles from Wikipedia API: {e}")
        return None

def get_article_categories(title: str) -> list:
    """
    Fetch the categories of a specific Wikipedia article.

    Args:
        title (str): The title of the article.

    Returns:
        list: A list of categories.
        None: If an error occurs.
    """
    params = {
        'action': 'query',
        'format': 'json',
        'titles': title,
        'prop': 'categories',
        'cllimit': 'max'
    }

    try:
        response = requests.get(WIKIPEDIA_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        pages = data.get('query', {}).get('pages', {})
        categories = []

        for page in pages.values():
            for category in page.get('categories', []):
                categories.append(category['title'])

        return categories

    except (requests.RequestException, ValueError) as e:
        print(f"Error fetching categories for article '{title}': {e}")
        return None

def get_article_sections(title: str) -> list:
    """
    Fetch the sections of a specific Wikipedia article.

    Args:
        title (str): The title of the article.

    Returns:
        list: A list of sections with their titles and level.
        None: If an error occurs.
    """
    params = {
        'action': 'parse',
        'format': 'json',
        'page': title,
        'prop': 'sections'
    }

    try:
        response = requests.get(WIKIPEDIA_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        sections = data.get('parse', {}).get('sections', [])
        return [{'title': section['line'], 'level': section['level']} for section in sections]

    except (requests.RequestException, ValueError) as e:
        print(f"Error fetching sections for article '{title}': {e}")
        return None