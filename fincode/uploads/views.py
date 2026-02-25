from django.shortcuts import render, redirect
from .forms import FinancialUploadForm

def upload_financials(request):
    if request.method == 'POST':
        form = FinancialUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'uploads/success.html')
    else:
        form = FinancialUploadForm()

    return render(request, 'uploads/upload.html', {'form': form})
