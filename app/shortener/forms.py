from django.forms import ModelForm
from django.urls import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Submit

from .models import URL


class URLForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(URLForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('Make it shorter', 'Make it shorter'))
        # url_list_path = reverse('url_list')
        # self.helper.layout.append(HTML(f'<a href="{url_list_path}" class="btn btn-secondary">My URL list</a>'))
			
    class Meta:
        model = URL
        fields = ('original_url', 'code')
