from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import UploadedFile
import os
import subprocess

def file_list(request):
    files = UploadedFile.objects.all().order_by('-uploaded_at')
    return render(request, 'file_list.html', {'files': files})

def file_upload(request):
    if request.method == 'POST':
        file = request.FILES['file']
        uploaded = UploadedFile.objects.create(file=file, filename=file.name)
        return redirect('file_list')
    return render(request, 'file_upload.html')

def file_detail(request, file_id):
    file = get_object_or_404(UploadedFile, id=file_id)
    return render(request, 'file_detail.html', {'file': file})

# def convert_to_pdf(request, file_id):
#     file = get_object_or_404(UploadedFile, id=file_id)
#     input_path = file.file.path
#     output_dir = os.path.join(settings.MEDIA_ROOT, 'converted')
#     os.makedirs(output_dir, exist_ok=True)

#     # Run LibreOffice conversion
#     subprocess.run([
#         'libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', output_dir, input_path
#     ])

#     converted_file_name = os.path.splitext(os.path.basename(input_path))[0] + '.pdf'
#     converted_path = os.path.join(output_dir, converted_file_name)

#     context = {
#         'original_name': file.filename,
#         'converted_url': settings.MEDIA_URL + 'converted/' + converted_file_name
#     }
#     return render(request, 'convert_result.html', context)


def convert_to_pdf(request, file_id):
    file = get_object_or_404(UploadedFile, id=file_id)
    input_path = file.file.path
    output_dir = os.path.join(settings.MEDIA_ROOT, "converted")
    os.makedirs(output_dir, exist_ok=True)

    # Convert using LibreOffice
    try:
        subprocess.run([
            r"C:\Program Files\LibreOffice\program\soffice.exe",
            "--headless", "--convert-to", "pdf",
            "--outdir", output_dir, input_path
        ], check=True)
    except subprocess.CalledProcessError:
        return render(request, "convert_result.html", {
            "original_name": file.filename,
            "converted_url": None,
            "error": "Conversion failed. Please check LibreOffice installation."
        })

    # Get converted file name
    converted_name = os.path.splitext(os.path.basename(input_path))[0] + ".pdf"
    converted_path = os.path.join(output_dir, converted_name)
    converted_url = settings.MEDIA_URL + "converted/" + converted_name

    return render(request, "convert_result.html", {
        "original_name": file.filename,
        "converted_url": converted_url,
        "error": None,
    })