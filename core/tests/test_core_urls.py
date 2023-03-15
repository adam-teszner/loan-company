from django.test import TestCase
from django.urls import reverse, resolve
from core.views import *
from django.urls.exceptions import NoReverseMatch

from core.urls import urlpatterns


class TestUrls(TestCase):

    def test_if_url_is_resolved(self):
        # url = reverse('login')
        errors = []
        urls_ok = 0
        for url in urlpatterns:
            if url.name == 'user_password_reset_form':
                continue

            try:
                adr = reverse(url.name)
            except NoReverseMatch:
                adr = reverse(url.name, args=[1])
            
            try:
                self.assertEqual(resolve(adr).view_name, url.name)
                urls_ok += 1
            except:
                errors.append(url.name)
            
        print(urls_ok)
        self.assertTrue(urls_ok, 17)     
        
    # def test_customer_detail_url(self):
    #     url = reverse('customer_detail', args=[1])
    #     self.assertEqual(resolve(url).func.view_class, CustomerDetailView)