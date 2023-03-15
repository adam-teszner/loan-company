from urllib.parse import parse_qs, urlencode, urlparse

from django import template
from django.core.exceptions import ObjectDoesNotExist

from core.models import UserInfo

register = template.Library()


@register.simple_tag(takes_context=True)
def user_first_name(context):
    request = context['request']
    try:
        user_id = request.user.id
        user_name = UserInfo.objects.get(user=user_id)
        return user_name.first_name
    except ObjectDoesNotExist:
        return request.user.username


@register.simple_tag(takes_context=True)
def user_last_name(context):
    request = context['request']
    try:
        user_id = request.user.id
        user_name = UserInfo.objects.get(user=user_id)
        return user_name.last_name
    except ObjectDoesNotExist:
        return None


@register.simple_tag(takes_context=True)
def user_icon(context):
    request = context['request']
    try:
        user_id = request.user.id
        user = UserInfo.objects.get(user=user_id)
        return user.first_name[0].upper() + user.last_name[0].upper()
    except ObjectDoesNotExist:
        return None


@register.simple_tag(takes_context=True)
def sort_table_header(context, th_name=None, paginate=False):
    '''
    Creates a querystring with sorting parameters.
    Arranges sort-order by order of clicking eg:
    Last column clicked becomes first in sorting order.
    ----
    Params:
        context (dict): Passed by django
        th_name (str): Table header name
        pagintate (bool): Set to True when tag is placed inside pagination
            navigation. Put page number after the tag, e.g.
    
    ``` <a href="{% sort_table_header paginate=True %}
        {{ page_obj.next_page_number }}">next</a> ```
    
    Returns:
        Full path with column sorting order and page number (if present)
    '''
    request = context['request']
    path = request.get_full_path_info()
    query_params = urlparse(path).query
    base = urlparse(path).path
    order = parse_qs(query_params).get('order_by')
    page = parse_qs(query_params).get('page')
    
    if order is None:
        order = []

    if paginate == True:
        page = ''

    # Move table column header-name to the beginning of sorting order
    # If header already present in sorting order change sorting
    # method to oppsite (if asc, change to dsc)
    if th_name in order:
        order.remove(th_name)
        order.insert(0, f'-{th_name}')
    elif f'-{th_name}' in order:
        order.remove(f'-{th_name}')
        order.insert(0, th_name)
    else:
        order.insert(0, th_name) if th_name is not None else order

    query_string = {
        'order_by': order,
        'page': page
    }

    # If first page or no pagination, remove page from query_string
    if page is None:
        query_string.pop('page')

    # Remove "order_by" key when order list is empty
    if not order:
        query_string.pop('order_by')

    new_url_query = urlencode(query_string, doseq=True)
    url = base + '?' + new_url_query
    return url


@register.simple_tag(takes_context=True)
def sort_active_th(context):
    request = context['request']
    return str(request.GET.getlist('order_by'))
