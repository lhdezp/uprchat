

def is_document_link( url: str) -> bool:
        extensions = ["pdf", "doc", "txt"]
        return any(ext in url for ext in extensions)

def parse_docs(response):
    print(f"url:{response.url} content is a document")
    data = {
        "title": f'url: {response.url}',
        "content": f'DOCUMENT content:',
        "body": f'{str(response)}'
        }

    return data
