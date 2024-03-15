import requests
def semantic(papers):
     rs = []
     for paper in papers:
        title = paper.get('title', '')
        year = paper.get('year', '') # Assuming you have a function parse_year to process the year
        author_names = [author.get('name', '') for author in paper.get('authors', [])]
        if not author_names:
            continue
        author = ', '.join(author_names) # Assuming you have a function parse_author_name to process the author names
        abstract = paper.get('abstract', '')
        pdf_url = paper.get('openAccessPdf', {}).get('url', '') if paper.get('openAccessPdf') else ''
        if (abstract != '' and pdf_url!= ''):
            rs.append({
            'id': len(rs),
            'title': title,
            'author': author,
            'authors': author_names,
            'published': year,
            'pdf_url': pdf_url,
            'abstract': abstract
        })
        else:
            continue
     if (len(rs)>5):
        rs = rs[:5]
     return rs
def search_in_semantic(query: str, max_results: int = 40) -> dict:
    # Define the headers with the API key
    headers = {
        'x-api-key': 'fXtwPJIYby5MEMOJdrN067O7rtfDrs3O7TKZbzMt'
    }
    
    # Define the query parameters
    params = {
        'query': query,
        'limit': max_results,
    }
    
    # Make the GET request
    response = requests.get('https://api.semanticscholar.org/graph/v1/paper/search', params=params, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        res = response.json()
        Ids = [str(s['paperId']) for s in res['data']]
        # The data to send in the request
        data = {
            'ids': Ids
                }
        response = requests.post('https://api.semanticscholar.org/graph/v1/paper/batch?fields=title,year,authors,openAccessPdf,abstract', json=data, headers=headers)
        return response.json()
    else:
        # Handle the error, for example, by raising an exception or returning an error message
        raise Exception(f"Request failed with status code {response.status_code}")
'''
# Example usage
query = 'canada'
try:
    results = search_in_semantic(query)
    print(results)
    print(semantic(results))
except Exception as error:
    print(f'Error: {error}')
'''