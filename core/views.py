from django.shortcuts import redirect, render
from django.contrib import messages

from .forms import ContatoForm, ProdutoModelForm
from .models import Produto
def index(req):
    context = {
        'produtos': Produto.objects.all()
    }
    return render(req, 'index.html', context)

def contato(req):
    form = ContatoForm(req.POST or None)

    if str(req.method) == 'POST':
        if form.is_valid():
            form.send_mail()

            messages.success(req, 'E-mail enviado com sucesso')
            form = ContatoForm()
        else:
            messages.error(req, 'Erro ao enviar')

    context = {
        'form': form
    }
    return render(req, 'contato.html', context)

def produto(req):
    if str(req.user) != 'AnonymousUser':
        if str(req.method) == 'POST':
            form = ProdutoModelForm(req.POST, req.FILES)
            if form.is_valid():

                form.save()
            
                messages.success(req, 'Produto salvo')
                form = ProdutoModelForm()
            else:
                messages.error(req, 'Não foi possivel salvar')
        else:
            form = ProdutoModelForm()
        context = {
            'form': form
            }
        return render(req, 'produto.html', context)
    else: 
        return redirect('index')