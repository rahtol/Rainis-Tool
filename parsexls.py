import pandas as pd
import re


def col_rename(colname: str):
    if colname.startswith('Project Value'):
        return 'Project Value'
    else:
        return colname


def is_sheet_relevant(sheet, sheetname):
    ok = set(['Parameter Name', 'Project Value', 'Related Component']) <= set(sheet.columns)
    return ok


def parse_sheet(sheet, odict, sheetname):
    for index, row in sheet.iterrows():
        related_component = str(row['Related Component']).upper()
        if related_component in ['OBCU_ATP', 'SYSTEM']:
            identifier = row['Parameter Name']
            value = str(row['Project Value'])
            match = re.fullmatch(r'\d+', value)
            if match:
                odict[identifier] = int(value)
            else:
                # print(f'non-numerical value for "{identifier}": "{value}"')
                odict[identifier] = value  # store as str instead


def parse_xls(infname, odict):
    xls = pd.read_excel(infname, sheet_name=None)
    for key, sheet in xls.items():
        sheet.rename(columns=col_rename, inplace=True)
        if is_sheet_relevant(sheet, key):
            print(f'    parsing sheet: {key}')
            parse_sheet(sheet, odict, key)


def get_xlsitems(infname):
    xlsitems = dict()
    parse_xls(infname, xlsitems)
    return xlsitems
