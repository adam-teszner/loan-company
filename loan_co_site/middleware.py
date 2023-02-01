# import datetime


class CookieMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not request.COOKIES.get('visited'):
            response.set_cookie('visited', 'yes', max_age=2592000)
            # print('NO COOKIE')

        return response