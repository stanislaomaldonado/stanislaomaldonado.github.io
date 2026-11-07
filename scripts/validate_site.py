"""Check local links, document identities and static hosting configuration."""
from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.links = []
        self.h1 = 0
    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == 'h1':
            self.h1 += 1
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        for key in ('src', 'href'):
            if key in attrs:
                self.links.append((attrs[key], attrs.get('data-document-id')))

def main():
    catalog = json.loads((ROOT / 'content/documents.json').read_text(encoding='utf-8'))
    documents = catalog['documents']
    assert len({d['id'] for d in documents}) == len(documents), 'Duplicate document IDs'
    assert len({d['path'] for d in documents}) == len(documents), 'Duplicate document paths'
    registry = {d['id']:d for d in documents}
    for doc in documents:
        path = (ROOT / doc['path']).resolve()
        assert path.is_relative_to(ROOT / 'documents'), doc['path']
        data = path.read_bytes()
        assert data.startswith(b'%PDF-'), doc['id']
        assert len(data) == doc['bytes'], doc['id']
        assert sha256(data).hexdigest() == doc['sha256'], doc['id']
        assert len(data) < 95 * 1024 * 1024, doc['id']
    actual_pdfs = {p.relative_to(ROOT).as_posix() for p in (ROOT / 'documents').rglob('*.pdf')}
    assert actual_pdfs == {d['path'] for d in documents}, 'Unregistered or missing PDFs'
    pages = {}
    for path in ROOT.rglob('*.html'):
        source = path.read_text(encoding='utf-8')
        assert 'dropbox.com' not in source, path
        assert '\ufffd' not in source, path
        page = Page()
        page.feed(source)
        assert page.h1 == 1, path
        assert len(page.ids) == len(set(page.ids)), path
        pages[path.resolve()] = page
    references = {ident:0 for ident in registry}
    link_count = 0
    for path, page in pages.items():
        for url, document_id in page.links:
            parsed = urlparse(url)
            if parsed.scheme or url.startswith('//'):
                continue
            target = (ROOT / unquote(parsed.path.lstrip('/'))) if parsed.path.startswith('/') else (path.parent / unquote(parsed.path)) if parsed.path else path
            target = target.resolve()
            assert target.is_relative_to(ROOT), (path, url)
            assert target.exists(), (path, url)
            if target.is_dir():
                target = target / 'index.html'
            if parsed.fragment and target.suffix == '.html':
                assert unquote(parsed.fragment) in pages[target].ids, (path, url)
            if document_id:
                assert document_id in registry, document_id
                assert target == (ROOT / registry[document_id]['path']).resolve(), (path, document_id)
                references[document_id] += 1
            if target.suffix == '.pdf':
                assert document_id, (path, url, 'PDF link missing document ID')
            link_count += 1
    assert all(references.values()), references
    for css in (ROOT / 'assets').glob('*.css'):
        for url in re.findall(r'url\([\'"]?([^\)\'\"]+)', css.read_text(encoding='utf-8')):
            assert (css.parent / url).exists(), (css.name, url)
    assert (ROOT / 'CNAME').read_text(encoding='utf-8').strip() == 'www.stanislaomaldonado.org'
    assert (ROOT / '.nojekyll').exists()
    print(json.dumps({'html_pages':len(pages), 'local_links_checked':link_count,
                      'documents':len(documents), 'document_links':sum(references.values()),
                      'total_pdf_bytes':sum(d['bytes'] for d in documents)}))

if __name__ == '__main__':
    main()
