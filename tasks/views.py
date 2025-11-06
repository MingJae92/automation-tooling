from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
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
    
    # Handle task creation
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
                task = Task.objects.get(id=task_id)
                task.completed = True
                task.save()
                messages.success(request, 'Task marked as completed!')
            except Task.DoesNotExist:
                messages.error(request, 'Task not found.')
            return redirect('dashboard')
        
        elif action == 'delete':
            task_id = request.POST.get('task_id')
            try:
                task = Task.objects.get(id=task_id)
                task.delete()
                messages.success(request, 'Task deleted successfully!')
            except Task.DoesNotExist:
                messages.error(request, 'Task not found.')
            return redirect('dashboard')
    
    tasks = Task.objects.all()

    # Get page number from query params (default to 0)
    try:
        page = int(request.GET.get('page', 0))
        if page < 0:
            page = 0
    except ValueError:
        page = 0
    
    start = page * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE

    if page == 0:
        paginated_tasks = tasks[start:end]
    else:
        start = (page + 1) * ITEMS_PER_PAGE
        end = start + ITEMS_PER_PAGE
        paginated_tasks = tasks[start:end]

    total_tasks = tasks.count()
    total_pages = (total_tasks + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
    
    context = {
        'tasks': paginated_tasks,
        'current_page': page,
        'total_pages': total_pages,
        'has_next': page < total_pages - 1,
        'has_prev': page > 0,
        'username': request.user.username,
    }
    
    return render(request, 'tasks/dashboard.html', context)
