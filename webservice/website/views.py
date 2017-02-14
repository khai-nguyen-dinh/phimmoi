from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from django.views import generic

from website.models import Phim


class IndexView(generic.ListView):
    template_name = 'website/index.html'
    context_object_name = 'list_film'

    def get_queryset(self):
        return Phim.objects.order_by('-year')[:8]

def list_all_phim_le(request):
    tmp = Phim.objects.order_by('-year')
    paginator = Paginator(tmp, 20)
    page = request.GET.get('page')
    try:
        list_film = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        list_film = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        list_film = paginator.page(paginator.num_pages)

    return render(request, 'website/get_all_data.html', {'list_film': list_film})


def get_data_from_search(request):

    if request.method == 'POST':
        text = request.POST['text']
    else:
        text = request.GET.get('q')

    tmp = Phim.objects.filter(title__contains=text)
    paginator = Paginator(tmp, 20)
    page = request.GET.get('page')
    try:
        list_film = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        list_film = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        list_film = paginator.page(paginator.num_pages)

    return render(request, 'website/search.html', {'list_film': list_film, 'q': text})
