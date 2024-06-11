notes = []

def countDifference(string1: str, string2: str) -> int:
    return sum([0 if string1[i] == string2[i] else 1 for i in range(min(len(string1), len(string2)))])

def countMirroredDifference(line_string: str, index: int) -> int:
    return countDifference(line_string[:index][::-1], line_string[index:])

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
    row_overlap_counts = [0] * number_of_columns
    column_overlap_counts = [0] * number_of_rows

    for row in note:
        for i in row_symmetry_range:
            row_overlap_counts[i] += countMirroredDifference(row, i)

    row_symmetries = [i for i, row_count in enumerate(row_overlap_counts) if row_count == 1]

    for j in range(number_of_columns):
        column = getColumnAt(note, j)
        for i in columns_symmetry_range:
            column_overlap_counts[i] += countMirroredDifference(column, i)
            
    column_symmetries = [i for i, col_count in enumerate(column_overlap_counts) if col_count == 1]

    day1Result += sum(row_symmetries) + 100 * sum(column_symmetries)

print(day1Result)
