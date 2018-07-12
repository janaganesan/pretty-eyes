from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
from django.views import generic
from django import forms

from .forms import LogFileNameForm
from .models import Order, Report
from .config import read_config, write_config

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
            return HttpResponseRedirect('/prettyeyes/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LogFileNameForm()

    return render(request, 'prettyeyes/home.html', {'form': form})

def filters(request):
    filters = {}
    content = read_config()
    if 'filters' in content:
        filters = content['filters']

    if request.method == 'POST':
        filters = {}
        data = request.POST
        for key, value in zip(data.getlist("key"), data.getlist("value")):
            filters[key] = value
        write_config({'filters': filters})

    elif request.is_ajax():
        return JsonResponse({'filters': filters})

    return HttpResponse('')

def prettyeyes(request):
    template = loader.get_template('prettyeyes/prettyeyes.html')
    context = {
        #'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

def orders(request):
    orders = []
    for o in Order.objects.all():
        order = {}
        order.update({'order_id': o.order_id, 'pk': o.id})
        order['reports'] = [{'name': r.name(), 'pk': r.pk} for r in o.report_set.all() if r.is_matching_filter()]
        orders.append(order)
    return JsonResponse({'orders': orders})

def order_detail(request):
    orders = [{'order_id': order.order_id, 'pk': order.id} for order in Order.objects.all()]
    return JsonResponse({'orders': orders})

class OrderDetailView(generic.DetailView):
    model = Order
    # DOCS: template name is client_detail
    template_name = 'prettyeyes/report.html'

    # Use this to pass any extra information
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(OrderDetailView).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        # context['reverse_report'] = self.get_object().report_set.all()[::-1]
        return context

def report_detail(request, pk):
    order = Order.objects.get(id=pk)
    reports = [{'name': r.name(), 'pk': r.pk, 'report': str(r)} for r in order.report_set.all()]
    return JsonResponse({'reports': reports})

def report_table(request, pk):
    report = Report.objects.get(id=pk)
    data = report.report_json()['report']
    return render(request, 'prettyeyes/report_table.html', {'data': sorted(data.items())})

