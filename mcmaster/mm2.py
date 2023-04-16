import subprocess
import os
import time
#$ python -m pip install pypdf2

#import PyPDF2

page_n = 1003
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

# print(' '.join(['curl', '-o', fname, url]))
# process = subprocess.Popen(['curl', '-o', fname, url], stderr=subprocess.PIPE)
# output, error = process.communicate()
# if process.returncode != 0:
#     print("Curl error")
#     print(error.decode('utf-8'))

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_experimental_option('prefs', {
    "download.default_directory": "/home/jtf/pdfs",
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True
})

driver = webdriver.Chrome(options=options)
driver.get(url)
driver.implicitly_wait(300)
time.sleep(30)

exit()
if os.path.exists(fname):
    urls = get_pdf_links(fname)
    print(urls)
else:
    print(f'File {fname} does not exist')
