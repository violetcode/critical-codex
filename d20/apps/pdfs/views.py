from django import http
from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import Context
import xhtml2pdf.pisa as pisa

try:
    import StringIO
    StringIO = StringIO.StringIO
except Exception:
    from io import StringIO
import cgi

from d20.apps.core.models import Account
from d20.apps.charactersheet.models import CharacterSheet


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO()
    pdf = pisa.pisaDocument(StringIO( "{0}".format(html) ), result)
    if not pdf.err:
        return http.HttpResponse(result.getvalue(), content_type='application/pdf')
    return http.HttpResponse('There were some errors... <pre>%s</pre>' % cgi.escape(html))

def charactersheetPDF(request, slug):
    charsheet = get_object_or_404(CharacterSheet, slug=slug)
    return render_to_pdf('pdfs/character.html',{
        'pagesize':'A4',
        'title':'Charactersheet',
        'charsheet':charsheet})
