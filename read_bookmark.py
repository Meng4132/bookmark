from PyPDF2 import PdfFileReader as pdfreader
from PyPDF2.generic import Destination


class _PageFinder:
    def __init__(self, reader):
        '''Build a dict
            self.page_map -> {IndirectObject: page_num}'''
        self.reader = reader
        self.page_map = {str(self.reader.getPage(i)): i
                        for i in range(self.reader.numPages)}

    def get(self, obj) -> int:
        '''Return the page number of the Page IndirectObject'''
        return self.page_map[str(obj)]


def get_outlines(reader):
    outlines = reader.getOutlines()
    pf = _PageFinder(reader)
    n = 0

    def _get(reader, outlines, pf, n):
        for outline in outlines:
            if type(outline) == Destination:
                prefix = '\t' * n
                title, page = outline['/Title'], pf.get(outline['/Page'])
                print(f'{prefix}{title} {page}')  # format string
            else:
                n += 1
                _get(reader, outline, pf, n)
                n -= 1
    _get(reader, outlines, pf, n)


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: python read_bookmark.py {pdf_file_path}')
        exit()
    pdf_file_path = sys.argv[1]
    with open(pdf_file_path, 'rb') as f:
        reader = pdfreader(f)
        get_outlines(reader)
