from django.urls import path


from inscricoes import views as v

app_name = 'inscricoes'


urlpatterns = [
    path('', v.InscricaoList.as_view(), name='produto_list'),
    path('listpdf/', v.GeneratePDF.as_view(), name='list_pdf'),
    path('<int:pk>/', v.produto_detail, name='produto_detail'),
    path('add/', v.ProdutoCreate.as_view(), name='produto_add'),
    path('add2/', v.produto_add, name='produto_add2'),
    path('<int:pk>/edit/', v.ProdutoUpdate.as_view(), name='produto_edit'),
    path('<int:pk>/json/', v.produto_json, name='produto_json'),

]
