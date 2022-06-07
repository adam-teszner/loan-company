from core.models import UserInfo
from django.template import Library



register = Library()

@register.simple_tag(takes_context=True)
def user_first_name(context):
    request = context['request']
    try:
        user_id = request.user.id
        user_name = UserInfo.objects.get(user=user_id)
        return user_name.first_name
    except:
        return request.user.username