import os
from pprint import pprint
import pathlib

from django import forms
from django.db import transaction
from django.db.models.functions import Lower
from django.views.generic import FormView, DeleteView, CreateView, UpdateView
from django.views.generic import ListView, DetailView, TemplateView

from apps.main.models import Experiment, Configuration
from apps.main.models import Parameter, CHAR_LENGTH


APP_NAME= 'main'
DEFAULT_PATH = '/daqroot'


def path_getter(uri=DEFAULT_PATH):
    if uri is None:
        uri = DEFAULT_PATH
    path = pathlib.Path(uri.replace('file:', ''))
    if not path.exists():
        path = pathlib.Path(DEFAULT_PATH)
    # show_parent =  path.as_posix() != DEFAULT_PATH
    p = path
    parents = []
    if p.is_dir():
        parents.append(p)
    while p.as_posix() != DEFAULT_PATH:
        p = p.parent
        parents.append(p)
    parents = parents[::-1]
    if parents:
        parents = parents[1:]

    if path.is_dir():
        entries = [p for p in path.iterdir() if not p.name.startswith('.')]
    else:
        entries = []
    return parents, path, entries

class NewExperimentForm(forms.ModelForm):
    class Meta:
        model = Experiment
        fields = ['name']



class NewConfigView(CreateView):
    model = Configuration
    fields = ['name', 'experiment']

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['experiment_id'] = self.kwargs['experiment_id']
        return context

    def get_form(self):
        form = super().get_form()
        form.fields['experiment'].widget = forms.HiddenInput()
        form.fields['experiment'].initial = int(self.kwargs['experiment_id'])
        return form

    def get_success_url(self):
        return r'/main/experiment/{}'.format(self.kwargs['experiment_id'])


class DeleteExperimentView(DeleteView):
    model = Experiment
    success_url = '/main/experiment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['configs'] = Configuration.objects.filter(experiment=context['experiment']).order_by(Lower('name'))
        return context

class DeleteConfigView(DeleteView):
    model = Configuration

    def get_success_url(self):
        return r'/main/experiment/{}'.format(self.get_context_data()['configuration'].experiment_id)

class DeleteParamView(DeleteView):
    model = Parameter

    def get_object(self, queryset=None):
        param = Parameter.objects.get(id=int(self.kwargs['param_id']))
        self.config_id = param.configuration_id
        return param

    def get_success_url(self):
        return r'/main/config/{}'.format(self.config_id)


class NewExperimentView(CreateView):
    model = Experiment
    fields = ['name']

    def get_success_url(self):
        return r'/main/experiment'


class CloneExperimentView(FormView):
    template_name = '{}/experiment_update_form.html'.format(APP_NAME)
    form = NewExperimentForm
    form_class = form

    def form_valid(self, form):
        experiment = Experiment.objects.get(id=int(self.kwargs['experiment_id']))
        experiment.clone(form.cleaned_data['name'])
        return super().form_valid(form)

    def get_success_url(self):
        return r'/main/experiment'


class CloneConfigForm(forms.ModelForm):
    class Meta:
        model = Configuration
        fields = ['name']

class CloneConfigView(FormView):
    template_name = '{}/configuration_update_form.html'.format(APP_NAME)
    form_class = CloneConfigForm

    def form_valid(self, form):
        config = Configuration.objects.get(id=int(self.kwargs['config_id']))
        config.clone(new_name=form.cleaned_data['name'])
        self.experiment_id = config.experiment_id
        return super().form_valid(form)

    def get_success_url(self):
        return r'/main/experiment/{}'.format(self.experiment_id)


class ExperimentListView(ListView):
    model = Experiment

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    def get_queryset(self):
        return Experiment.objects.all().order_by(Lower('name'))


class ConfigListView(ListView):
    model = Configuration

    def get_queryset(self):
        return Configuration.objects.filter(
            experiment_id=int(self.kwargs['experiment_id'])
        ).order_by(Lower('name'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['experiment'] = Experiment.objects.get(id=int(self.kwargs['experiment_id']))
        return context

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)


class ChangeParamView(UpdateView):
    model = Parameter
    fields = ['name', 'type']
    template_name = '{}/update_parameter_view.html'.format(APP_NAME)

    def get_object(self):
        return Parameter.objects.get(id=int(self.kwargs['param_id']))

    def get_success_url(self):
        param = self.get_object()
        url = '/main/config/{}'.format(param.configuration_id)
        print('>>>>>>>>> url {}'.format(url))
        return url

    def form_valid(self, form):
        param = self.get_object()
        if Parameter.objects.filter(configuration=param.configuration, name=form.data['name']).exists():
            form.add_error('name', 'A parameter named "{}" already exists'.format(form.data['name']))
            return self.form_invalid(form)
        return super().form_valid(form)


class NewParamView(CreateView):
    model = Parameter
    fields = ['name', 'type', 'configuration']

    def get_form(self):
        form = super().get_form()
        form.fields['configuration'].widget = forms.HiddenInput()
        form.fields['configuration'].initial = int(self.kwargs['config_id'])
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['config_id'] = self.kwargs['config_id']
        return context

    def get_success_url(self):
        return '/main/config/{}'.format(self.kwargs['config_id'])

class TagForm(forms.Form):
    pass


class TagFileView(FormView):
    template_name = '{}/tag_file.html'.format(APP_NAME)
    form_class = TagForm
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._success_url = ''

    def get_success_url(self):
        return self._success_url

    def get_form(self):
        form = super().get_form()
        form.request = self.request
        form.view = self

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        path_uri = self.request.GET.get('path_uri')
        parents, path, entries = path_getter(path_uri)
        context['csv_file'] = path
        context['netcdf_file'] = path.parent.joinpath(path.name.replace(path.suffix, '.nc'))
        context['config_id'] = self.kwargs['config_id']
        context['params'] = Parameter.objects.filter(configuration_id=int(self.kwargs['config_id']))
        return context

class ParamForm(forms.Form):
    type_map = {
        'str': forms.CharField,
        'int': forms.IntegerField,
        'float': forms.FloatField,
    }

    def clean(self):
        clean_data = super().clean()
        clean_data['selected_file'] = self.request.POST.get('selected_file')
        clean_data['current_path'] = self.request.POST.get('current_path')
        clean_data.update(self.view.kwargs)
        return clean_data

class ParamListView(FormView):
    template_name = '{}/parameter_list.html'.format(APP_NAME)
    form_class = ParamForm
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._success_url = ''

    def get_success_url(self):
        return self._success_url

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs['request'] = self.request

    def get_form(self):
        form = super().get_form()
        form.request = self.request
        form.view = self
        self._success_url = '/main/config/{}'.format(self.kwargs['config_id'])
        params = Parameter.objects.filter(configuration_id=int(self.kwargs['config_id'])).order_by(Lower('name'))
        for param in params:
            field_class = form.type_map[param.type]
            form.fields['params{}'.format(param.id)] = field_class(initial=param.value, label=param.name)

        # form.fields['input_file'] = forms.FileField(label="", required=False)
        # form.fields['input_file'].required = False
        return form

    def get_context_data(self, **kwargs):
        path_uri = self.request.GET.get('path_uri')
        parents, path, entries = path_getter(path_uri)

        context = super().get_context_data(**kwargs)
        context['config'] = Configuration.objects.get(id=int(self.kwargs['config_id']))
        context['current_path'] = path
        context['entries'] = entries
        context['parents'] = parents

        return context

    def save_params_values(self, cleaned_data):
        for key, value in cleaned_data.items():
            if 'params' in key:
                param_id = int(key.replace('params', ''))
                param = Parameter.objects.get(id=param_id)
                param.value = value
                param.save()

    def tag_file_if_needed(self, cleaned_data):
        path, file_name = cleaned_data['current_path'], cleaned_data['selected_file']
        if path and file_name:
            path = pathlib.Path(os.path.join(cleaned_data['current_path'], cleaned_data['selected_file']))
            self._success_url = '/main/tag_file/{}/?path_uri={}'.format(
                cleaned_data['config_id'],
                path.as_uri(),
            )

    @transaction.atomic
    def form_valid(self, form):
        self.save_params_values(form.cleaned_data)
        print()
        pprint(form.cleaned_data)

        self.tag_file_if_needed(form.cleaned_data)
        return super().form_valid(form)
    # def save_params_values(self, cleaned_data):
    #
    # @transaction.atomic
    # def form_valid(self, form):
    #
    #     for key, value in form.cleaned_data.items():
    #         if 'params' in key:
    #             param_id = int(key.replace('params', ''))
    #             param = Parameter.objects.get(id=param_id)
    #             param.value = value
    #             param.save()
    #
    #     return super().form_valid(form)

    # def render_to_response(self, context, **response_kwargs):
    #     return super().render_to_response(context, **response_kwargs)


class FilePickerView(TemplateView):
    template_name = '{}/tag_file.html'.format(APP_NAME)

    # # IM WORKING ON A FILE_PICKER VIEW.  IT WILL SIMPLY TAKE A PATHLIB .AS_URI()
    # # STRING AS AN ARGUMENT AND RENDER LINKS TO OTHER PATHS
    # # MAYBE I SHOULD PUT THE URI AS AN HTML QUERY PARAMETER
    #
    #
    # # Here is some code I was playing with in ipython notebook
    # #
    # import pathlib
    # import os
    # import urllib
    #
    # p0 = pathlib.Path('/Users/rob/Google Drive/')
    #
    # file_list, path_list = [], []
    # for f in p.iterdir():
    #     if f.name.startswith('.'):
    #         continue
    #
    #     if f.is_dir():
    #         path_list.append(f)
    #     else:
    #         file_list.append(f)
    #
    # p0.as_uri()
