from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.shortcuts import redirect
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from .models import Task, Tag
from .forms import TaskForm
from collections import defaultdict
import calendar
from datetime import date

@login_required

def task_list(request):
    tasks = Task.objects.filter(user=request.user)

    view_type = request.GET.get('view', 'list')

    status = request.GET.get('status')
    priority = request.GET.get('priority')
    tag = request.GET.get('tag')
    calendar_tasks = defaultdict(list)
    tasks_no_date = []

    today = date.today()
    year = today.year
    month = today.month

    cal = calendar.monthcalendar(year, month)


    if status:
        tasks = tasks.filter(status=status)

    if priority:
        tasks = tasks.filter(priority=priority)

    if tag:
        tasks = tasks.filter(tags__id=tag)

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # důležité!
            task.save()
            form.save_m2m()
            return redirect('task_list')
    else:
        form = TaskForm()


    for task in tasks:
        if task.due_date:
            task_date = task.due_date.date()
            calendar_tasks[task_date].append(task)
        else:
            tasks_no_date.append(task)


    tasks_by_day = {day: [] for week in cal for day in week if day != 0}

    for task in tasks:
        if task.due_date:
            if task.due_date.year == year and task.due_date.month == month:
                tasks_by_day[task.due_date.day].append(task)


    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'form': form,
        'tags': Tag.objects.filter(user=request.user),
        'calendar_tasks': dict(calendar_tasks),
        'tasks_no_date': tasks_no_date, 
        'view_type': view_type,
        'calendar': cal,
        'tasks_by_day': tasks_by_day,
        'month': month,
        'year': year,
        'today_day': today.day,
    })


def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/task_form.html', {'form': form})

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('task_list')

def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.status = 'DOKONCENO'
    task.save()
    return redirect('task_list')

def stats(request):
    tasks = Task.objects.filter(user=request.user)

    total = tasks.count()
    completed = tasks.filter(status='DOKONCENO').count()
    in_progress = tasks.filter(status='ROZPRACOVANO').count()
    todo = tasks.filter(status='ZADANO').count()

    priority_counts = [0, 0, 0, 0, 0]

    for task in tasks:
        priority_counts[task.priority - 1] += 1

    return render(request, 'tasks/stats.html', {
        'total': total,
        'completed': completed,
        'in_progress': in_progress,
        'todo': todo,
        'priority_counts': priority_counts,
    })

@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            form.save_m2m()
            return redirect('task_list')
    else:
        form = TaskForm()

    return render(request, 'tasks/add_task.html', {'form': form})

