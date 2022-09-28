import csv
import xlwt
from django.http import HttpResponse
import datetime

# from django.template.loader import render_to_string
# from weasyprint import HTML
# import tempfile
from django.db.models import Sum
# CREATE A URL BUTTON THAT LINKS TO THE VIEW
def export_csv(request):
  
  response = HttpResponse(content_type='text/csv')
  response['Content-Disposition'] = 'attachment; filename=Name.csv'
  
  writer = csv.writer(response)
  writer.writerow(['headers', 'values'])
  
  queryset = ''
  for items in queryset:
    writer.writerow(['item1', 'item2'])
  
  return response


def export_excel(request):
# pip install xlwt
  response = HttpResponse(content_type='application/ms-excel')
  response['Content-Disposition'] = 'attachment; filename=Name.xls' + str(datetime.datetime.now())+'.xls'
  wb = xlwt.Workbook(encoding='utf-8')
  ws = wb.add_sheet('Expense')
  row_num = 0
  font_style = xlwt.XFStyle()
  font_style.font.bold = True
  
  columns = ['headers', 'values']
  for col_num in range(len(columns)):
    ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
  
  queryset = ''
  for row in queryset:
    row_num+=1
    
    for col_num in range(len(row)):
      ws.write(row_num, col_num, str(row[col_num]), font_style)
      
  wb.save(response)
  
  return response


# def export_pdf(request):
# # pip install weasyprint
#   response = HttpResponse(content_type='application/pdf')
#   response['Content-Disposition'] = 'inline; attachment; filename=Name.xls' + str(datetime.datetime.now())+'.pdf' # INLINE IS ADDED SO AS NOT TO DOWNLOAD IT DIRECTLY
#   response['Content-Transfer-Encoding'] = 'binary'
  
#   queryset = ""
#   sum = queryset.aggregate(Sum('amount')) #AMOUNT IS THE FIELD IN THE QUERYSET
  
#   html_string = render_to_string('expenses/pdf-output.html', {'expenses': queryset, 'total': sum{'amount_sum'}})
#   html = HTML(string=html_string)
  
#   result = html.write_pdf()
  
#   with tempfile.NamedTemporaryFile(delete=True) as output:
#     output.write(result)
#     output.flush()
    
#     output = open(output.name, 'rb')
#     response.write(output.read())
    
#   return response


