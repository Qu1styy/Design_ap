from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import RegisterForm, DesignRequestForm, CategoryForm
from .models import DesignRequest, Category, DesignRequest
from django.contrib import messages



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
            return redirect('my_requests')  # возвращаем в профиль
    else:
        form = DesignRequestForm()

    return render(request, 'main/create.html', {'form': form})

@login_required
def my_requests(request):
    # Получаем параметр фильтра из GET-запроса, например ?status=new
    status_filter = request.GET.get('status')

    requests = DesignRequest.objects.filter(user=request.user)

    if status_filter:
        requests = requests.filter(status=status_filter)

    return render(request, 'main/my_requests.html', {'requests': requests, 'status_filter': status_filter})

@login_required
def delete_design_request(request, request_id):
    design_request = get_object_or_404(DesignRequest, id=request_id, user=request.user)

    if design_request.status != 'new':
        messages.error(request, "Эту заявку нельзя удалить, она уже в работе или выполнена.")
        return redirect('my_requests')

    if request.method == 'POST':
        design_request.delete()
        messages.success(request, "Заявка успешно удалена!")
        return redirect('my_requests')

    return render(request, 'main/delete_request.html', {'request_obj': design_request})

@login_required
def delete_request(request, pk):
    design_request = get_object_or_404(DesignRequest, pk=pk)

    # Проверяем: заявку может удалить только владелец и только если статус "Новая"
    if design_request.user != request.user:
        messages.error(request, "Вы не можете удалить чужую заявку.")
        return redirect('my_requests')

    if design_request.status != 'new':
        messages.error(request, "Вы не можете удалить заявку, которая уже в работе или выполнена.")
        return redirect('my_requests')

    if request.method == 'POST':
        design_request.delete()
        messages.success(request, "Заявка успешно удалена!")
        return redirect('my_requests')

    return render(request, 'main/confirm_delete.html', {'design_request': design_request})

def index(request):
    latest_done_requests = DesignRequest.objects.filter(
        status=DesignRequest.Status.DONE
    ).order_by('-created_at')[:4]

    in_progress_count = DesignRequest.objects.filter(
        status=DesignRequest.Status.IN_PROGRESS
    ).count()

    return render(request, 'main/index.html', {
        'latest_done_requests': latest_done_requests,
        'in_progress_count': in_progress_count
    })

def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def admin_panel(request):
    return render(request, 'main/admin_panel.html')

def filter_status(request):
    return render(request, 'main/filter_status.html')

def categories_list(request):
    return render(request, 'main/categories_list.html')

def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def categories_list(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories_list')
    else:
        form = CategoryForm()

    return render(request, 'main/categories_list.html', {
        'categories': categories,
        'form': form
    })

@login_required
@user_passes_test(is_admin)
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        category.delete()  # заявки удалятся автоматически
        return redirect('categories_list')

    return render(request, 'main/delete_category.html', {
        'category': category
    })
