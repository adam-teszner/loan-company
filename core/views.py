from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.views.generic import CreateView, DetailView
from .models import Customer, Adress, UserInfo
from .forms import (CustCreatePersonalInfo, CustCreateAdressForm,
                    CustomSignUpForm)
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

# def include_user_info(request):
#     user_id = request.user.id
#     user_name = UserInfo.objects.get(user=user_id)
#     context = {
#         'user_name': user_name,
#         'test_field': 'Tralalala'
#     }

#     return render(request, 'registration/login_usr_info.html', context=context)

# Wrocic do INCLUDE TEMPLATE - ale w tym przypadku zbędne

def index(request): 
  
    # try:
    #     user_id = request.user.id
    #     user_name = UserInfo.objects.get(user=user_id)
    #     context = {
    #         'user_name': user_name.first_name
    #     }
    # except:
    #     context = {
    #         'user_name': request.user.username
    #     }

    # Jest zrobione jako custom_simple_template_tag

    return render(request, 'base.html')

@login_required
def create_customer(request):
    return render(request, 'core/create_customer.html')

class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    fields = '__all__'

#     def form_valid(self, form):
#         form.instance.adress_id = self.kwargs.get('pk')
#         return super(CustomerCreateView, self).form_valid(form)

# class AdressCreateView(CreateView):
#     model = Adress
#     fields = '__all__'

@login_required
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


class RegisterUser(View):
    user_info_form = CustomSignUpForm
    user_create_form = UserCreationForm
    template_name = 'core/sign_up.html'
    initial =   {'user_info_form': user_info_form,
                'user_create_form': user_create_form}

    def get(self, request, *args, **kwargs):
        self.user_create_form(initial = self.initial)
        self.user_info_form(initial = self.initial)
        return render(request, self.template_name, self.initial)

    def post(self, request, *args, **kwargs):
        
        user_info = self.user_info_form(request.POST)
        user_create = self.user_create_form(request.POST)
        if user_info.is_valid() and user_create.is_valid():
            z = user_info.save(commit=False)
            x = user_create.save(commit=False)
            z.user = x
            x.save()
            z.save()

            # WYMYSLIC KROTSZA WERSJĘ !!! !! z comitem itd 

            return HttpResponseRedirect(reverse('index'))

        return render(request, self.template_name, self.initial)
            