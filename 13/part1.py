notes = []

def oneStartsWithOther(string1: str, string2: str) -> bool:
    return string1.startswith(string2) or string2.startswith(string1)

def isSymmetricAt(line_string: str, index: int) -> bool:
    return oneStartsWithOther(line_string[:index][::-1], line_string[index:])

def getColumnAt(note: [str], col_index: int) -> str:
    return ''.join([row[col_index] for row in note])

day1Result = 0

with open('input.txt', encoding="utf-8") as f:
    note = []
    for line in f.readlines():
        if line == '\n':
            notes.append(note)
            note = []
            continue

        note.append(line[:len(line) - 1])

    notes.append(note)

for note in notes:
    number_of_columns = len(note[0])
    number_of_rows = len(note)
    row_symmetry_range = range(1, number_of_columns)
    columns_symmetry_range = range(1, number_of_rows)
    row_symmetries = list(row_symmetry_range)
    columns_symmetries = list(columns_symmetry_range)

    for row in note:

        for i in row_symmetry_range:
            if not i in row_symmetries:
                continue

            if not isSymmetricAt(row, i):
                row_symmetries.remove(i)

    for j in range(number_of_columns):
        column = getColumnAt(note, j)

        for i in columns_symmetry_range:
            if not i in columns_symmetries:
                continue

            if not isSymmetricAt(column, i):
                columns_symmetries.remove(i)

    day1Result += sum(row_symmetries) + 100 * sum(columns_symmetries)

print(day1Result)
