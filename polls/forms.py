from django import forms
from .models import School, Students,Teachers,principal,studentabouts,teacherabouts,Post,MessageModel,Comment

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
        )

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['schoolname', 'profile_photo','schooltype','country','city','state','address']

class principalregForm(forms.ModelForm):
    join = forms.DateField(required=False, 
                           widget=forms.SelectDateWidget(years=range(1960, 2050)))
    email = forms.EmailField()
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model=principal
        fields =['username','password','email','join','school']

class EditssprincipalForm(forms.ModelForm):
    join = forms.DateField(required=False, 
                           widget=forms.SelectDateWidget(years=range(1960, 2050)))
    class Meta:
        model=principal
        fields =['join','school']

class studentregForm(forms.ModelForm):
    email = forms.EmailField()
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    dob = forms.DateField(required=False, 
                           widget=forms.SelectDateWidget(years=range(1960, 2050)))
    join = forms.DateField(required=False, 
                           widget=forms.SelectDateWidget(years=range(1960, 2050)))
    seperate = forms.DateField(required=False, 
                           widget=forms.SelectDateWidget(years=range(1960, 2050)))
    principal = forms.ModelChoiceField(queryset=principal.objects.all())
    class Meta:
        model=Students
        fields =['principal','username','password','email','first_name','last_name','dob','join','seperate','gender','classs','section', 'rollno','profile_photo']

class editStudentForm(forms.ModelForm):
    dob = forms.DateField(required=False, 
                           widget=forms.SelectDateWidget(years=range(1960, 2050)))
    join = forms.DateField(required=False, 
                           widget=forms.SelectDateWidget(years=range(1960, 2050)))
    seperate = forms.DateField(required=False, 
                           widget=forms.SelectDateWidget(years=range(1960, 2050)))
    classs=forms.CharField(max_length=50,widget=forms.TextInput)
    section=forms.CharField(max_length=50,widget=forms.TextInput)
    rollno=forms.CharField(max_length=50,widget=forms.TextInput)
    profile_photo=forms.FileField(max_length=150,widget=forms.FileInput,required=False)
    class Meta:
        model=Students
        fields =['profile_photo','classs','section','rollno','join','seperate','principal']

class editsStudentForm(forms.ModelForm):
    join = forms.DateField(required=False, 
                           widget=forms.SelectDateWidget(years=range(1960, 2050)))
    seperate = forms.DateField(required=False, 
                           widget=forms.SelectDateWidget(years=range(1960, 2050)))
    classs=forms.CharField(max_length=50,widget=forms.TextInput)
    section=forms.CharField(max_length=50,widget=forms.TextInput)
    rollno=forms.CharField(max_length=50,widget=forms.TextInput)
    class Meta:
        model=studentabouts
        fields =['classs','section','rollno','join','seperate']

class editssStudentForm(forms.ModelForm):
    dob = forms.DateField(required=False, 
                           widget=forms.SelectDateWidget(years=range(1960, 2050)))
    join = forms.DateField(required=False, 
                           widget=forms.SelectDateWidget(years=range(1960, 2050)))
    seperate = forms.DateField(required=False, 
                           widget=forms.SelectDateWidget(years=range(1960, 2050)))
    classs=forms.CharField(max_length=50,widget=forms.TextInput)
    section=forms.CharField(max_length=50,widget=forms.TextInput)
    rollno=forms.CharField(max_length=50,widget=forms.TextInput)
    profile_photo=forms.FileField(max_length=150,widget=forms.FileInput,required=False)
    class Meta:
        model=Students
        fields =['profile_photo','classs','section','rollno','join','seperate']

class TeacherregForm(forms.ModelForm):
    email = forms.EmailField()
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    to = forms.DateField(required=False, 
                           widget=forms.SelectDateWidget(years=range(1960, 2050)))
    dob = forms.DateField(required=False, 
                           widget=forms.SelectDateWidget(years=range(1960, 2050)))
    join = forms.DateField(required=False, 
                           widget=forms.SelectDateWidget(years=range(1960, 2050)))
    seperate = forms.DateField(required=False, 
                           widget=forms.SelectDateWidget(years=range(1960, 2050)))
    principal = forms.ModelChoiceField(queryset=principal.objects.all())
    class Meta:
        model=Teachers
        fields =['principal','username','password','email','first_name','last_name','dob','join','seperate','gender','classs','section','profile_photo']

class editTeacherForm(forms.ModelForm):
    join = forms.DateField(required=False, 
                           widget=forms.SelectDateWidget(years=range(1960, 2050)))
    seperate = forms.DateField(required=False, 
                           widget=forms.SelectDateWidget(years=range(1960, 2050)))
    classs=forms.CharField(max_length=50,widget=forms.TextInput)
    section=forms.CharField(max_length=50,widget=forms.TextInput)
    qualification=forms.ChoiceField(choices=my_study,widget=forms.Select)
    profile_photo=forms.FileField(max_length=150,widget=forms.FileInput,required=False)
    class Meta:
        model=Teachers
        fields =['qualification','profile_photo','classs','section','join','seperate','principal']

class editsTeacherForm(forms.ModelForm):
    join = forms.DateField(required=False, 
                           widget=forms.SelectDateWidget(years=range(1960, 2050)))
    seperate = forms.DateField(required=False, 
                           widget=forms.SelectDateWidget(years=range(1960, 2050)))
    classs=forms.CharField(max_length=50,widget=forms.TextInput)
    class Meta:
        model=teacherabouts
        fields =['classs','join','seperate']

class editssTeacherForm(forms.ModelForm):
    to = forms.DateField(required=False, 
                           widget=forms.SelectDateWidget(years=range(1960, 2050)))
    from1 = forms.DateField(required=False, 
                           widget=forms.SelectDateWidget(years=range(1960, 2050)))
    join = forms.DateField(required=False, 
                           widget=forms.SelectDateWidget(years=range(1960, 2050)))
    seperate = forms.DateField(required=False, 
                           widget=forms.SelectDateWidget(years=range(1960, 2050)))
    classs=forms.CharField(max_length=50,widget=forms.TextInput)
    section=forms.CharField(max_length=50,widget=forms.TextInput)
    qualification=forms.ChoiceField(choices=my_study,widget=forms.Select)
    profile_photo=forms.FileField(max_length=150,widget=forms.FileInput,required=False)
    class Meta:
        model=Teachers
        fields =['to','from1','qualification','profile_photo','classs','section','join','seperate']

class PostForm(forms.ModelForm):
    body = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': '5',
            'cols':'60',
            'placeholder': 'Say Something...'
            }))
    post_type = forms.ChoiceField(choices=Post.POST_TYPES)
    image_or_video = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        required=False)

    class Meta:
        model = Post
        fields = ['body', 'post_type','image_or_video']
    

class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={'rows': '1',
                   'placeholder': 'Add Comment...'}
        ))

    class Meta:
        model = Comment
        fields = ['comment']

class ThreadForm(forms.Form):
    username = forms.CharField(label='', max_length=100)

class MessageForm(forms.ModelForm):
    body = forms.CharField(label='', max_length=1000)

    image = forms.ImageField(required=False)

    class Meta:
        model = MessageModel
        fields = ['body', 'image']

class ShareForm(forms.Form):
    body = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': '3',
            'placeholder': 'Say Something...'
            }))
