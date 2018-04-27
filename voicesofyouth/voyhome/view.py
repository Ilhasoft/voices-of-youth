from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from voicesofyouth.voyhome.models import Slide
from voicesofyouth.voyhome.forms import SlideForm


class SlideView(LoginRequiredMixin, TemplateView):
    template_name = 'slide/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = Slide.objects.all()
        return context


class AddSlideView(LoginRequiredMixin, TemplateView):
    template_name = 'slide/form.html'

    def post(self, request, *args, **kwargs):
        form = SlideForm(request.POST, request.FILES)

        if form.is_valid():
            slide = Slide(
                image=form.cleaned_data.get('image'),
                created_by=request.user,
                modified_by=request.user,
            )
            slide.save()
            messages.success(request, _('Image saved'))
            return redirect(reverse('voy-admin:home:index_slide'))
        else:
            context = self.get_context_data()
            context['data_form'] = form
            messages.error(request, form.non_field_errors())

            return render(request, self.template_name, context)

        return self.get(request)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        user = self.request.user
        if user.is_local_admin:
            messages.error(request, _('Access denied'))
            return redirect(reverse('voy-admin:home:index'))

        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_form'] = SlideForm()
        return context


class RemoveSlideView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        image_id = kwargs['image']
        if image_id:
            image = get_object_or_404(Slide, pk=image_id)
            image.delete()

            messages.success(request, _('Image removed'))
        return redirect(reverse('voy-admin:home:index_slide'))
