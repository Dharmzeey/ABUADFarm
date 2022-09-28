import os
import datetime
import xlwt
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


def link_callback(uri, rel):
  """
  Convert HTML URIs to absolute system paths so xhtml2pdf can access those
  resources
  """
  result = finders.find(uri)
  if result:
    if not isinstance(result, (list, tuple)):
      result = [result]
    result = list(os.path.realpath(path) for path in result)
    path=result[0]
  else:
    sUrl = settings.STATIC_URL        # Typically /static/
    sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL         # Typically /media/
    mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

    if uri.startswith(mUrl):
      path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
      path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
      return uri

  # make sure that file exists
  if not os.path.isfile(path):
    raise Exception(
      'media URI must start with %s or %s' % (sUrl, mUrl)
    )
  return path

def render_to_pdf(template_src, context_dict={}):
    template_path = template_src
    context = context_dict
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
      html, dest=response, link_callback=link_callback)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

#Opens up page as PDF
def view_pdf(request, data, *args, **kwargs):
  pdf = render_to_pdf(kwargs['template_name'], data)
  return HttpResponse(pdf, content_type='application/pdf')

# AUTOMATICALLY DOWNLOADS PDF
def download_pdf(request, data, *args, **kwargs):
  pdf = render_to_pdf(kwargs['template_name'], data)
  response = HttpResponse(pdf, content_type='application/pdf')
  filename = "Invoice_%s.pdf" %("12341231")
  content = 'attachment; filename="report.pdf"'
  response['Content-Disposition'] = content
  return response


# EXCEL
# EXCEL
def export_excel(request, data):
  # pip install xlwt
  response = HttpResponse(content_type='application/ms-excel')
  response['Content-Disposition'] = 'attachment; filename=Report' + str(datetime.datetime.now())+'.xls'
  wb = xlwt.Workbook(encoding='utf-8')
  ws = wb.add_sheet('Purchase')
  row_num = 0
  font_style = xlwt.XFStyle()
  font_style.font.bold = True
  
  # THE IF 'ADMIN_FLAG' CHECK IF THE VIEW ACCESSING THE XLWT IS FROM USER OR ADMIN, SO IT CAN KNOW WHEN TO INCLUDE 'CUSTOMER' COLUMN OR NOT
  if 'admin_flag' in data.keys():
    columns = ['CUSTOMER','DATE', 'ITEM', 'QUANTITY(kG)', 'PRICE(₦)']
  else:
    columns = ['DATE', 'ITEM', 'QUANTITY(kG)', 'PRICE(₦)']
  for col_num in range(len(columns)):
    ws.write(row_num, col_num, columns[col_num], font_style)
  
  queryset = data['goods']
  total = 0
  if 'admin_flag' in data.keys():
    for row in queryset:
      row_num+=1
      ws.write(row_num, 0, str(row.owner))
      ws.write(row_num, 1, str(row.date_ordered).split(" ")[0])
      ws.write(row_num, 2, str(row.item))
      ws.write(row_num, 3, row.quantity)
      ws.write(row_num, 4, row.price)
      total += row.price
    # THIS BELOW WRITES THE TOTAL AFTER THE WHOLE LOOP
    ws.write(len(queryset) + 1, 0, "TOTAL", font_style)
    ws.write(len(queryset) + 1, 4, total, font_style)
  else:
    for row in queryset:
      row_num+=1
      
      ws.write(row_num, 0, str(row.date_ordered).split(" ")[0])
      ws.write(row_num, 1, str(row.item))
      ws.write(row_num, 2, row.quantity)
      ws.write(row_num, 3, row.price)
      total += row.price
    # THIS BELOW WRITES THE TOTAL AFTER THE WHOLE LOOP
    ws.write(len(queryset) + 1, 0, "TOTAL", font_style)
    ws.write(len(queryset) + 1, 3, total, font_style)

  wb.save(response)
  
  return response
