
import xlsxwriter as excel
import pandas as pd

from constants import *

global workbook
global worksheet


def createExcelWriter(name):
    file_name = './results/' +name+ '.xlsx'
    print("Creating file: " + file_name)
    return pd.ExcelWriter(file_name, engine='xlsxwriter')

def createExcelFile(name):
    workbook = excel.Workbook('./results/' + name + '.xlsx')
    # worksheet = workbook.add_worksheet()

    return workbook

def closeExcelFile(workbook):
    workbook.close()


# Insert Header columns into Excel
def create_excel_header_cols(worksheet):
    worksheet.write(0, YEAR_COL, 'YEAR')
    worksheet.write(0, YARDS_COL, 'YARDS')
    worksheet.write(0, TDS_COL, 'TDS')
    worksheet.write(0, GS_COL, 'GS')
    return worksheet

# Insert Data as rows into table. 
def insert_row_data(worksheet, row, year, total):
    worksheet.write(row, YEAR_COL, year)
    worksheet.write(row, YARDS_COL, total['Yds'])
    worksheet.write(row, TDS_COL, total['TD'] )
    worksheet.write(row, GS_COL, total['GS'])
    return worksheet

def writeToTable(df, writer, sheetName):    
    df.to_excel(writer, sheet_name=sheetName, startrow=2, startcol=0, header=True)
    writer.save()