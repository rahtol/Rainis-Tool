from pathlib import Path
import io
import re


def parse_all_babs(directory, odict):
    pathlist = Path('./data_in').glob('**/*.bab')
    for path in pathlist:
        # because path is object not string
        path_in_str = str(path)
        print(f'    parse bab: {path_in_str}')
        parse_bab(path_in_str, odict)


def parse_bab(fn: str, odict):
    with open(fn, 'rb') as f:
        f.seek(0, 2)  # move the cursor to the end of the file
        size = f.tell()  # total number of bytes in file
        f.seek(128, 0)  # move cursor to byte 128 from start of file
        sb = f.read(size - 256)  # reduce size to read of file by header plus footer size
        s = sb.decode('cp1252')  # utf-8 doesn't work because of german umlaute !
        buf = io.StringIO(s)
        for line in buf:
            match = re.search(r'(\w+)\s*[=]\s*([\d,]+)[;]', line)
            if match:
                identifier = match.group(1)
                value = match.group(2)
                if re.fullmatch(r'\d+', value):
                    odict[identifier] = int(value)
                else:
                    odict[identifier] = value


def get_babitems(indir):
    babitems = {}
    parse_all_babs(indir, babitems)
    return babitems
