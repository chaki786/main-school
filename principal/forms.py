from django import forms
from .models import principalabout,Schoolabout,Principalabouts

class DateInput(forms.DateInput):
    input_type = "date"

gender_choice=(
        ("Male","Male"),
        ("Female","Female")
    )
    
my_study=(
        ('',''),
        ('10th Class','10th Class'),
        ('12th Class','12th Class'),
        ('B.A.','B.A.'),
        ('BCA','BCA'),
        ('BBA','BBA'),
        ('B.Tech','B.Tech'),
        ('B.Com','B.Com'),
        ('B.Ed','B.Ed'),
        ('MBA','MBA'),
        ('MCA','MCA'),
        ('M.Tech','M.Tech'),
        ('M.A.','M.A.'),
        ('M.Com','M.Com'),
        ('M.Ed','M.Ed'),
        ('Ph.D','Ph.D'),
        )

class PrincipalForm(forms.ModelForm):
    dob = forms.DateField(required=False, 
                           widget=forms.SelectDateWidget(years=range(1960, 2050)))
    join = forms.DateField(required=False, 
                           widget=forms.SelectDateWidget(years=range(1960, 2050)))
    seperate = forms.DateField(required=False, 
                           widget=forms.SelectDateWidget(years=range(1960, 2050)))
    to = forms.DateField(required=False, 
                           widget=forms.SelectDateWidget(years=range(1960, 2050)))
    from1 = forms.DateField(required=False, 
                           widget=forms.SelectDateWidget(years=range(1960, 2050)))
    class Meta:
        model=principalabout
        fields =['cname','fname','lname','dob','gender','qualification','from1','to', 'profile_photo','seperate','join']

class editPrincipalForm(forms.ModelForm):
    dob = forms.DateField(required=False, 
                           widget=forms.SelectDateWidget(years=range(1960, 2050)))
    join = forms.DateField(required=False, 
                           widget=forms.SelectDateWidget(years=range(1960, 2050)))
    seperate = forms.DateField(required=False, 
                           widget=forms.SelectDateWidget(years=range(1960, 2050)))
    to = forms.DateField(required=False, 
                           widget=forms.SelectDateWidget(years=range(1960, 2050)))
    from1 = forms.DateField(required=False, 
                           widget=forms.SelectDateWidget(years=range(1960, 2050)))
    fname=forms.CharField(max_length=50,widget=forms.TextInput)
    lname=forms.CharField(max_length=50,widget=forms.TextInput)
    cname=forms.CharField(max_length=50,widget=forms.TextInput)
    gender=forms.ChoiceField(choices=gender_choice,widget=forms.Select)
    qualification=forms.ChoiceField(choices=my_study,widget=forms.Select)
    profile_photo=forms.FileField(max_length=150,widget=forms.FileInput,required=False)
    class Meta:
        model=principalabout
        fields =['cname','fname','lname','dob','gender','qualification','from1','to', 'profile_photo','seperate','join']

class editsPrincipalForm(forms.ModelForm):
    to = forms.DateField(required=False, 
                           widget=forms.SelectDateWidget(years=range(1960, 2050)))
    from1 = forms.DateField(required=False, 
                           widget=forms.SelectDateWidget(years=range(1960, 2050)))
    qualification=forms.ChoiceField(choices=my_study,widget=forms.Select)
    cname=forms.CharField(max_length=50,widget=forms.TextInput)
    class Meta:
        model=Principalabouts
        fields =['qualification','from1','to','cname']

class SchoolForm(forms.ModelForm):
    content= forms.TextInput()
    class Meta:
        model= Schoolabout
        fields= ['content']

class EditSchoolForm(forms.ModelForm):
    content= forms.TextInput()
    class Meta:
        model= Schoolabout
        fields= ['content']

    