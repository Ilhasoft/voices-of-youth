from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models.query_utils import Q

from voicesofyouth.theme.models import Theme
from voicesofyouth.tag.models import Tag


class ReportFilterForm(forms.Form):
    theme = forms.ModelChoiceField(queryset=None,
                                   required=False,
                                   empty_label='Theme',
                                   widget=forms.Select(attrs={'class': 'form-control m-b'}))

    tag = forms.ModelChoiceField(queryset=None,
                                 required=False,
                                 empty_label='Tag',
                                 widget=forms.Select(attrs={'class': 'form-control m-b'}))

    def __init__(self, *args, **kwargs):
        project_qs = kwargs.pop('project')
        super(ReportFilterForm, self).__init__(*args, **kwargs)

        ct_project = ContentType.objects.get_for_model(project_qs)

        themes_qs = Theme.objects.filter(project=project_qs).distinct()
        tags_qs = Tag.objects.filter(Q(content_type=ct_project, object_id=project_qs.id)).distinct()
        # tag_qs = Tag.objects.filter(project=project_qs).distinct()

        self.fields['theme'].queryset = themes_qs
        self.fields['tag'].queryset = tags_qs
