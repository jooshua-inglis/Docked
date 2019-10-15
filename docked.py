

import logging
import os
import argparse
import subprocess
import platform
import shelve
import shutil
import venv


logging.basicConfig(level=logging.DEBUG,format =' %(asctime)s = %(levelname)s  %(message)s')
logging.disable(logging.CRITICAL)

script_directory = os.path.dirname(os.path.realpath(__file__))

try:
    import markdown as md
    import mdx_math
except ModuleNotFoundError:
    script = {'Windows':'/setup.bat',
    'Linux':'/setup.sh',
    'OS X':'/setup.sh'}[platform.system()]
    subprocess.call(script_directory +  script)


pdf_converter = {'Windows':'wkhtmltox-win.exe',
                 'Linux':'wkhtmltopdf',
                 'OS X':'wkhtmltopdf'}[platform.system()]



def change_file(input_file,  new_extension, new_path=0,):
    output = os.path.splitext(input_file)[0] + new_extension
    output = os.path.join(new_path,os.path.basename(output))
    return (output)


def convert(doc_format=None, style=None, template=None, user_input=None, html_output=None):
    print('version 1.2.1')
    shelf = shelve.open(script_directory+'/data/info')
    try:
        if not shelf['name']:
            shelf['name'] = input('What is your name?: ')
    except:
        shelf['name'] = input('What is your name?: ')

    parser = argparse.ArgumentParser(description='My Markdown Converter')
    parser.add_argument('dir', nargs='*', type=str)
    parser.add_argument('-o', metavar='--output', help='The Output', type=str)
    parser.add_argument('-c', metavar='--css',    help='css file you want to use', type=str)
    parser.add_argument('-t', metavar='--html',   help='the html template you want to use', type=str)

    args = parser.parse_args()

    if args.dir:
        user_input = args.dir[0]
    elif user_input:
        pass
    else:
        user_input = input("What file do you want to convert? ")

    user_input = os.path.abspath(user_input)

    try:
        input_markdown = open(user_input,'r').read()
    except:
        print('Cannot open ' + user_input)
        return()

    html = md.markdown(input_markdown, extensions=['markdown.extensions.extra','markdown.extensions.nl2br','mdx_math'])

    if args.c:
        style = args.c

    if style:
        fallback_template = '{{ STYLE }} /n {{ BODY }}'
    else:
        fallback_template = '{{ BODY }}'

    if args.t:
        template = args.t

    if template:
        try:
            template = open(template,'r+').read()
        except:
            print('bad html template')
            template = fallback_template
    else:
        template = fallback_template

    html = template.replace('{{ BODY }}', html)

    if style:
        logging.debug('css')
        try:
            style = '<style>\n' + open(style,'r+').read() + '\n</style>'
            html = html.replace('{{ STYLE }}', style)
        except:
            html = html.replace('{{ STYLE }}', '')
            print('bad css template')


    if args.o:
        html_output = args.o
    elif len(args.dir) >= 2:
        html_output = args.dir[1]
    else:
        html_output = change_file(user_input, '.html', os.getcwd())

    pdf_output = change_file(html_output, '.pdf', os.getcwd())

    if doc_format == "html":
        open(html_output,'w').write(html)
        print('Done')
        return()
    elif doc_format == "pdf":
        subprocess.call([
            pdf_converter,
            '-q',
            '-T', '24.5',
            '-B', '14',
            '-R', '19',
            '-L', '19',
            '--header-line',
            '--header-font-size','9',
            '--header-right', '[date]',
            '--header-font-name', "'Open Sans'",
            '--header-spacing', '7',
            '--header-left', shelf['name'],
            '--header-center','[doctitle]',
            '--javascript-delay', '5000',
            '--footer-font-size', '9',
            '--footer-font-name', "'Open Sans'",
            '--footer-right','[page]',
            f"<({html})" ,pdf_output
            ])
        print('Done')


def to_pdf():
    convert('pdf',style=script_directory + '/data/style_sheet.css', template=script_directory + '/data/notes.html')


def change_css():
    parser = argparse.ArgumentParser(description='Change css file')
    parser.add_argument('dir', nargs=1, type=str)
    args = parser.parse_args()
    try:
        shutil.copyfile(args.dir[0], script_directory + '/data/style_sheet.css')
    except:
        print("error")

def change_name():
    shelf = shelve.open(script_directory+'/data/info')
    shelf['name'] = input('Enter name: ')


if __name__ == "__main__":
    to_pdf()