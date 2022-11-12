from django.contrib.auth.models import User


def search(request):

    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    users = User.objects.filter(username__iexact=search_query)
    return users, search_query