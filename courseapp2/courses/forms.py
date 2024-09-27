from django import forms

from courses.models import Course
from django.forms import SelectMultiple, TextInput, Textarea

# class CourseCreateForm(forms.Form):

#     title = forms.CharField(
#         label="Kurs başlığı",
#         required=True, 
#         error_messages={"required": "kurs başlığı girmelisiniz"},
#         widget=forms.TextInput(attrs={"class": "form-control"})
#     )
#     description = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control"}))
#     imageUrl = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
#     slug = forms.SlugField(widget=forms.TextInput(attrs={"class": "form-control"}))


class CourseCreateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('title','description','image','slug')#'__all__' hepsini getirir
        labels = {
            "title":"başlık",
            "description":"açıklama",
        }
        widgets = {
            "title": TextInput(attrs={"class":"form-control"}),
            "description":Textarea(attrs={"class":"form-control"}),
            "slug":TextInput(attrs={"class":"form-control"}),
        }
        error_messages = {
            "title":{
                "required": "kurs başlığı girmelisiniz",
                "max_legth":"maksimum 50 karakter girmelisiniz"
            },
            "description":{
                "required":"Kurs açıklaması zorunludur"
            }
        }

class CourseEditForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('title','description','image','slug','categories','isActive')
        labels = {
            "title":"başlık",
            "description":"açıklama",
        }
        widgets = {
            "title": TextInput(attrs={"class":"form-control"}),
            "description": Textarea(attrs={"class":"form-control"}),
            "slug": TextInput(attrs={"class":"form-control"}),
            "categoris": SelectMultiple(attrs={"class":"form-control"})
        }
        error_messages = {
            "title":{
                "required": "kurs başlığı girmelisiniz",
                "max_legth":"maksimum 50 karakter girmelisiniz"
            },
            "description":{
                "required":"Kurs açıklaması zorunludur"
            }
        }


class UploadForm(forms.Form):
    image=forms.ImageField()
