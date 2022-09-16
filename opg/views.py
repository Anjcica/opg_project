from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.template import loader
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Opg, Product
from .forms import OpgForm, ProductForm
from user.forms import UserCreationForm
from django.forms import inlineformset_factory


def index(request):
    if request.user.is_authenticated and not(request.user.is_admin):
        return redirect('profile')
    context = {}
    template = loader.get_template('opg/index.html')
    return HttpResponse(template.render(context, request))


def register(request):
    user_form = UserCreationForm()
    opg_form = OpgForm()
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        opg_form = OpgForm(request.POST)
        if user_form.is_valid() and opg_form.is_valid():
            user = user_form.save(commit=False)
            opg = opg_form.save(commit=False)

            # Checking if OPG with same name, but different letter case already exist in database
            for name in Opg.objects.all().values_list("name"):
                print(name)
                if opg.name.upper() == name[0].upper():
                    messages.error(request, "Already exist OPG with same name ")
                    return redirect('register')

            opg.user = user
            user.save()
            opg.save()
            login(request, user)
            return redirect('/add_product')
        else:
            for user_error in list(user_form.errors.values()):
                messages.error(request, user_error)
            for opg_error in list(opg_form.errors.values()):
                messages.error(request, opg_error)

    context = {
        'user_form': user_form,
        'opg_form': opg_form,
    }
    template = loader.get_template('opg/register.html')
    return HttpResponse(template.render(context, request))


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
    ProductFormSet = inlineformset_factory(Opg, Product, fields=('name', 'category', 'opg'), extra=7, can_delete=False)
    formset = ProductFormSet(queryset=Product.objects.none(), instance=opg)
    if request.method == 'POST':
        formset = ProductFormSet(request.POST, instance=opg)
        if formset.is_valid:
            try:
                formset.save()
            except ValueError as e:
                messages.error(request, e)
                return redirect('add_product')
            return redirect('product_list')
        else:
            for error in formset.errors:
                messages.error(request, error)

    context = {
        'formset': formset,
    }
    template = loader.get_template('opg/add_product.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url='login')
def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
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
            return redirect('product_list')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
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
            for error in list(opg_form.errors.values()):
                messages.error(request, error)

    context = {
        'opg_form': opg_form,
    }
    template = loader.get_template('opg/edit_profile.html')
    return HttpResponse(template.render(context, request))
