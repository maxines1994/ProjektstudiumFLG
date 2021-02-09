from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView
from gtapp.models import CustOrder, CustOrderDet, SuppOrder
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin


# Stornierung CustOrder Position
class Cust_order_det_cancel_view(LoginRequiredMixin, UpdateView):
    fields = []
    template_name = "cancel.html"

    def get_object(self, queryset=None):
        obj = CustOrderDet.objects.get(id=self.kwargs['id'])
        return obj

    def form_valid(self, form):
        obj = self.get_object()
        obj.status = obj.Status.STORNIERT
        obj.save()
        return HttpResponseRedirect("/cust_order/alter/" + str(form.instance.cust_order.id) + "/")

# Stornierung CustOrder
class Cust_order_cancel_view(LoginRequiredMixin, UpdateView):
    fields = []
    template_name = "cancel.html"

    def get_object(self, queryset=None):
        obj = CustOrder.objects.get(id=self.kwargs['id'])
        return obj

    def form_valid(self, form):
        obj = self.get_object()
        dets = CustOrderDet.objects.filter(cust_order=obj.id)
        if not dets.exclude(status=CustOrderDet.Status.BESTANDSPRUEFUNG_AUSSTEHEND).exclude(status=CustOrderDet.Status.STORNIERT).exists():
            for det in dets:
                det.status = det.Status.STORNIERT
                det.save()
            return HttpResponseRedirect("/cust_order/alter/" + str(form.instance.id) + "/")
        else:
            return Http404()


# Stornierung CustOrder
class Supp_order_cancel_view(LoginRequiredMixin, UpdateView):
    fields = []
    template_name = "cancel.html"

    def get_object(self, queryset=None):
        obj = SuppOrder.objects.get(id=self.kwargs['id'])
        return obj

    def form_valid(self, form):
        obj = self.get_object()
        obj.status = obj.Status.STORNIERT
        obj.save()
        return HttpResponseRedirect("/supp_order/")

