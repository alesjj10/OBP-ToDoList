from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from .models import Task, Tag
from .forms import TaskForm

@login_required

def task_list(request):
    tasks = Task.objects.filter(user=request.user)

    status = request.GET.get('status')
    priority = request.GET.get('priority')
    tag = request.GET.get('tag')


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

    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'form': form,
        'tags': Tag.objects.filter(user=request.user)
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