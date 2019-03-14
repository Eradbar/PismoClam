import csv
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView,DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Survey
from django.contrib.auth import login
from django.views.generic.base import TemplateView

from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from blog.forms import SurveyForm
from django.template.context_processors import request
from django.forms.formsets import formset_factory

from lxml import html
import requests
from datetime import datetime

import blog.transferBeachValue
from blog import forms

BEACHES = {
    "Pismo Beach": "pismo",
    "Morro Bay": "morro",
    "Cayucos Beach": "cayucos",
    "Oceano Beach": "oceano",
    "Coronado Beach": "coronado",
    "Zuma Beach": "zuma",
    "Huntington Beach": "huntington",
    "Imperial Beach": "imperial",
    "Moonlight Beach": "moonlight",
    "Silver Strand Beach": "silverStrand",
    "Santa Monica Beach": "santaMonica",
    "Avila Beach": "avila",
    "Point Mugu Beach": "pointMugu",
}

websiteLibrary = {
    "pismoST": "http://www.surf-forecast.com/breaks/Pismo-Beach-Pier/seatemp",
    "pismoTC": "https://www.weatherforyou.com/reports/index.php?config=&forecast=zandh&pands=pismo+beach&Submit=Get+Weather",
    "morroSeaTemp": "http://www.surf-forecast.com/breaks/Morro-Bay/seatemp",
    "morroTempCoord":"https://www.weatherforyou.com/reports/index.php?config=&forecast=zandh&pands=Morro+Bay+State+Park&Submit=Get+Weather",
    "cayucosST": "http://www.surf-forecast.com/breaks/Cayucos-Pier/seatemp",
    "cayucosTC": "https://www.weatherforyou.com/reports/index.php?config=&forecast=zandh&pands=93430&Submit=Get+Weather",
    "oceanoST": "http://www.surf-forecast.com/breaks/Oceano/seatemp",
    "oceanoTC": "https://www.weatherforyou.com/reports/index.php?config=&forecast=zandh&pands=Oceano&Submit=Get+Weather",
    "coronadoST": "http://www.surf-forecast.com/breaks/Coronado-Beaches/seatemp",
    "coronadoTC": "https://www.weatherforyou.com/reports/index.php?config=&pass=&dpp=&forecast=zandh&config=&place=coronado&state=ca&country=us",
    "zumaST": "http://www.surf-forecast.com/breaks/Zuma-Beach/seatemp",
    "zumaTC": "https://www.weatherforyou.com/reports/index.php?place=zuma+beach&state=ca",
    "huntingtonST": "http://www.surf-forecast.com/breaks/Huntington-Beach/seatemp",
    "huntingtonTC": "https://www.weatherforyou.com/reports/index.php?config=&forecast=zandh&pands=Huntington+Beach&Submit=Get+Weather",
    "imperialST": "http://www.surf-forecast.com/breaks/Imperial-Beach/seatemp",
    "imperialTC": "https://www.weatherforyou.com/reports/index.php?config=&forecast=zandh&pands=Imperial+Beach&Submit=Get+Weather",
    "moonlightST": "http://www.surf-forecast.com/breaks/Moonlight-Beach/seatemp",
    "moonlightTC": "https://www.weatherforyou.com/reports/index.php?config=&forecast=zandh&pands=Moonlight+State+Beach&Submit=Get+Weather",
    "silverStrandST": "http://www.surf-forecast.com/breaks/Silver-Strand/seatemp",
    "silverStrandTC": "https://www.weatherforyou.com/reports/index.php?config=&forecast=zandh&pands=92118&Submit=Get+Weather",
    "santaMonicST": "http://www.surf-forecast.com/breaks/Santa-Monic-Pier/seatemp",
    "santaMonicaTC": "https://www.weatherforyou.com/reports/index.php?config=&forecast=zandh&pands=Santa+Monica+Pier&Submit=Get+Weather",
    "avilaST": "https://www.seatemperature.org/north-america/united-states/avila-beach.htm",
    "avilaTC": "https://www.weatherforyou.com/reports/index.php?config=&forecast=zandh&pands=93424&Submit=Get+Weather",
    "pointMuguST": "http://www.surf-forecast.com/breaks/Point-Mugu/seatemp",
    "pointMuguTC": "https://www.weatherforyou.com/reports/index.php?config=&forecast=zandh&pands=Point+Mugu&Submit=Get+Weather"
}



def home(request):
    context ={
        'surveys': Survey.objects.all()
    }
    return render(request, 'blog/home.html', context)


class selectBeach(LoginRequiredMixin, TemplateView):
    
    template_name = 'blog/beach.html'

    def get(self, request):
        blog.transferBeachValue.beach = request.POST.get('beachValue', "")
        return render(request, self.template_name)
        
    def post(self,request):
        blog.transferBeachValue.beach = request.POST.get('beachValue', "")
        print("2"+blog.transferBeachValue.beach)
        return redirect('survey-create')

    
class PostListView(LoginRequiredMixin, ListView):
    model = Survey
    template_name = 'blog/home.html'
    context_object_name = 'surveys'
    ordering = ['-date_posted']

class PostDetailView(DetailView):
    model = Survey

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Survey
    success_url = '/'

    def test_func(self):
        survey = self.get_object()
        if self.request.user == survey.author or self.request.user.is_staff:
            return True
        return False
    
class SurveyView(LoginRequiredMixin, TemplateView):
    template_name = 'blog/survey_form.html'

    def get(self, request, **kwargs):
        form = SurveyForm()
        item = kwargs.get('pk')
        beach = blog.transferBeachValue.beach
        
        try:
            url = (websiteLibrary[BEACHES[beach] + 'ST'])
            page = requests.get(url)
            tree = html.fromstring(page.content)
            seaTemp = tree.xpath('//span[@class="temp"]/text()')
            sTemp = (float(seaTemp[0]) * (9/5)) + 32
            sTemp = str(sTemp) + ' F'
        except:
            sTemp = 0;
        
        try:
            url = (websiteLibrary[BEACHES[beach] + 'TC']) 
            page = requests.get(url)
            tree = html.fromstring(page.content)
            temp = tree.xpath('//span[@class="Temp"]/text()')
            airTemp = temp[0]     
        except:
                airTemp = ""
        
        if(item != None):
            object = Survey.objects.filter(pk=kwargs.get('pk'))
            form.fields["surveyName"].initial = Survey.objects.only('surveyName').get(pk=kwargs.get('pk')).surveyName
            form.fields["location"].initial = Survey.objects.only('location').get(pk=kwargs.get('pk')).location
            form.fields["region"].initial = Survey.objects.only('region').get(pk=kwargs.get('pk')).region
            form.fields["dateSampled"].initial = Survey.objects.only('region').get(pk=kwargs.get('pk')).dateSampled
            form.fields["transNumber"].initial = Survey.objects.only('transNumber').get(pk=kwargs.get('pk')).transNumber
            form.fields["startLat"].initial = Survey.objects.only('startLat').get(pk=kwargs.get('pk')).startLat
            form.fields["startLong"].initial = Survey.objects.only('startLong').get(pk=kwargs.get('pk')).startLong
            form.fields["endLat"].initial = Survey.objects.only('endLat').get(pk=kwargs.get('pk')).endLat
            form.fields["endLong"].initial = Survey.objects.only('endLong').get(pk=kwargs.get('pk')).endLong
            form.fields["clams"].initial = Survey.objects.only('clams').get(pk=kwargs.get('pk')).clams
            form.fields["waterTemp"].initial = Survey.objects.only('waterTemp').get(pk=kwargs.get('pk')).waterTemp
            form.fields["airTemp"].initial = Survey.objects.only('airTemp').get(pk=kwargs.get('pk')).airTemp
        else:
            form.fields["location"].initial = beach            
            form.fields["waterTemp"].initial = sTemp
            form.fields["airTemp"].initial = airTemp  
            #form.fields["clams"].widget = 
        
        args = {'form': form}
        return render(request, self.template_name, args)
    
    def post(self, request, **kwargs):
        item = kwargs.get('pk')
        
        if(item == None):
            form = SurveyForm(request.POST)
            if form.is_valid():
                item = form.save(commit=False)
                item.author = request.user
                item.save()
                surveyName = form.cleaned_data['surveyName']
                location = form.cleaned_data['location']
                region = form.cleaned_data['region']
                transNumber = form.cleaned_data['transNumber']
                startLat = form.cleaned_data['startLat']
                startLong = form.cleaned_data['startLong']
                endLat = form.cleaned_data['endLat']
                endLong = form.cleaned_data['endLong']
                clams = form.cleaned_data['clams']
                waterTemp = form.cleaned_data['waterTemp']
                airTemp = form.cleaned_data['airTemp']
                return redirect('blog-home')
        else:
            form = SurveyForm(request.POST)
            if form.is_valid():
                Survey.objects.filter(pk=kwargs.get('pk')).update(surveyName=form.cleaned_data['surveyName'])
                Survey.objects.filter(pk=kwargs.get('pk')).update(location=form.cleaned_data['location'])
                Survey.objects.filter(pk=kwargs.get('pk')).update(region=form.cleaned_data['region'])
                Survey.objects.filter(pk=kwargs.get('pk')).update(transNumber=form.cleaned_data['transNumber'])
                Survey.objects.filter(pk=kwargs.get('pk')).update(startLat=form.cleaned_data['startLat'])
                Survey.objects.filter(pk=kwargs.get('pk')).update(startLong=form.cleaned_data['startLong'])
                Survey.objects.filter(pk=kwargs.get('pk')).update(endLat=form.cleaned_data['endLat'])
                Survey.objects.filter(pk=kwargs.get('pk')).update(endLong=form.cleaned_data['endLong'])
                Survey.objects.filter(pk=kwargs.get('pk')).update(clams=form.cleaned_data['clams'])
                Survey.objects.filter(pk=kwargs.get('pk')).update(waterTemp=form.cleaned_data['waterTemp'])
                Survey.objects.filter(pk=kwargs.get('pk')).update(airTemp=form.cleaned_data['airTemp'])
            return redirect('blog-home')
            
        args = {'form': form}
        return render(request, self.template_name, args)

def about(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        return render(request, 'blog/about.html', {'title': 'About'})
    
def PackClam(request):
    SurveyInstance = Survey(request.POST)
    SurveyInstance.surveyName = request.POST['SurveyName']
    SurveyInstance.location = request.POST['location']
    SurveyInstance.region = request.POST['Region']
    SurveyInstance.transNumber = request.POST['TransectNumber']
    SurveyInstance.startLat = request.POST['Slat']
    SurveyInstance.startLong = request.POST['Slon']
    SurveyInstance.endLat = request.POST['Elat']
    SurveyInstance.endLong = request.POST['Elon']
    SurveyInstance.clams = request.POST['clamSizeList']

@permission_required('admin.can_add_log_entry')
def DataDownload(request):
    items = Survey.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Dispostion'] = 'attachment; filename="pismoClamSurvey.csv"'

    writer = csv.writer(response, delimiter=',')
    writer.writerow(['title', 'content'])

    for obj in items:
        writer.writerow([obj.title, obj.content])

    return response