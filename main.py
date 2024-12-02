from parsebabs import get_babitems
from parsexls import get_xlsitems
from time import time

version = 'Rainis tool, v1.00, 01-12-2024'

def check_babitems(babitems, xlsitems, outfn):
    counts = {'ok int': 0, 'ok str': 0, 'value_mismatch': 0, 'type_mismatch': 0, 'key_not_found_error': 0}
    with open(outfn, 'w') as f:
        for identifier, value in babitems.items():
            if identifier in xlsitems:
                if isinstance(value, int) and isinstance(xlsitems[identifier], int):
                    if xlsitems[identifier] == value:
                        counts['ok int'] += 1
                        f.write(f'ok int {identifier}, value={value}\n')
                    else:
                        counts['value_mismatch'] += 1
                        f.write(f'int value mismatch on "{identifier}": bab={value}, xls={xlsitems[identifier]}\n')
                elif isinstance(value, str) and isinstance(xlsitems[identifier], str):
                    if xlsitems[identifier] == value:
                        counts['ok str'] += 1
                        f.write(f'ok str {identifier}, value="{value}"\n')
                    else:
                        counts['value_mismatch'] += 1
                        f.write(f'str value mismatch on "{identifier}": bab={value}, xls={xlsitems[identifier]}\n')
                else:
                    counts['type_mismatch'] += 1
                    f.write(f'type mismatch on "{identifier}": bab={value}, xls={xlsitems[identifier]}\n')
            else:
                counts['key_not_found_error'] += 1
                f.write(f'key not found in xls error: "{identifier}"\n')
        f.close()
    return counts


t0 = time()
print(version)

babitems = get_babitems('./data_in')
# print(babitems)
print(f'babitems: #entries={len(babitems)}')

t1 = time()
xlsitems = get_xlsitems('data_in\TGMT_Configuration_Data_Line6_R3_2_8_A6Z00057582214_-.xlsx')
# print(xlsitems)
num_int_entries = sum(1 for val in xlsitems.values() if isinstance(val, int))
print(f'xlsitems: #total_entries={len(xlsitems)}, #numerical_entries={num_int_entries}')

counts = check_babitems(babitems, xlsitems, './data_out/check_babitems.log')
print('check_babitems: ', counts)

t2 = time()
print(f'processing time: {t2 - t0} seconds')
