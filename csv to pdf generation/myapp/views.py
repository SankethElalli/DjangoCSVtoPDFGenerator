from django.shortcuts import render
from django.http import HttpResponse
import csv
from django.http import HttpResponse
from .models import Person
from reportlab.pdfgen import canvas
from django.shortcuts import render, redirect
from django.shortcuts import render

def index(request):
    return render(request, 'myapp/index.html')

def generate_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="persons.pdf"'

    persons = Person.objects.all()

    c = canvas.Canvas(response)
    c.drawString(100, 800, "Persons List")
    y = 750
    for person in persons:
        c.drawString(100, y, f"Name: {person.first_name} {person.last_name}, Email: {person.email}")
        y -= 20
    
    c.save()
    return response


def import_persons_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            return HttpResponse('File is not a CSV')

        # Assuming your CSV file has headers like 'first_name', 'last_name', 'email'
        decoded_file = csv_file.read().decode('utf-8')
        csv_data = csv.reader(decoded_file.splitlines(), delimiter=',')

        # Assuming the first row is header and the remaining are data rows
        header = next(csv_data)
        for row in csv_data:
            # Assuming Person model has fields 'first_name', 'last_name', 'email'
            _, created = Person.objects.update_or_create(
                first_name=row[0],
                last_name=row[1],
                email=row[2]
            )

        # Render success template with a link to generate PDF
        return render(request, 'import-success.html')

    return render(request, 'import_csv.html')  # Assuming import_csv.html is your import form
    return redirect('index')
