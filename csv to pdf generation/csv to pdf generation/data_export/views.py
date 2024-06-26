from django.shortcuts import render
from django.http import HttpResponse
import csv
import io
from reportlab.pdfgen import canvas
from .forms import UploadFileForm

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            # Read CSV file
            decoded_file = file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.reader(io_string, delimiter=',', quotechar='"')
            # Generate PDF
            buffer = io.BytesIO()
            p = canvas.Canvas(buffer)
            y = 800
            for row in reader:
                text = ', '.join(row)
                p.drawString(100, y, text)
                y -= 20
            p.showPage()
            p.save()
            buffer.seek(0)
            return HttpResponse(buffer, content_type='application/pdf')
    else:
        form = UploadFileForm()
    return render(request, 'data_export/upload.html', {'form': form})
