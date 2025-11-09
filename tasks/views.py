from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Task


def login_view(request):
    """Handle user login."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")

    form = AuthenticationForm()
    return render(request, 'tasks/login.html', {'form': form})


def logout_view(request):
    """Handle user logout."""
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    """
    Display user's tasks with add, complete, and delete functionality.
    Includes pagination with ITEMS_PER_PAGE = 5.
    """
    ITEMS_PER_PAGE = 5

    # Handle task actions
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add':
            title = request.POST.get('title', '').strip()
            if title:
                Task.objects.create(user=request.user, title=title)
                messages.success(request, 'Task added successfully!')
            return redirect('dashboard')

        elif action == 'complete':
            task_id = request.POST.get('task_id')
            try:
                task = Task.objects.get(id=task_id, user=request.user)
                task.completed = True
                task.save()
                messages.success(request, 'Task marked as completed!')
            except Task.DoesNotExist:
                messages.error(request, 'Task not found.')
            return redirect('dashboard')

        elif action == 'delete':
            task_id = request.POST.get('task_id')
            try:
                task = Task.objects.get(id=task_id, user=request.user)
                task.delete()
                messages.success(request, 'Task deleted successfully!')
            except Task.DoesNotExist:
                messages.error(request, 'Task not found.')
            return redirect('dashboard')

    # Get tasks only for the logged-in user
    tasks = Task.objects.filter(user=request.user).order_by('-id')

    # Use Django Paginator
    page_number = request.GET.get('page', 1)
    paginator = Paginator(tasks, ITEMS_PER_PAGE)
    # automatically handles invalid page numbers
    page_obj = paginator.get_page(page_number)

    context = {
        'tasks': page_obj.object_list,
        'page_obj': page_obj,
        'username': request.user.username,
    }

    return render(request, 'tasks/dashboard.html', context)
