from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader

from .forms import LogFileNameForm
from .models import Order

def home(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LogFileNameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/pretty-eyes/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LogFileNameForm()

    return render(request, 'pretty-eyes/home.html', {'form': form})

def view_log(request):
    template = loader.get_template('pretty-eyes/view_log.html')
    context = {
        #'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

def orders(request):
    orders = [{'order_id': order.order_id} for order in Order.objects.all()]
    return JsonResponse({'orders': orders[-10:]})
