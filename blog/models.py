from urllib.request import urlopen
from django.db import models
from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import validate_comma_separated_integer_list
from dataclasses import field
from importlib.resources import contents
from turtledemo.chaos import plot
#from pip._vendor.requests.api import post

class Post(models.Model):
    title = models.CharField(max_length = 100)
    content = models.CharField(max_length = 100)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
class PostContent(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    content = models.CharField(max_length = 100)
    
class PostForm(forms.ModelForm):
    title = forms.CharField(required=True)
    
    def __init__(self, *args, **kwargs):
        super.__init__(*args, **kwargs)
        contents = PostContent.objects.filter(
            content=self.instance
        )
        for i in range(len(contents) + 1):
            field_name = 'content_%s' % (i,)
            self.fields[field_name] = forms.CharField(required=False)
            try:
                self.initial[field_name] = contents[i].content
            except IndexError:
                self.initial[field_name] = ""
                
        field_name = 'content_%s' % (i + 1,)
        self.fields[field_name] = forms.CharField(required=False)
        self.fields[field_name] = ""
        
    def clean(self):
        contents = set()
        i = 0
        field_name = 'content_%s' % (i,)
        while self.cleaned_data.get(field_name):
            content = self.cleaned_data[field_name]
            if content in contents:
                self.add_error(field_name,'Duplicate')
            else:
                contents.add(content)
            i += 1
            field_name = 'content_%s' % (i,)
        self.cleaned_data["contents"] = contents
        
    def save(self):
        post = self.instance
        post.title = self.cleaned_data["title"]
        
        post.content_set.all().delete()
        for content in self.cleaned_data["contents"]:
            PostContent.objects.create(
                post = post,
                content = content,
            )
            
    def get_content_fields(self):
        for field_name in self.fields:
            if field_name.startswith('content_'):
                yield self[field_name]