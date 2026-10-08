import openpyxl

from config.config import EXCEL_FILE, SHEET_NAME


def read_excel():
    workbook = openpyxl.load_workbook(EXCEL_FILE)
    worksheet = workbook[SHEET_NAME]

    data = []
    keys = [cell.value for cell in worksheet[2]]
    for row in worksheet.iter_rows(min_row=3, values_only=True):
        dict_data = dict(zip(keys, row))
        if dict_data["is_true"]:
            data.append(dict_data)
    workbook.close()
    return data

