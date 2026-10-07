from django.views.generic import (CreateView, DetailView, ListView, TemplateView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from . import (models, forms)


class PhotographListView(LoginRequiredMixin, ListView):
    """
    Class-based view for Photograph list template
    """
    template_name = 'photographs/list.html'
    model = models.Photograph

    def get_queryset(self):
        queryset = self.model.objects.filter(published=True)
        search = self.request.GET.get('search', '')
        if search != '':
            queryset = queryset.filter(
                Q(image__icontains=search) |
                Q(image_name_es__icontains=search) |
                Q(image_name_en__icontains=search) |
                Q(description_es__icontains=search) |
                Q(description_en__icontains=search) |
                Q(acknowledgements__icontains=search) |
                Q(notes__icontains=search)
            )
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PhotographDetailView(LoginRequiredMixin, DetailView):
    """
    Class-based view for Photograph detail template
    """
    template_name = 'photographs/detail.html'
    model = models.Photograph

    def get_queryset(self):
        queryset = self.model.objects.all()
        # Users who aren't logged in cannot see unpublished objects
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(published=True)
        return queryset

    def get_context_data(self, **kwargs):
        # Get current context
        context = super().get_context_data(**kwargs)
        # Add form for creating a user_contribution
        context['usercontribution_create_form'] = forms.PhotographUserContributionCreateForm
        return context


class PhotographUserContributionCreateView(LoginRequiredMixin, CreateView):
    """
    Class-based view to create a new models.PhotographUserContribution object in the database.

    Note that this view doesn't have a template.
    It's only intended to receive post requests and redirect on success/fail.

    The template that includes the HTML form for submitting to this view is in the above PhotographDetailView.
    See the get_context_data() method in the PhotographDetailView for more details.
    """

    template_name = 'photographs/usercontribution-create-success.html'
    form_class = forms.PhotographUserContributionCreateForm
    success_url = reverse_lazy('photographs:usercontribution-create-success')

    def form_invalid(self, form):
        return reverse_lazy('photographs:usercontribution-create-fail')


class PhotographUserContributionCreateSuccessTemplateView(LoginRequiredMixin, TemplateView):
    """
    Class-based view to show the PhotographUserContribution create success template
    """

    template_name = 'photographs/usercontribution-create-success.html'
