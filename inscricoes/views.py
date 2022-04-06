from io import BytesIO
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.db.models import Q, Count
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView, View, TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import InscricaoForm, InscricaoNotaForm, AvisoForm
from .models import Inscricao, FimInscricoes


@login_required(login_url='login/')
def home(request):
    return render(request, 'produto_list.html')

@login_required(login_url='login/')
def produto_list(request):
    template_name = 'produto_list.html'
    objects = Inscricao.objects.order_by("id").all()
    count = Inscricao.bjects.values("cpf").annotate(Count("id"))
    contador = {'count': count}

    search = request.GET.get('search')
    if search:
        objects = objects.filter(nome__icontains=search)
    context = {'object_list': objects}
    return render(request, template_name, context, contador)

class InscricaoList(ListView):
    model = Inscricao
    template_name = 'produto_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super(InscricaoList, self).get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(nome__icontains=search) |
                Q(cpf__icontains=search)
            )
        return queryset

class ListaInscritosListView(ListView):
    model = Inscricao
    template_name = 'produto_list.html'
    context_object_name = 'inscritos'

'''PDF'''

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


class GeneratePdf(View):

    def get(self, request, *args, **kwargs):
        data = Inscricao.objects.all()
        pdf = render_to_pdf('list_pdf.html', data)
        return HttpResponse(pdf, content_type='application/pdf')



class GeneratePDF(View):

    def get(self, request, *args, **kwargs):
        object = Inscricao.objects.all()
        dados = {
            'object_list': object,
        }
        template = get_template('list_pdf.html')

        html = template.render(dados)
        pdf = render_to_pdf('list_pdf.html', dados)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %("12341231")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")



"""class GerarPDFMixin:
    def render_to_pdf(self, template_end, context_dict={}):
        template = get_template(template_end)
        html = template.render(context_dict)
        result = BytesIO()
        try:
            pdf = pisa.pisaDocument(BytesIO(html.encode("")), result)
            return HttpResponse(result.getvalue(), context_type='application/pdf')
        except Exception as e:
            print(e)
            return None
class ProdutoListPdfView(View, GerarPDFMixin):
    def get(self, request, *args, **kwargs):
        inscritos = Produto.objects.all()
        dados = {
            'inscritos': inscritos,
        }
        pdf = GerarPDFMixin()
        return pdf.render_to_pdf('list_pdf.html', dados)"""



def produto_detail(request, pk):
    template_name = 'produto_detail.html'
    obj = Inscricao.objects.get(pk=pk)
    context = {'object': obj}
    return render(request, template_name, context)


def produto_add(request):
    form = InscricaoForm(request.POST or None)
    template_name = 'produto_form2.html'

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('inscricao:produto_list'))

    context = {'form': form}
    return render(request, template_name, context)

class Upload(CreateView):
    model = Inscricao
    template_name = 'documento_form.html'
    form_class = InscricaoForm


class ProdutoCreate(CreateView):
    model = Inscricao
    template_name = 'documento_form.html'
    form_class = InscricaoForm


class ProdutoUpdate(UpdateView):
    model = Inscricao
    template_name = 'documento_form.html'
    form_class = InscricaoForm



class ProdutoNotaUpdate(UpdateView):
    model = Inscricao
    template_name = 'documento_form_nota.html'
    form_class = InscricaoNotaForm


def produto_json(request, pk):
    inscricao = Inscricao.objects.filter(pk=pk)
    data = [item.to_dict_json() for item in inscricao]
    return JsonResponse({'data': data})


def save_data(data):
    '''
    Salva os dados no banco.
    '''
    aux = []
    for item in data:
        nome = item.get('nome')
        cpf = str(item.get('cpf'))
        aprovado = True if item.get('aprovado') == 'True' else False
        email = item.get('email')

        obj = Inscricao(
            nome=nome,
            cpf=cpf,
            aprovado=aprovado,
            email=email,
        )
        aux.append(obj)
    Inscricao.objects.bulk_create(aux)


class PdfDebug(TemplateView):
    template_name = 'list_pdf.html'


"""AVISOS"""


class ListaAvisosView(ListView):
    model = FimInscricoes
    template_name = 'aviso_list.html'
    context_object_name = 'avisos'

class AvisoCreate(CreateView):
    model = FimInscricoes
    template_name = 'aviso_form.html'
    form_class = AvisoForm


class AvisoUpdate(UpdateView):
    model = FimInscricoes
    template_name = 'aviso_form.html'
    form_class = AvisoForm


class ListaAvisosView2(ListView):
    model = FimInscricoes
    template_name = 'aviso_list2.html'
    context_object_name = 'avisos'

