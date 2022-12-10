import json
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.response import TemplateResponse
from django.views.generic import (CreateView, DetailView, ListView,
                                TemplateView, UpdateView,)
from django.views.generic.edit import BaseUpdateView
from .models import Customer, Adress, UserInfo
from .forms import (CustCreatePersonalInfo, CustCreateAdressForm,
                    CustomSignUpForm, CustomWorkplaceForm,
                    AddNewProductForm, CustCreatePersonalInfoUpdate,
                    ChangeUsername, CustomLogin, CustomPasswordResetFrorm,
                    CustomSetPasswordForm, CustomPasswordChangeForm, 
                    CustomUserCreationForm)
from django.views import View
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import (PasswordChangeView,
                                PasswordChangeDoneView, PasswordResetView,
                                PasswordResetDoneView, PasswordResetConfirmView,
                                LoginView)                                                                    
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

'''
### Trying Inline Formset ###
from django.forms.models import inlineformset_factory

UserInfoFormSet = inlineformset_factory(User, UserInfo, fields='__all__')
'''


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
    workplace_form = CustomWorkplaceForm(request.POST, prefix='workplace_form')
    pesel_check = request.GET.get('pesel')

    cust_inst = CustCreatePersonalInfo()
    cust_adr_inst = CustCreateAdressForm(prefix='customer_adress')
    wrk_adr_inst = CustCreateAdressForm(prefix='workplace_adr_form')    #prefix dlatego bo jest adress 2 instatncje - workplace i zwykly !!
    wrk_inst = CustomWorkplaceForm(prefix='workplace_form')

    initial = {
                'customer_form': cust_inst,
                'customer_adress': cust_adr_inst,
                'workplace_adr_form': wrk_adr_inst,
                'workplace_form': wrk_inst,
            }

    context = {
                'customer_form': customer_form,
                'customer_adress': customer_adress,
                'workplace_adr_form': workplace_adr_form,
                'workplace_form': workplace_form,
            } 

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

            return HttpResponse(merged_json, content_type='application/json')

        except:
            # print('BRAK')
            return render(request, 'core/custom_create.html', initial) 
    
    
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
        # print('JEDEN')
        return render(request, 'core/custom_create.html', context)

            
    elif request.method == 'POST' and request.POST.get('customer_id_value') != '':

        customer_id = request.POST.get('customer_id_value')
        customer_instance = Customer.objects.get(id=customer_id)

        cust_update = CustCreatePersonalInfoUpdate(request.POST, instance=customer_instance)
        cust_adress_update = CustCreateAdressForm(request.POST, prefix='customer_adress', instance=customer_instance.adress)
        workplace_adr_update = CustCreateAdressForm(request.POST, prefix='workplace_adr_form', instance=customer_instance.workplace.adress)
        workplace_update = CustomWorkplaceForm(request.POST, prefix='workplace_form', instance=customer_instance.workplace)


        cust_update.save()
        cust_adress_update.save()
        workplace_adr_update.save()
        workplace_update.save()
        
        return redirect('customer_detail', pk=customer_id)   
    
    else:
        # print('DWA!!')
        return render(request, 'core/custom_create.html', initial)


        ### SKROCIC TO - ZROBIC LADNIEJSZE, EFEKTYWNE BARDZIEJ ###

class LoginUser(LoginView):
    authentication_form = CustomLogin

    
class RegisterUser(SuccessMessageMixin, View):
    success_message = 'Account created succesufully !'
    user_info_form = CustomSignUpForm
    user_create_form = CustomUserCreationForm
    user_adress_form = CustCreateAdressForm
    template_name = 'registration/sign_up.html'
    data = {}
    data['user_info_form'] = CustomSignUpForm()
    data['user_create_form'] = CustomUserCreationForm()
    data['user_adress_form'] = CustCreateAdressForm()

    def get(self, request):

        return render(request, self.template_name, context=self.data)


    def post(self, request):
        
        user_info = self.user_info_form(self.request.POST, request.FILES or None)
        user_create = self.user_create_form(self.request.POST)
        user_adress = self.user_adress_form(self.request.POST)
        if user_info.is_valid() and user_create.is_valid():
            z = user_info.save(commit=False)
            x = user_create.save(commit=False)
            y = user_adress.save(commit=False)
            z.adress = y
            z.user = x
            x.save()
            y.save()
            z.save()

            # WYMYSLIC KROTSZA WERSJĘ !!! !! z comitem itd 
            messages.success(self.request, self.success_message)
            return HttpResponseRedirect(reverse('index'))
        context = {}
        context['user_info_form'] = user_info
        context['user_create_form'] = user_create
        context['user_adress_form'] = user_adress
        
        # print('ERRORS')
        return render(request, self.template_name, context)
            


class UserProfileView(LoginRequiredMixin, DetailView):

    model = UserInfo
    fields = '__all__'
    template_name = 'registration/profile.html'
    queryset = UserInfo.objects.all()
    # pk_url_kwarg = 'id'

    def get_object(self, queryset=None):
        queryset = self.queryset
        id = self.kwargs['id']
        obj = queryset.get(user=id)
        return obj


    def get(self, *args, **kwargs):
        id = self.kwargs['id']
        current_user = self.request.user.id

        if current_user != id:
            # return render(self.request, self.template_name, context={'massage': 'You dont have permissions to see that !!'})
            raise PermissionDenied
        return super().get(*args, **kwargs)





#### Experimenting... ####
class UserProfileEditView(LoginRequiredMixin, UpdateView):
    queryset = UserInfo.objects.all()
    template_name = 'registration/profile_edit.html'
    fields = '__all__'
    


    def get_object(self, *args, **kwargs):
        queryset = self.queryset
        id = self.kwargs['id']
        obj = queryset.get(user=id)
        return obj
    
    
    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data['user_info'] = CustomSignUpForm(instance=self.object)
        data['user_adress'] = CustCreateAdressForm(instance=self.object.adress)
        data['user_basic'] = ChangeUsername(instance=self.object.user)
        # data['user_profile_image'] = UserInfo.objects.get(id=self.kwargs['id']).profile_pic

        if self.kwargs['id'] != self.request.user.id:
            raise PermissionDenied
        return data

    def post(self, request, *args, **kwargs):
        object = self.get_object()
        forms = [
                CustCreateAdressForm(self.request.POST, instance=object.adress),
                ChangeUsername(self.request.POST, instance=object.user),
                CustomSignUpForm(self.request.POST, self.request.FILES or None,  instance=object)
                ]
        for form in forms:
            if form.is_valid():
                form.save()
                # print(form)
            else:
                return render(request, self.template_name, context={
                    'user_info':CustomSignUpForm(self.request.POST, self.request.FILES or None, instance=object),
                    'user_adress':CustCreateAdressForm(self.request.POST, instance=object.adress),
                    'user_basic':ChangeUsername(self.request.POST, instance=object.user)
                })
        return redirect('user_profile', id=self.kwargs['id'])


class UserChangePassword(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'registration/password_change.html'
    # success_url = reverse_lazy('user_password_done', kwargs={'id': })

    def get_success_url(self, *args, **kwargs):
        id = self.kwargs['id']
        # print(id)
        return reverse('user_password_done', kwargs={'id': id})
    

class UserChangePasswordDone(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'registration/password_change_done_new.html'


class UserResetPassword(SuccessMessageMixin, PasswordResetView):
    form_class = CustomPasswordResetFrorm
    success_message = 'Email has been sent to %(email)s'
    email_template_name = 'registration/reset_password_email.html'
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('index')


class UserResetPasswordForm(SuccessMessageMixin, PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    success_message = 'Password changed succesfully'
    template_name = 'registration/reset_password_form.html'
    success_url = reverse_lazy('login')



class CustomerListView(LoginRequiredMixin, ListView):

    paginate_by = 50

    def get_queryset(self):

        default_order = ['-created_date']
        order = self.request.GET.getlist('order_by', default_order)
        # print(self.request.GET)
        # print(order)
        return Customer.objects.filter(created_by=self.request.user.id).order_by(*order)

    
class CustomerDetailView(LoginRequiredMixin, DetailView):

    model = Customer
    queryset = Customer.objects.all()
    template_name = 'core/customer_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user.id != self.object.created_by.id:
            raise PermissionDenied
        return super().get(request, *args, **kwargs)


class AddNewProductView(LoginRequiredMixin, View):

    add_product_form = AddNewProductForm
    template_name = 'core/add_product.html'
    initial = {'add_product': add_product_form }

    def get(self, request, id):    
        self.add_product_form(initial=self.initial)
        customer_instance = Customer.objects.get(id=id)
        if self.request.user.id != customer_instance.created_by.id:
            raise PermissionDenied
        return render(request, self.template_name, context={'add_product': self.add_product_form, 'customer_id': customer_instance.id})

    def post(self, request, id):
        customer_instance = Customer.objects.get(id=id)
        add_prod = self.add_product_form(request.POST)
        if add_prod.is_valid():
            s = add_prod.save(commit=False)
            s.owner = customer_instance
            s.save()
            return redirect('customer_detail', pk=id)
        else:
            # print(add_prod.errors)
            return render(request, self.template_name, context={'add_product': add_prod, 'customer_id': customer_instance.id})

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
    
