from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils import timezone

class CustomUser(AbstractUser):
    user_type_data=((1,"Principal"),(2,"Teacher"),(3,"Student"))
    user_type=models.CharField(default=1,choices=user_type_data,max_length=10)

class School(models.Model):
    schoolname = models.CharField(max_length=200)
    profile_photo = models.ImageField(upload_to='school_photos/')
    schooltype=models.CharField(max_length=20)
    address=models.CharField(max_length=100)
    country=models.CharField(max_length=20)
    state=models.CharField(max_length=20)
    city=models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.schoolname} ({self.schooltype}), {self.address}"
    
class FollowRequest(models.Model):
    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='follower_requests')
    following = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='following_requests')
    accepted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower.username} wants to follow {self.following.username}"

class principal(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE, blank=True, null=True, related_name='principal')
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    follow_request = models.ForeignKey(FollowRequest, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='followerp')
    timestamp = models.DateTimeField(auto_now_add=True) 
    join = models.DateField(null=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    objects=models.Manager()

    def __str__(self):
        return f"{self.school}"

    def get_school(self):
        return self.school

    def get_absolute_url(self):
        return reverse("polls:loginn")

class Students(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=True, null=True, related_name='student')
    profile_photo = models.ImageField(null=True, blank=True, upload_to='Studentreg')
    principal = models.ForeignKey(principal, on_delete=models.CASCADE,related_name='studentsp')
    gender = models.CharField(max_length=10, blank=True, null=True)
    follow_request = models.ForeignKey(FollowRequest, on_delete=models.CASCADE, null=True, blank=True, related_name='followerw')
    dob = models.DateField(null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    join = models.DateField(null=True)
    separate = models.DateField(null=True)
    classs = models.CharField(max_length=20)
    section = models.CharField(max_length=20)
    rollno = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def get_school(self):
        return self.school
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
    def user_id(self):
        return self.user.id

    def get_absolute_url(self):
        return reverse("polls:loginn")
    
    def get_absolutes_url(self):
        return reverse("hod:manage_student")

    @property
    def photo_url(self):
        if self.profile_photo and hasattr(self.profile_photo, 'url'):
            return self.profile_photo.url

    def get_edit_url(self):
        return reverse("hod:edit_student", kwargs={"student_id": self.id})
    
    def get_delete_url(self):
        return reverse("hod:deleteform1", kwargs={"pk": self.id})

    def get_edits_url(self):
        return reverse("student:edit_students", kwargs={"student_id": self.id})
    
class studentabouts(models.Model):
    id=models.AutoField(primary_key=True)
    student = models.ForeignKey(Students, on_delete=models.CASCADE, related_name='studentabouts',blank=False,null=False)
    join= models.DateField(null=True)
    seperate = models.DateField(null=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='studentss')
    classs=models.CharField(max_length=20)
    section=models.CharField(max_length=20)
    rollno=models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

class Teachers(models.Model):
    id=models.AutoField(primary_key=True)
    principal = models.ForeignKey(principal, on_delete=models.CASCADE,related_name='teachersp')
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE, blank=True, null=True,related_name='teacher')
    profile_photo = models.ImageField(null=True,blank=True,upload_to='Teacherreg')
    follow_request = models.ForeignKey(FollowRequest, on_delete=models.CASCADE, null=True, blank=True, related_name='followerss')
    gender = models.CharField(max_length=10,blank=True, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    dob = models.DateField(null=True)
    join= models.DateField(null=True)
    qualification=models.CharField(max_length=10)
    seperate = models.DateField(null=True)
    classs=models.CharField(max_length=20)
    section=models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    objects=models.Manager()

    def get_school(self):
        return self.school

    def user_id(self):
        return self.user.id

    def get_absolute_url(self):
        return reverse("polls:loginn")
    
    def get_absolutes_url(self):
        return reverse("hod:manage_teacher")

    @property
    def photo_url(self):
        if self.profile_photo and hasattr(self.profile_photo, 'url'):
            return self.profile_photo.url

    def get_edit_url(self):
        return reverse("teacher:edit_teacher")
    
    def get_edits_url(self):
        return reverse("hod:edit_teacher", kwargs={"pk": self.id})
    
    def get_delete_url(self):
        return reverse("hod:deleteform2", kwargs={"pk": self.id})
    
class teacherabouts(models.Model):
    id=models.AutoField(primary_key=True)
    teacher = models.ForeignKey(Teachers, on_delete=models.CASCADE, related_name='teacherabouts',blank=False,null=False)
    join= models.DateField(null=True)
    qualification=models.CharField(max_length=10)
    seperate = models.DateField(null=True)
    school = models.ForeignKey(principal, on_delete=models.CASCADE, related_name='teacherss')
    classs=models.CharField(max_length=20)
    section=models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

class Post(models.Model):
    POST_TYPES = (
        ('Physical Learning', 'Physical Learning'),
        ('Visual Learning', 'Visual Learning'),
    )
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='posts')
    post_type = models.CharField(max_length=30, choices=POST_TYPES, default='text')
    body = models.TextField()
    image_or_video = models.FileField(upload_to='uploads/%Y/%m/%d/', blank=True)
    image = models.ManyToManyField('Image', blank=True)
    created_on = models.DateTimeField(default=timezone.now)
    shared_on = models.DateTimeField(blank=True, null=True)
    shared_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='+')
    likes = models.ManyToManyField(CustomUser, blank=True, related_name='likepol')
    dislikes = models.ManyToManyField(CustomUser, blank=True, related_name='dislikepol')
    shared_body=models.TextField(blank=True,null=True)
    
    def is_video(self):
        return self.image_or_video.name.lower().endswith('.mp4')

    def is_image(self):
        return self.image_or_video.name.lower().endswith('.jpeg') or self.image_or_video.name.lower().endswith('.jpg') or self.image_or_video.name.lower().endswith('.png')
                        
    def get_likes_url(self):
        return reverse("hod:like", kwargs={"pk": self.id})

    def get_dislikes_url(self):
        return reverse("hod:dislike", kwargs={"pk": self.id})
    
    def get_likest_url(self):
        return reverse("teacher:like", kwargs={"pk": self.id})

    def get_dislikest_url(self):
        return reverse("teacher:dislike", kwargs={"pk": self.id})
    
    def get_likess_url(self):
        return reverse("student:like", kwargs={"pk": self.id})

    def get_dislikess_url(self):
        return reverse("student:dislike", kwargs={"pk": self.id})

    def get_detail_url(self):
        return reverse("hod:post_detail", kwargs={"pk": self.id})
    
    def get_edit_url(self):
        return reverse("hod:post_edit", kwargs={"pk": self.id})
    
    def get_editt_url(self):
        return reverse("teacher:post_edit", kwargs={"pk": self.id})
    
    def get_edits_url(self):
        return reverse("student:post_edit", kwargs={"pk": self.id})
    
    def get_delete_url(self):
        return reverse("hod:post_delete", kwargs={"pk": self.id})
    
    def get_deletet_url(self):
        return reverse("teacher:post_delete", kwargs={"pk": self.id})
    
    def get_deletes_url(self):
        return reverse("student:post_delete", kwargs={"pk": self.id})
    
    def create_tags(self):
        for word in self.body.split():
            if (word[0] == '#'):
                tag = Tag.objects.filter(name=word[1:]).first()
                if tag:
                    self.tags.add(tag.pk)  
                else:
                    tag = Tag(name=word[1:])
                    tag.save()
                    self.tags.add(tag.pk)
                    self.save()

        if self.shared_body:
             for word in self.shared_body.split():
                  if (word[0] == '#'):
                    tag = Tag.objects.filter(name=word[1:]).first()
                    if tag:
                        self.tags.add(tag.pk)
                    else:
                        tag = Tag(name=word[1:])
                        tag.save()
                        self.tags.add(tag.pk)
                        self.save()
                        
    class Meta:
        ordering = ['-created_on', '-shared_on']

        
class Image(models.Model):
    image = models.FileField(upload_to='uploads/post_photos', blank=True, null=True)
    caption = models.CharField(max_length=255, blank=True)
    
class Comment(models.Model):
    comment = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE,related_name='comments')
    likes = models.ManyToManyField(CustomUser, blank=True, related_name='comment_likes')
    dislikes = models.ManyToManyField(CustomUser, blank=True, related_name='comment_dislikes')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='+')

    def get_detail_url(self):
        return reverse("hod:comment_detail", kwargs={"pk": self.id})  
    
    @property
    def children(self):
            return Comment.objects.filter(parent=self).order_by('-created_on').all()
    
    @property
    def is_parent(self):
            if self.parent is None:
                    return True
            return False

class Notification(models.Model):
	# 1 = Like, 2 = Comment, 3 = Follow, #4 = DM
    notification_type = models.IntegerField()
    to_user = models.ForeignKey(CustomUser, related_name='notification_to', on_delete=models.CASCADE, null=True)
    from_user = models.ForeignKey(CustomUser, related_name='notification_from', on_delete=models.CASCADE, null=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    user_has_seen = models.BooleanField(default=False)
    follow_request = models.ForeignKey(FollowRequest, on_delete=models.CASCADE, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('hod:profiles', args=[self.follow_request.following.pk])
    
class ThreadModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='threads')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='send_threads')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_threads')
    is_read = models.BooleanField(default=False)
    read_timestamp = models.DateTimeField(blank=True, null=True)

class MessageModel(models.Model):
    thread = models.ForeignKey(ThreadModel, related_name='messages', on_delete=models.CASCADE, blank=True, null=True)
    sender_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    body = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='uploads/message_photos', blank=True, null=True)
    is_read = models.BooleanField(default=False)
    read_timestamp = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.body} ({self.sender_user} -> {self.receiver_user})"

class Tag(models.Model):
	name = models.CharField(max_length=255) 
