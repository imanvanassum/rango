import json, os
import urllib.parse
import urllib.request

def main():
    s = input('Enter search query:')
    a = run_query(s)
    print(a)
    
def read_webhose_key():
    webhose_api_key = None
    script_full_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_full_path)
    one_dir_lower = os.path.dirname(script_dir)
    key_in_base_dir = os.path.join(one_dir_lower,'search.key')
    key_in_app_dir = os.path.join(script_dir,'search.key')


    try:
        with open(key_in_base_dir, 'r') as f:
            webhose_api_key = f.readline().strip()
    except:
        try:
            with open(key_in_app_dir, 'r') as f:
                webhose_api_key = f.readline().strip()
        except:
            raise IOError('search.key file not found')

    return webhose_api_key

def run_query(search_terms, size=10):
    """
    Given a string containing search terms (query), and a number or results to
    return (default of 10), returns a list of results from Webhose, with each
    result consisting of a title, link and summary
    """
    webhose_api_key = read_webhose_key()

    if not webhose_api_key:
        raise KeyError('Webhose key not found')

    root_url = 'http://webhose.io/search'
    query_string = urllib.parse.quote(search_terms)
    search_url = ('{root_url}?token={key}&format=json&q={query}'
                '&sort=relevancy&size={size}').format(
                root_url=root_url,key=webhose_api_key,
                query=query_string, size=size)

    results = []

    try:
        response = urllib.request.urlopen(search_url).read().decode('utf-8')
        json_response = json.loads(response)

        for post in json_response['posts']:
            results.append({'title': post['title'],
                            'link': post['url'],
                            'summary': post['text'][:200]})
    except:
        print("Error when querying the Webhose API")

    return results

if __name__ == '__main__':
    main()
