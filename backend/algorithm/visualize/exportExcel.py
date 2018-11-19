import xlsxwriter
# 生成用于word作图的excel表格
def export(X, label_pred):
    cluster1 = []
    cluster2 = []
    j = 0

    for i in label_pred:
        if (i == 1):
            cluster1.append(X[j][4])
        else:
            cluster2.append(-X[j][4])
        j += 1

    workbook = xlsxwriter.Workbook("网页标签.xlsx")
    worksheet = workbook.add_worksheet()
    headings = ['用户访问编号', '恶意访问', '善意访问']
    data = [
        range(0, 1000),
        cluster1[0:1000],
        cluster2[0:1000]
    ]

    worksheet.write_row('A1', headings)

    worksheet.write_column('A2', data[0])
    worksheet.write_column('B2', data[1])
    worksheet.write_column('C2', data[2])

    workbook.close()