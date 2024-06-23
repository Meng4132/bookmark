from PyPDF2 import PdfFileReader as pdfreader, PdfFileWriter as pdfwriter


class BookMarkMaker:
    """Add bookmark to PDF file.
    pdf_path: the path to your pdf
    bookmark_path: """
    def __init__(self, pdf_path, bookmark_path, savepdf_path, offset=''):
        book = pdfreader(open(pdf_path, "rb"))
        pdf = pdfwriter()
        pdf.cloneDocumentFromReader(book)
        self.pdf = pdf
        self.bookmark_path = bookmark_path
        self.savepdf_path = savepdf_path
        self.offset = int(offset) if offset is not None else 0
    def process_bookmark(self):
        with open(self.bookmark_path) as f:
            cnt_list = [process(i.rstrip() for i in f.readlines() if i.strip() != ""]
        print("here:", cnt_list)
        self.marks = []
        self.pages = []
        self.levels = []
        for line in cnt_list:
            self.marks.append(' '.join(line.split(None, -1)[:-1]))
            self.pages.append(line.split(None, -1)[-1])
        for i in self.marks:
            self.levels.append(i.count(".") + 1)  # or '\t'
        self.info = [(title, page, level) for title, page, level in zip(self.marks, self.pages, self.levels)]
        self.add_bookmarks(self.info)

    def add_mark(self, title, page, parent_mark=None):
        if parent_mark:
            mark = self.pdf.addBookmark(
                title, self.offset + int(page), parent=parent_mark)
        else:
            mark = self.pdf.addBookmark(title, self.offset + int(page) - 1)
        return mark
    def add_bookmarks(self, info):
        bookmark_parents = []
        bookmark_parents.append(self.add_mark(info[0][0],
                                info[0][1]))
        for i in range(1, len(info)):
            if info[i][2] <= info[i-1][2]:
                if info[i][2] == 1:
                    bookmark_parents.clear()
                    bookmark_parents.append(self.add_mark(info[i][0], info[i][1]))
                    continue
                else:
                    bookmark_parents = bookmark_parents[:info[i][2]-1]
            bookmark_parents.append(self.add_mark(info[i][0], info[i][1], bookmark_parents[info[i][2]-2]))
    def save(self):
        with open(self.savepdf_path, "wb") as f:
            self.pdf.write(f)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print('Usage: python3 add_bookmark.py {pdf_path} {bookmark_path} {savepdf_path} [offset]')
        exit()
    offset = None
    pdf_path, bookmark_path, savepdf_path, *_ = sys.argv[1:]
    if ''.join(_).isdigit():
        offset = ''.join(_)
    bmm = BookMarkMaker(
        pdf_path,
        bookmark_path,
        savepdf_path,
        offset
    )
    bmm.process_bookmark()
    bmm.save()
    print('Saved:', savepdf_path)
