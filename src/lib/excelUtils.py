
from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.writer.excel import ExcelWriter
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE


def writeExcelRow(workSheet, headers, rowIndex, data):
    cellIndex = 1
    for head in headers:
        try:
            if head in info:
                content = ILLEGAL_CHARACTERS_RE.sub(r'', data[head])
                workSheet.cell(rowIndex, cellIndex).value = content.strip()
            else:
                workSheet.cell(rowIndex, cellIndex).value = ""
            cellIndex = cellIndex+1
        except:
            print(rowIndex)


def writeExcel(workSheet, headers, products):
    for index, head in headers:
        workSheet.cell(1, index+1).value = head.strip()

    for index, p in products:
        writeExcelRow(workSheet, headers, index + 2, p)
