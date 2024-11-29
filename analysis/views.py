from django.shortcuts import render, redirect, get_object_or_404
from .forms import BloodAnalysisForm
from .models import BloodAnalysis
from .utils import process_image  # Оцифровка изображения, создадим позже
import csv
import os

def upload_image(request):
    if request.method == 'POST':
        form = BloodAnalysisForm(request.POST, request.FILES)
        if form.is_valid():
            analysis = form.save()
            analysis.result = process_image(analysis.image.path)
            analysis.save()
            save_to_csv(analysis.upload_id, analysis.result)
            return redirect('result', pk=analysis.pk)
    else:
        form = BloodAnalysisForm()
    return render(request, 'analysis/upload.html', {'form': form})

def result(request, pk):
    analysis = get_object_or_404(BloodAnalysis, pk=pk)
    return render(request, 'analysis/result.html', {'analysis': analysis})

def save_to_csv(upload_id, result):
    # Путь к папке, где будет храниться CSV файл
    results_dir = os.path.join('results')  # Папка для результатов
       
    # Путь к CSV файлу
    csv_file_path = os.path.join(results_dir, 'results.csv')
    
    # Открываем CSV файл в режиме добавления (append)
    with open(csv_file_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Проверяем, есть ли уже заголовки в файле, если нет, добавляем их
        if csvfile.tell() == 0:
            writer.writerow(['Upload ID', 'Result'])  # Заголовки столбцов

        # Записываем данные (upload_id и результат)
        writer.writerow([upload_id, result])