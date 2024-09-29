import sql3Funcs

def getColumnValues(path, table_name, index):
    table = sql3Funcs.get_from_table(path, table_name)
    column = list()

    for string in table:
        column.append(string[index])

    return column

def toListBySep(text, sep):
    arr = text.split(sep)

    while '' in arr:
        arr.remove('')

    return arr
