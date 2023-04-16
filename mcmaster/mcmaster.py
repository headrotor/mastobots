import subprocess
import os

#$ python -m pip install pypdf2

#import PyPDF2

page_n = 1001
url = f"https://www.mcmaster.com/catalog/128/{page_n}/"
fname = f"page-{page_n}.pdf"

from pdfrw import PdfReader

def get_pdf_links(file_path):
    pdf = PdfReader(file_path)
    urls = []
    for page in pdf.pages:
        annotations = page['/Annots']
        if annotations:
            for annotation in annotations:
                annotation_obj = annotation.resolve()
                if annotation_obj['/Subtype'] == '/Link':
                    action = annotation_obj['/A']
                    if action and action['/S'] == '/URI':
                        url = action['/URI']
                        urls.append(url)
    return urls

def get_pdf_linksOLD(file_path):
    with open(file_path, 'rb') as file:
        pdf = PyPDF2.PdfReader(file)
        urls = []
        for page in range(pdf.getNumPages()):
            page_obj = pdf.getPage(page)
            annotations = page_obj.get('/Annots')
            if annotations:
                for annotation in annotations:
                    annotation_obj = annotation.getObject()
                    if annotation_obj.get('/A'):
                        url = annotation_obj['/A']['/URI']
                        urls.append(url)
    return urls

print(' '.join(['curl', '-o', fname, url]))
process = subprocess.Popen(['curl', '-o', fname, url], stderr=subprocess.PIPE)
output, error = process.communicate()
if process.returncode != 0:
    print("Curl error")
    print(error.decode('utf-8'))

if os.path.exists(fname):
    urls = get_pdf_links(fname)
    print(urls)
else:
    print(f'File {fname} does not exist')
