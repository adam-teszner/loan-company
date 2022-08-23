import json
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.response import TemplateResponse
from django.views.generic import (CreateView, DetailView, ListView,
                                TemplateView, UpdateView)
from .models import Customer, Adress, UserInfo
from .forms import (CustCreatePersonalInfo, CustCreateAdressForm,
                    CustomSignUpForm, CustomWorkplaceForm,
                    AddNewProductForm, CustCreatePersonalInfoUpdate)
from django.views import View
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework.decorators import api_view


def index(request): 
  

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
    customer_adress = CustCreateAdressForm(request.POST, prefix='customer_adress')
    workplace_adr_form = CustCreateAdressForm(request.POST, prefix='workplace_adr_form')    #prefix dlatego bo jest adress 2 instatncje - workplace i zwykly !!
    workplace_form = CustomWorkplaceForm(request.POST)
    pesel_check = request.GET.get('pesel')
    

    if request.method == 'GET' and pesel_check:
        try:
            cust_obj = Customer.objects.get(social_security_no_pesel=pesel_check)
            customer_data = serializers.serialize('json', [cust_obj])
            customer_adr = serializers.serialize('json', [cust_obj.adress])
            workplace_data = serializers.serialize('json', [cust_obj.workplace])
            workplace_adress_data = serializers.serialize('json', [cust_obj.workplace.adress])
            customer_creator = UserInfo.objects.get(user=cust_obj.created_by.id)

            json_list = [customer_data, customer_adr, workplace_data, workplace_adress_data]
            data_2 = []
            for item in json_list:
                data_2.extend(json.loads(item))

            data_2.append({
                'creator_first_name' : customer_creator.first_name,
                'creator_last_name' : customer_creator.last_name
                })

            merged_json = json.dumps(data_2, indent=2)

            # print(merged_json)
            return HttpResponse(merged_json, content_type='application/json')

        except:
            print('BRAK')
            context = {
                'customer_form': customer_form,
                'customer_adress': customer_adress,
                'workplace_adr_form': workplace_adr_form,
                'workplace_form': workplace_form,
            }
            # return HttpResponse('Error')
            return render(request, 'core/custom_create.html', context) 
    
    
    if request.method == 'POST' and request.POST.get('customer_id_value') == '':


        if customer_form.is_valid() and customer_adress.is_valid() and workplace_adr_form.is_valid() and workplace_form.is_valid():

            
            x = customer_form.save(commit=False)
            z = customer_adress.save(commit=False)
            y = workplace_adr_form.save(commit=False)
            q = workplace_form.save(commit=False)
            
            x.created_by = request.user
            x.adress = z
            q.adress = y
            x.workplace = q

            z.save()            
            y.save()
            q.save()
            x.save()

            return redirect('customer_detail', pk=x.id)
            # teraz dziala, warto to PRINTOWAC !!!!  w request.post wychodzi:
            # with keyword arguments '{'kwargs': {'pk': 18}}' not found. 1 pattern(s) tried: ['my_customers_list/(?P<pk>[0-9]+)\\Z']
            # gdy bylo kwargs={'pk': x.id} to wyszlo to wyzej !

        else:
            context = {
                'customer_form': customer_form,
                'customer_adress': customer_adress,
                'workplace_adr_form': workplace_adr_form,
                'workplace_form': workplace_form,
            }


            return render(request, 'core/custom_create.html', context)

            
    elif request.method == 'POST' and request.POST.get('customer_id_value') != '':

        customer_id = request.POST.get('customer_id_value')
        customer_instance = Customer.objects.get(id=customer_id)

        cust_update = CustCreatePersonalInfoUpdate(request.POST, instance=customer_instance)
        cust_adress_update = CustCreateAdressForm(request.POST, prefix='customer_adress', instance=customer_instance.adress)
        workplace_adr_update = CustCreateAdressForm(request.POST, prefix='customer_adress', instance=customer_instance.workplace.adress)
        workplace_update = CustomWorkplaceForm(request.POST, instance=customer_instance.workplace)


        cust_update.save()
        cust_adress_update.save()
        workplace_adr_update.save()
        workplace_update.save()
        
        return redirect('customer_detail', pk=customer_id)   
    
    
    else:
        context = {
            'customer_form': customer_form,
            'customer_adress': customer_adress,
            'workplace_adr_form': workplace_adr_form,
            'workplace_form': workplace_form,
        }

        return render(request, 'core/custom_create.html', context)


        ### SKROCIC TO - ZROBIC LADNIEJSZE, EFEKTYWNE BARDZIEJ ###

    

    
class RegisterUser(View):
    user_info_form = CustomSignUpForm
    user_create_form = UserCreationForm
    template_name = 'core/sign_up.html'
    initial =   {'user_info_form': user_info_form,
                'user_create_form': user_create_form}

    def get(self, request):
        self.user_create_form(initial = self.initial)
        self.user_info_form(initial = self.initial)
        return render(request, self.template_name, self.initial)

    def post(self, request):
        
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
            

class CustomerListView(LoginRequiredMixin, ListView):

    paginate_by = 8

    def get_queryset(self):

        default_order = ['-created_date']
        order = self.request.GET.getlist('order_by', default_order)
        # print(self.request.GET)
        # print(order)
        return Customer.objects.filter(created_by=self.request.user.id).order_by(*order)

    
class CustomerDetailView(LoginRequiredMixin, DetailView):

    model = Customer
    template_name = 'core/customer_detail.html'



class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'core/customer_update.html'


    ### The same as model = Customer ###


    # def get_object(self):
        # self.object = Customer.objects.get(pk=self.kwargs['pk'])
        # print(self.object)
        # print('test')
        # return Customer.objects.get(pk=self.kwargs['pk'])

    # fields = field_choice['some']
    # initial = {'first_name' : Customer.objects.get(pk=self.kwargs['pk']).first_name}

    ### End ###
    
    basic_form = CustCreatePersonalInfoUpdate
    adress_form = CustCreateAdressForm
    workplace_form = CustomWorkplaceForm

    


    def get(self, request, pk):
        mode = self.request.GET.getlist('mode', default=None)
        object = Customer.objects.get(pk=self.kwargs['pk'])

        basic_form_inst = self.basic_form()
        adress_form_inst = self.adress_form()
        workplace_form_inst = self.workplace_form()
        
        # basic_initial = {}
        # for f in basic_form_inst.fields.keys():
        #     basic_initial[str(f)] = getattr(object, f)

        basic_initial = { str(f): getattr(object, f) for f in basic_form_inst.fields.keys() }
        adress_initial = { str(f): getattr(object.adress, f) for f in adress_form_inst.fields.keys() }
        workplace_initial = { str(f): getattr(object.workplace, f) for f in workplace_form_inst.fields.keys() }
        workplace_adress_initial = { str(f): getattr(object.workplace.adress, f) for f in adress_form_inst.fields.keys() }

        context_var = {
            'basic': { 
                'basic' : self.basic_form(initial=basic_initial) },
            'contact' : {
                'adress' : self.adress_form(initial=adress_initial),
                'form': self.basic_form(initial=basic_initial),
                },
            'workplace' : {
                'form': self.basic_form(initial=basic_initial)
                }
    }
        

        if mode[0] == 'basic' and len(mode) == 1:
            print('jeden')
            print(object)

            # print(obj)
            
            return render(request, self.template_name, context=context_var['basic'])
        elif mode[0] == 'contact' and len(mode) == 1:
            print('dwa')
            print(mode)
            print(request.GET)
            # return render(request, self.template_name, context=context_var['contact'])
            print(context_var)
            print(basic_initial)
            return HttpResponse(context_var['basic'], content_type='application/text')

        elif mode[0] == 'workplace' and len(mode) == 1:
            print('cztery')
            print(mode)
            print(request.GET)
            return render(request, self.template_name)
        
        else: 
            print('TRZY else wyszlo')
            print(request.GET)
            return render(request, self.template_name)




    def post(self, request, pk):
        object = Customer.objects.get(pk=self.kwargs['pk'])
        basic_form_post = self.basic_form(request.POST, instance=object)
        adress_form_post = self.adress_form(request.POST, instance=object.adress)
        workplace_form_post = self.workplace_form(request.POST, instance=object.workplace)
        workplace_adress_form_post = self.adress_form(request.POST, instance=object.workplace.adress)
        if basic_form_post.is_valid():
            basic_form_post.save()
            
        if adress_form_post.is_valid():
            adress_form_post.save()
        
        if workplace_form_post.is_valid():
            workplace_form_post.save()

        if workplace_adress_form_post.is_valid():
            workplace_adress_form_post.save()

        return HttpResponseRedirect(reverse('customer_detail', kwargs={'pk':pk}))
        # return redirect('customer_detail', pk=pk)




class AddNewProductView(LoginRequiredMixin, View):

    add_product_form = AddNewProductForm
    template_name = 'core/add_product.html'
    initial = {'add_product': add_product_form }

    def get(self, request, id):    
        self.add_product_form(initial=self.initial)
        return render(request, self.template_name, self.initial)

    def post(self, request, id):
        customer_instance = Customer.objects.get(id=id)
        add_prod = self.add_product_form(request.POST)
        if add_prod.is_valid():
            s = add_prod.save(commit=False)
            s.owner = customer_instance
            s.save()
            return redirect('customer_detail', pk=id)
        else:
            return render(request, self.template_name, self.initial)

class jsonTestView(View):
    def get(self, request):

        pesel = 21241411111     


        cust_obj = Customer.objects.get(social_security_no_pesel=pesel)

        customer_data = serializers.serialize('json', {cust_obj})
        customer_adress = serializers.serialize('json', [cust_obj.adress])
        workplace_data = serializers.serialize('json', [cust_obj.workplace])
        workplace_adress_data = serializers.serialize('json', [cust_obj.workplace.adress])

        json_list = [customer_data, customer_adress, workplace_data, workplace_adress_data]
        data_2 = []
        for item in json_list:
            data_2.extend(json.loads(item))

        merged_json = json.dumps(data_2, indent=2)

        context = {

            'customer' : merged_json
        }

        # return render(request, 'core/test.html', context=context)
        # return JsonResponse(context, safe=False, json_dumps_params={'indent':'    '})
        return HttpResponse(merged_json, content_type='application/json')
    

class restApi(View):

    def get(self, *args, **kwargs):

        print(self.request.GET)
        print(self.request.POST)

        body = self.request.body  # byte string of json data
        data = {}

        try:
            data = json.loads(body) # string of Json data > python dict
        except:
            pass
        print(data)

        data['params'] = dict(self.request.GET)
        data['headers'] = dict(self.request.headers)
        data['content_type'] = self.request.content_type

        return JsonResponse(data)


@api_view(['GET'])
def api_home(request, *args, **kwargs):

    '''
    DRF api view
    '''
    model_data = Customer.objects.all().order_by('?').first() # random ordering, first item only
    data = {}

    data = model_to_dict(model_data, fields = ['first_name', 'last_name', 'dob', 'adress'])
    return Response(data)
