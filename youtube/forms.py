from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import DownloadTask,fileCreation,processdownload
class DownloadTaskforms(forms.ModelForm):
    class Meta:
        model=DownloadTask
        fields=['name','link','image','user']
        widget= {
            'image': forms.ClearableFileInput(attrs= {"rows":4,"class":"form-control-file"}),
            'user': forms.Textarea(attrs= {"rows":5,"class":"form-control-file"}),
            'link': forms.TextInput(attrs= {"class": "form_control"})
                }
                                          
class fileCreationforms(forms.ModelForm):
        class Meta:
            model= fileCreation
            fields=['name','link','image','title','errormessage','file_path']
            widget= {
        
            'name': forms.TextInput(attrs= {"class": "form_control"}),
            'link': forms.TextInput(attrs= {"class": "form_control"}),
            'image': forms.ClearableFileInput(attrs= {"rows":4,"class":"form-control-file"}),
            'title': forms.TextInput(attrs= {"class": "form_control"}),
            'errormessage': forms.Textarea(attrs= {"class": "form_control"}),
            'file_path': forms.TextInput(attrs= {"class": "form_control"})
                                                                                    
                }
                                          
        def clean_errormessage(self):
            errormessage = self.cleaned_data.get ("errormessage")

            if fileCreationforms.objects.filter(errormessage=errormessage,paid=False).exists():
                raise forms.ValidationError("Hata mesaji verir")
            return errormessage

class processdownloadforms(forms.ModelForm):
        model= processdownload
        fields=['created','updated','session_key']
        widget= {
        
        'created': forms.TextInput(attrs= {"class": "form_control"}),
        'updated': forms.TextInput(attrs= {"class": "form_control"}),
        'session_key': forms.Textarea(attrs= {"class": "form_control"})

        }
