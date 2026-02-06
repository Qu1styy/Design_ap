from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, DesignRequestForm
from .models import DesignRequest

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'main/register.html', {'form': form})

def index(request):
    return render(request, 'main/index.html')

@login_required
def profile(request):
    return render(request, 'main/profile.html')

@login_required
def create_design_request(request):
    if request.method == 'POST':
        form = DesignRequestForm(request.POST, request.FILES)
        if form.is_valid():
            design_request = form.save(commit=False)
            design_request.user = request.user
            # статус "Новая" ставится автоматически
            design_request.save()
            return redirect('profile')  # возвращаем в профиль
    else:
        form = DesignRequestForm()

    return render(request, 'main/create.html', {'form': form})

@login_required
def my_requests(request):
    requests = DesignRequest.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(request, 'main/my_requests.html', {
        'requests': requests
    })

@login_required
def delete_design_request(request, request_id):
    design_request = get_object_or_404(
        DesignRequest,
        id=request_id,
        user=request.user
    )

    if request.method == 'POST':
        design_request.delete()
        return redirect('my_requests')

    return render(
        request,
        'main/delete_request.html',
        {'request_obj': design_request}
    )