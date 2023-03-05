# Imports
import html2text
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from bs4.formatter import HTMLFormatter
import requests
import os
import sys

sys.setrecursionlimit(1000000)  # solve problem 'maximum recursion depth exceeded'

##Classes
class UnsortedAttributes(HTMLFormatter):
    def attributes(self, tag):
        for k, v in tag.attrs.items():
            yield k, v
            
## Functions

def recursively_translate(node):
    for x in range(len(node.contents)):
        if isinstance(node.contents[x], str):
            if node.contents[x].strip() != '':
                try:
                    node.contents[x].replaceWith(GoogleTranslator(source='en', target='hi').translate(node.contents[x]))
                except:
                    pass
        elif node.contents[x] != None:
            recursively_translate(node.contents[x])

def chunkstring(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))

# File Directory
files_from_folder = r"C:\Users\devil\Desktop\My Web Sites\Translator Class Central\www.classcentral.com\report\online-learning-deals"
use_translate_folder = False
destination_language = 'hi'  
extension_file = ".html"
directory = os.fsencode(files_from_folder)

# H2T textmaker construction
textmaker = html2text.HTML2Text()
textmaker.ignore_links = True
textmaker.bypass_tables = False
textmaker.images_to_alt = True
textmaker.protect_links = True

# Open the file
with open("www.classcentral.com\index.html", 'r', encoding="utf-8") as HTMLFile:
    index = HTMLFile.read()
    soup = BeautifulSoup(index, features='html.parser')
    text = textmaker.handle(index)
    lines = (i.strip() for i in text.splitlines())
    test = soup.get_text()
    


# Walk thruogh the file and translate them            
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    print(filename)
    if filename == 'y_key_e479323ce281e459.html' or filename == 'directory.html': #ignore this 2 files
        continue
    if filename.endswith(extension_file):
        with open(os.path.join(files_from_folder, filename), encoding='utf-8') as html:
            soup = BeautifulSoup('<pre>' + html.read() + '</pre>', 'html.parser')
            for title in soup.findAll('title'):
                recursively_translate(title)
                    
            for meta in soup.find_all('meta', {'name': 'description'}):
                try:
                    recursively_translate(meta)
                except:
                    pass    
                
            for node in soup.find_all('header'):
                try:
                    recursively_translate(node)
                except:
                    pass
                
            for body in soup.find_all('body',class_=''):
                try:
                    recursively_translate(body)
                except:
                    pass            
            for p in soup.find_all('p'):
                try:
                    recursively_translate(p)
                except:
                    pass 
                    
            for a in soup.find_all('a'):
                try:
                    recursively_translate(a)
                except:
                    pass 
        # Creata a new html file                
        print(f'{filename} translated')
        soup = soup.encode(formatter=UnsortedAttributes()).decode('utf-8')
        new_filename = f'{filename.split(".")[0]}_{destination_language}.html'
        if use_translate_folder:
            try:
                with open(os.path.join(files_from_folder+r'\\translated', new_filename), 'w', encoding='utf-8') as new_html:
                    new_html.write(soup[5:-6])
            except:
                os.mkdir(files_from_folder+r'\translated')

                with open(os.path.join(files_from_folder+r'\\translated', new_filename), 'w', encoding='utf-8') as new_html:
                    new_html.write(soup[5:-6])
        else:
            with open(os.path.join(files_from_folder, new_filename), 'w', encoding='utf-8') as html:
                html.write(soup[5:-6])    