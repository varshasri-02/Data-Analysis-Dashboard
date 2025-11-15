import pandas as pd
from django.shortcuts import render
from .forms import UploadFileForm
from django.core.files.storage import FileSystemStorage

def handle_uploaded_file(file):
    fs = FileSystemStorage()
    filename = fs.save(file.name, file)
    return fs.path(filename)

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_path = handle_uploaded_file(request.FILES['file'])
            df = pd.read_csv(file_path)
            summary_stats = df.describe().to_html()
            head = df.head().to_html()

            # Handling missing values
            missing_values = df.isnull().sum().to_frame().T.to_html()

            # Generate visualizations
            import matplotlib.pyplot as plt
            import seaborn as sns
            import os
            from io import BytesIO
            import base64

            plt.figure()
            sns.histplot(df.select_dtypes(include=['number']).dropna(), kde=True)
            hist_path = os.path.join('analysis', 'static', 'hist.png')
            plt.savefig(hist_path)
            plt.close()

            context = {
                'form': form,
                'summary_stats': summary_stats,
                'head': head,
                'missing_values': missing_values,
                'hist_path': hist_path,
            }
            return render(request, 'analysis/result.html', context)
    else:
        form = UploadFileForm()
    return render(request, 'analysis/upload.html', {'form': form})
