from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Product
from .forms import OpgForm, ProductForm, CreateUserForm


def index(request):
    if request.user.is_authenticated and not(request.user.is_superuser):
        return redirect('profile')
    context = {}
    template = loader.get_template('opg/index.html')
    return HttpResponse(template.render(context, request))


def register(request):
    user_form = CreateUserForm()
    opg_form = OpgForm()
    if request.method == 'POST':
        user_form = CreateUserForm(request.POST)
        opg_form = OpgForm(request.POST)
        if user_form.is_valid() and opg_form.is_valid():
            user = user_form.save(commit=False)
            opg = opg_form.save(commit=False)
            opg.user = user
            user.save()
            opg.save()
            login(request, user)
            return redirect('/add_product')
        else:
            messages.warning(request, 'Došlo je do pogreške')

    context = {
        'user_form': user_form,
        'opg_form': opg_form,
    }
    template = loader.get_template('opg/register.html')
    return HttpResponse(template.render(context, request))


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.info(request, 'Ime ili lozinka pogrešni')
    context = {}
    template = loader.get_template('opg/login.html')
    return HttpResponse(template.render(context, request))


def user_logout(request):
    logout(request)
    return redirect('/')


@login_required(login_url='login')
def product_list(request):
    products = request.user.opg.product_set.all()
    context = {
        'products': products,
    }
    template = loader.get_template('opg/product_list.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url='login')
def add_product(request):
    opg = request.user.opg
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.opg = opg
            product.save()
            messages.info(request, 'Proizvod dodan')
            return redirect('product_list')
        else:
            messages.warning(request, 'Došlo je do pogreške')
    context = {
        'form': form,
    }
    template = loader.get_template('opg/add_product.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url='login')
def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
        messages.info(request, 'Proizvod obrisan')
        return redirect('product_list')
    context = {
        'product': product
    }
    template = loader.get_template('opg/delete_product.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url='login')
def product(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.info(request, 'Proizvod editiran')
            return redirect('product_list')
        else:
            messages.warning(request, 'Došlo je do pogreške')
    context = {
        'form': form,
    }
    template = loader.get_template('opg/product.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url='login')
def profile(request):
    context = {
        'opg': request.user.opg,
    }
    template = loader.get_template('opg/profile.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url='login')
def edit_profile(request):
    opg = request.user.opg
    user = request.user
    opg_form = OpgForm(instance=opg)

    if request.method == 'POST':
        opg_form = OpgForm(request.POST, instance=opg)
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        if opg_form.is_valid():
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            opg_form.save()
            login(request, user)
            return redirect('/')
        else:
            messages.warning(request, 'Došlo je do pogreške')

    context = {
        'opg_form': opg_form,
    }
    template = loader.get_template('opg/edit_profile.html')
    return HttpResponse(template.render(context, request))
