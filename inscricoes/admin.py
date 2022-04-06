import csv
from datetime import datetime

from django.contrib import admin
from django.http import HttpResponse

from .models import Inscricao, FimInscricoes

MDATA = datetime.now().strftime('%Y-%m-%d')


@admin.register(FimInscricoes)
class FimInscricoes(admin.ModelAdmin):
    list_display = (
        'id',
        'fim_inscricao',


    )

@admin.register(Inscricao)
class InscricaoAdmin(admin.ModelAdmin):
    list_display = (
        'nome',
        'cpf',
        'telefone',
        'email',
        'upload',


    )
    search_fields = ('nome',)
    actions = ('export_as_csv', 'export_as_xlsx')

    class Media:
        js = (
            'https://code.jquery.com/jquery-3.3.1.min.js',
        )

    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response[
            'Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field)
                                   for field in field_names])

        return response

    export_as_csv.short_description = "Exportar CSV"

    def export_as_xlsx(self, request, queryset):

        meta = self.model._meta
        columns = (
            'nome',
            'cpf',
            'telefone',
            'email',
        )

        response = HttpResponse(content_type='application/ms-excel')
        response[
            'Content-Disposition'] = 'attachment; filename="%s_%s.xlsx"' % (meta, MDATA)

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet(self.model.__name__)

        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        default_style = xlwt.XFStyle()

        rows = queryset.values_list(
            'nome',
            'cpf',
            'telefone',
            'email',

        )
        for row, rowdata in enumerate(rows):
            row_num += 1
            for col, val in enumerate(rowdata):
                ws.write(row_num, col, val, default_style)

        wb.save(response)
        return response

    export_as_xlsx.short_description = "Exportar XLSX"
