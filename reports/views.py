from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import get_template
from django.views.generic import ListView, DetailView
from xhtml2pdf import pisa
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import ReportsSearchForm
from .models import Report


# Create your views here.
class ReportsListView(LoginRequiredMixin,ListView):
    model = Report
    template_name = 'reports/main.html'

    def get_queryset(self):
        query = self.request.GET.get('search')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        reports_qs = Report.objects.all()
        print(query)
        print(date_to)
        print(date_from)
        if query:
            pass
        elif date_from or date_to:
            reports_qs = Report.objects.filter(created__date__lte=date_to, created__date__gte=date_from)
        # Do your filter and search here
        return reports_qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = ReportsSearchForm(initial={
            'search': self.request.GET.get('search', ''),
            'date_from': self.request.GET.get('date_from', ''),
            'date_to': self.request.GET.get('date_from', ''),
        })

        return context


class ReportsDetailView(LoginRequiredMixin,DetailView):
    model = Report
    template_name = 'reports/detail.html'

@login_required()
def delete_report(request, pk):
    print(request.method)
    Report.objects.get(pk=pk).delete()
    return redirect('/reports')

@login_required()
def pdf_export(request, pk):
    template_path = 'reports/pdf.html'
    report = get_object_or_404(Report, pk=pk)
    context = {'object': report}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
