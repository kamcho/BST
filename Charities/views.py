from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.db.models import Sum

from Payments.models import CharityPayments, ProjectPayments
from .models import Charity, ChurchProjects
# Create your views here.



class CharitiesView(TemplateView):
    template_name = 'Charities/charities.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        charities = Charity.objects.filter(archived=False).order_by('created')
        context['charities'] = charities


        return context
    

class CreateCharity(TemplateView):
    template_name = 'Charities/create_charity.html'


    def post(self, *args, **kwargs):
        if self.request.method == 'POST':
            ends_on = self.request.POST.get('date')
            target = self.request.POST.get('target')
            title = self.request.POST.get('title')
            description = self.request.POST.get('description')

            charity = Charity.objects.create(target=target, title=title,
                                              description=description, closes_on=ends_on, totals=0)
            
            return redirect('charity-id', charity.id)

class CharityDetail(TemplateView):
    template_name = 'Charities/charity_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        charity = self.kwargs['id']
        charity = Charity.objects.get(id=charity)
        context['charity'] = charity
        contributions = CharityPayments.objects.filter(charity=charity)
        totals = contributions.aggregate(totals=Sum('amount'))['totals']
        if not totals:
            totals = 0
        context['balance'] = charity.target - totals
        context['totals'] = totals
        context['contributions'] = contributions
        return context
    
class ManageCharity(TemplateView):
    template_name = 'Charities/manage_charity.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        charity = self.kwargs['charity_id']
        charity = Charity.objects.get(id=charity)
        context['charity'] = charity

        return context
    
    def post(self, *args, **kwargs):
        if self.request.method == 'POST':
            ends_on = self.request.POST.get('date')
            target = self.request.POST.get('target')
            title = self.request.POST.get('title')
            description = self.request.POST.get('description')

            object_instance = self.get_context_data().get('charity')
            if 'update' in self.request.POST:
                object_instance.title = title
                object_instance.description = description
                object_instance.target = target
                # object_instance.closes_on = ends_on
                object_instance.save()

                return redirect(self.request.get_full_path())
            
            elif 'delete' in self.request.POST:
                object_instance.archived = True
                object_instance.save()

                return redirect('charities')
            




class ProjectsView(TemplateView):
    template_name = 'Charities/projects.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projects = ChurchProjects.objects.filter(archived=False, completed=False).order_by('created')
        context['projects'] = projects


        return context
    

class CreateProject(TemplateView):
    template_name = 'Charities/create_project.html'


    def post(self, *args, **kwargs):
        if self.request.method == 'POST':
            ends_on = self.request.POST.get('date')
            target = self.request.POST.get('target')
            title = self.request.POST.get('title')
            description = self.request.POST.get('description')

            project = ChurchProjects.objects.create(target=target, title=title,
                                              description=description, closes_on=ends_on)
            
            return redirect('project-id', project.id)

class ProjectDetail(TemplateView):
    template_name = 'Charities/project_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.kwargs['id']
        project = ChurchProjects.objects.get(id=project)
        context['project'] = project
        contributions = ProjectPayments.objects.filter(project=project)
        totals = contributions.aggregate(totals=Sum('amount'))['totals']
        if not totals:
            totals = 0
        context['balance'] = project.target - totals
        context['totals'] = totals
        context['contributions'] = contributions
        return context
    
class ManageProject(TemplateView):
    template_name = 'Charities/manage_project.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.kwargs['project_id']
        project = ChurchProjects.objects.get(id=project)
        context['project'] = project

        return context
    
    def post(self, *args, **kwargs):
        if self.request.method == 'POST':
            ends_on = self.request.POST.get('date')
            target = self.request.POST.get('target')
            title = self.request.POST.get('title')
            description = self.request.POST.get('description')

            object_instance = self.get_context_data().get('project')
            if 'update' in self.request.POST:
                object_instance.title = title
                object_instance.description = description
                object_instance.target = target
                # object_instance.closes_on = ends_on
                object_instance.save()

                return redirect(self.request.get_full_path())
            
            elif 'delete' in self.request.POST:
                object_instance.archived = True
                object_instance.save()

                return redirect('projects')