import requests

def search_paper(author, title, max_results=10):
    url = f"https://api.crossref.org/works?query.author={author}&query.title={title}&rows={max_results}"
    print(url)
    headers = {"Crossref-User-Agent": "lxy61490267@163.com"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        papers = response.json()["message"]["items"]
        for paper in papers:
            print(f"DOI: {paper['DOI']}")
            print(f"Title: {paper['title'][0]}")
            print(f"Abstract: {paper.get('abstract', 'No abstract available')}")
            print("-" * 80)
    else:
        print(f"Error: {response.status_code}")

if __name__ == "__main__":
    author = "guan huang"
    title = "carbon material"
    search_paper(author, title)
