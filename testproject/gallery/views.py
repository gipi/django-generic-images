# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext

from gallery.models import Cat


def gallery(request):
    return render_to_response(
        'gallery/gallery.html',
        {"cats": Cat.objects.all()},
        context_instance=RequestContext(request)
    )
