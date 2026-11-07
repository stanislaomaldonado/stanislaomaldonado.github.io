"""Replace a registered PDF while preserving every public link to it."""
import argparse
from datetime import date
from hashlib import sha256
import io
import json
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--id', required=True, help='Document ID from content/documents.json')
    parser.add_argument('--source', type=Path, required=True, help='Replacement PDF')
    parser.add_argument('--version', required=True, help='Version date or descriptive label')
    args = parser.parse_args()
    catalog_path = ROOT / 'content/documents.json'
    catalog = json.loads(catalog_path.read_text(encoding='utf-8'))
    document = next((doc for doc in catalog['documents'] if doc['id'] == args.id), None)
    if document is None:
        parser.error(f'Unknown document ID: {args.id}')
    destination = (ROOT / document['path']).resolve()
    if not destination.is_relative_to(ROOT / 'documents') or destination.suffix != '.pdf':
        parser.error('The catalog destination must be a PDF under documents/')
    data = args.source.read_bytes()
    if not data.startswith(b'%PDF-'):
        parser.error('The source is not a PDF')
    if len(data) >= 95 * 1024 * 1024:
        parser.error('The PDF must be smaller than 95 MiB')
    pdf = PdfReader(io.BytesIO(data))
    if pdf.is_encrypted or not pdf.pages:
        parser.error('The PDF must contain pages and open without a password')
    document.update(version=args.version, bytes=len(data), sha256=sha256(data).hexdigest(),
                    pages=len(pdf.pages), updated=date.today().isoformat())
    temporary = destination.with_suffix('.pdf.tmp')
    temporary.write_bytes(data)
    temporary.replace(destination)
    catalog_path.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(json.dumps({'id':args.id, 'path':document['path'], 'pages':document['pages'],
                      'version':args.version, 'bytes':len(data)}))

if __name__ == '__main__':
    main()
