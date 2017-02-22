import ipaddress
from django.views.generic import TemplateView


class BaseTopologyView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(BaseTopologyView, self).get_context_data(**kwargs)
        context.update({'src_address': self.src_address()})
        return context

    def src_address(self):
        address = None
        if self.request.META:
            if 'HTTP_X_FORWARDED_FOR' in self.request.META:
                addr = unicode(self.request.META['HTTP_X_FORWARDED_FOR'].split(',')[0])
            else:
                addr = unicode(self.request.META['REMOTE_ADDR'])
            address = ipaddress.ip_address(address=addr)
        return address


class IndexView(BaseTopologyView):
    template_name = 'ncrawl/index.html'
