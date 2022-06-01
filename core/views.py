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

#     def form_valid(self, form):
#         form.instance.adress_id = self.kwargs.get('pk')
#         return super(CustomerCreateView, self).form_valid(form)

# class AdressCreateView(CreateView):
#     model = Adress
#     fields = '__all__'


def custom_customer(request):

    customer_form = CustCreatePersonalInfo(request.POST)
    customer_adress = CustCreateAdressForm(request.POST)

    if request.method == 'POST':

        if customer_form.is_valid() and customer_adress.is_valid():

            
            x = customer_form.save(commit=False)
            z = customer_adress.save(commit=False)
            x.adress = z
            z.save()
            x.save()
            
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
