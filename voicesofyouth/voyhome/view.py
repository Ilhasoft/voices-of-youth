from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.conf import settings
from django.core.mail import send_mail

from voicesofyouth.voyhome.models import Slide
from voicesofyouth.voyhome.models import About
from voicesofyouth.user.models import MapperUser
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


class ReorderSlideView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        image_id = kwargs['image']
        act = kwargs['act']
        if image_id:
            image = get_object_or_404(Slide, pk=image_id)
            if act == 'up':
                image.up()
            elif act == 'down':
                image.down()
        return redirect(reverse('voy-admin:home:index_slide'))


class AboutView(LoginRequiredMixin, TemplateView):
    template_name = 'about/form.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()

        form = AboutForm(
            request.POST,
            request.FILES,
            instance=context.get('instance'))

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

        context['data_form'] = AboutForm(instance=about)
        context['image'] = about.thumbnail if hasattr(about, 'image') else None
        context['instance'] = about
        return context


class JoinRequestsView(LoginRequiredMixin, TemplateView):
    template_name = 'join/index.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        user = self.request.user
        if user.is_local_admin:
            messages.error(request, _('Access denied'))
            return redirect(reverse('voy-admin:home:index'))

        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['requests'] = MapperUser.objects.filter(is_active=False).order_by('-modified_on')
        return context


class JoinRequestsDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'join/view.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        user = self.request.user
        if user.is_local_admin:
            messages.error(request, _('Access denied'))
            return redirect(reverse('voy-admin:home:index'))

        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mapper_id = self.kwargs['mapper']
        context['mapper'] = get_object_or_404(MapperUser, pk=mapper_id)
        return context


class ApproveRequestsView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        mapper_id = kwargs['mapper']
        if mapper_id:
            mapper = get_object_or_404(MapperUser, pk=mapper_id)
            mapper.is_active = True
            mapper.save()

            if settings.EMAIL_HOST:
                send_mail(
                    'Welcome to Voices of Youth',
                    'Hi {}! You are a new mapper.'.format(mapper.first_name),
                    settings.EMAIL_FROM,
                    [mapper.email],
                    fail_silently=True,
                )

            messages.success(request, _('Mapper approved'))
        return redirect(reverse('voy-admin:home:index_requests'))


class RemoveRequestsView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        mapper_id = kwargs['mapper']
        if mapper_id:
            mapper = get_object_or_404(MapperUser, pk=mapper_id)
            mapper.delete()

            messages.success(request, _('Mapper removed'))
        return redirect(reverse('voy-admin:home:index_requests'))
