# 猜测是为了创建excel
import xlsxwriter
workbook = xlsxwriter.Workbook("chart_line.xlsx")
worksheet = workbook.add_worksheet()
headings = ['Number', '恶意访问', '善意访问']
data = [
    range(1, 1001),
    [10, 40, 50, 20, 10, 50],
    [30, 60, 70, 50, 40, 30],
]

worksheet.write_row('A1', headings)

worksheet.write_column('A2', data[0])
worksheet.write_column('B2', data[1])
worksheet.write_column('C2', data[2])

workbook.close()