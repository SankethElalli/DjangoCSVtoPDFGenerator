from django.urls import path
from . import views

urlpatterns = [
    path('import-csv/', views.import_persons_csv, name='import_csv'),
    path('import-success/', views.import_persons_csv, name='import_success'),  # Adjust the URL as per your preference
    path('generate-pdf/', views.generate_pdf, name='generate_pdf'),
]
