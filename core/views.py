from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.views.generic import CreateView, DetailView
from .models import Customer, Adress
from .forms import CustCreatePersonalInfo, CustCreateAdressForm

# Create your views here.


def index(request):
    return render(request, 'base.html')

def create_customer(request):
    return render(request, 'core/create_customer.html')

class CustomerCreateView(CreateView):
    model = Customer
    fields = '__all__'


def custom_customer(request):

    customer_form = CustCreatePersonalInfo(request.POST)
    customer_adress = CustCreateAdressForm(request.POST)

    if request.method == 'POST':



        if customer_form.is_valid() and customer_adress.is_valid():

            customer_form.save()
            customer_adress.save()
            return HttpResponseRedirect(reverse('index'))

        else:
            context = {
                'customer_form': customer_form,
                'customer_adress': customer_adress,
            }
    else:
        # return render(request, 'core/custom_create.html')
        context = {
            'customer_form': customer_form,
            'customer_adress': customer_adress,
        }
        return render(request, 'core/custom_create.html', context)

# def custom_customer(request):

#     customer_form = CustCreatePersonalInfo(request.POST)
#     customer_adress = CustCreateAdressForm(request.POST)
#     context = {
#             'customer_form': customer_form,
#             'customer_adress': customer_adress,
#         }
#     return render(request, 'core/custom_create.html', context)