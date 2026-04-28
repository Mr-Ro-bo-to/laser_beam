import xlsxwriter
import random

# Create workbook
workbook = xlsxwriter.Workbook('sales_report.xlsx')
worksheet = workbook.add_worksheet('Sales Data')

# --- Write data ---
headers = ['Month', 'Revenue', 'Expenses', 'Profit']
data = [
    ['Jan', 15000, 9000, 6000],
    ['Feb', 18000, 10500, 7500],
    ['Mar', 22000, 11000, 11000],
    ['Apr', 19000, 10000, 9000],
    ['May', 25000, 12000, 13000],
    ['Jun', 28000, 13500, 14500],
]

for col, header in enumerate(headers):
    worksheet.write(0, col, header)

for row, record in enumerate(data, start=1):
    for col, value in enumerate(record):
        worksheet.write(row, col, value)

# --- Create a line chart ---
chart = workbook.add_chart({'type': 'line'})

chart.add_series({
    'name': 'Revenue',
    'categories': ['Sales Data', 1, 0, 6, 0],  # Month column
    'values':     ['Sales Data', 1, 1, 6, 1],  # Revenue column
    'line': {'color': '#4472C4', 'width': 2.5},
})

chart.add_series({
    'name': 'Expenses',
    'categories': ['Sales Data', 1, 0, 6, 0],
    'values':     ['Sales Data', 1, 2, 6, 2],
    'line': {'color': '#ED7D31', 'width': 2.5},
})

chart.add_series({
    'name': 'Profit',
    'categories': ['Sales Data', 1, 0, 6, 0],
    'values':     ['Sales Data', 1, 3, 6, 3],
    'line': {'color': '#70AD47', 'width': 2.5},
})

chart.set_title({'name': 'Monthly Financial Overview'})
chart.set_x_axis({'name': 'Month'})
chart.set_y_axis({'name': 'Amount ($)'})
chart.set_size({'width': 500, 'height': 300})

worksheet.insert_chart('F2', chart)

workbook.close()
print("Excel file with chart saved!")