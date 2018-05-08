from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from voicesofyouth.voyhome.models import Slide
from voicesofyouth.voyhome.models import About
from voicesofyouth.voyhome.models import Contact
from voicesofyouth.voyhome.forms import SlideForm
from voicesofyouth.voyhome.forms import AboutForm


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


class AboutView(LoginRequiredMixin, TemplateView):
    template_name = 'about/form.html'

    def post(self, request, *args, **kwargs):
        form = AboutForm(request.POST, request.FILES)

        if form.is_valid():
            about = About.objects.all().first()
            if about:
                about.image = form.cleaned_data.get('image')
                about.about_project = form.cleaned_data.get('about_project')
                about.about_voy = form.cleaned_data.get('about_voy')
                about.save()
            else:
                about = About(
                    image=form.cleaned_data.get('image'),
                    about_project=form.cleaned_data.get('about_project'),
                    about_voy=form.cleaned_data.get('about_voy'),
                    created_by=request.user,
                    modified_by=request.user
                )
                about.save()
            messages.success(request, _('About saved'))
            return redirect(reverse('voy-admin:home:index_about'))
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
        about = About.objects.first()

        data = {
            'image': about.image if hasattr(about, 'image') else None,
            'about_project': about.about_project if hasattr(about, 'about_project') else None,
            'about_voy': about.about_voy if hasattr(about, 'about_voy') else None
        }

        context['data_form'] = AboutForm(initial=data)
        context['image'] = about.thumbnail if hasattr(about, 'image') else None
        return context


class ContactView(LoginRequiredMixin, TemplateView):
    template_name = 'contact/index.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        user = self.request.user
        if user.is_local_admin:
            messages.error(request, _('Access denied'))
            return redirect(reverse('voy-admin:home:index'))

        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contacts'] = Contact.objects.order_by('-created_on')
        return context


class ContactMessageView(LoginRequiredMixin, TemplateView):
    template_name = 'contact/view.html'

    def post(self, request, *args, **kwargs):
        contact_id = self.kwargs['contact']
        if contact_id:
            contact = get_object_or_404(Contact, pk=contact_id)
            contact.delete()
            messages.success(request, _('Contact removed'))
        return redirect(reverse('voy-admin:home:index_contact'))

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        user = self.request.user
        if user.is_local_admin:
            messages.error(request, _('Access denied'))
            return redirect(reverse('voy-admin:home:index'))

        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contact_id = self.kwargs['contact']
        context['message'] = get_object_or_404(Contact, pk=contact_id)
        return context
