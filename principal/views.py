from django.views.generic import ListView,View,DetailView,TemplateView
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.shortcuts import  get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic.edit import UpdateView, DeleteView,CreateView
from django.forms.models import modelformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q
from django.utils import timezone
import matplotlib.pyplot as plt
from django.urls import reverse
import io
import urllib, base64
import mplcursors
from polls.forms import EditssprincipalForm,PostForm,CommentForm,ThreadForm,MessageForm,ShareForm
from polls.models import Students,Teachers,CustomUser,principal,Post,Comment,Notification,ThreadModel,MessageModel,Image,FollowRequest
from .forms import PrincipalForm,editPrincipalForm,editsPrincipalForm,SchoolForm,EditSchoolForm
from .models import principalabout,Principalabouts,Schoolabout

@login_required
def menu(request):
    form1 = SchoolForm(request.POST)
    principals=principal.objects.get(user_id=request.user.id)
    posts = Post.objects.all().order_by('-created_on')
    form = PostForm(request.POST, request.FILES)
    files = request.FILES.getlist('image')
    share_form = ShareForm()

    if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()

            for f in files:
                img = Image(image=f)
                img.save()
                new_post.image.add(img)

            new_post.save()

    context = {
            'post_list': posts,
            'shareform': share_form,
            'profile':principals,
            'form': form,
            'forms': form1,
    }
    return render (request,'menupal.html',context)
    
@login_required
def dashboard(request):
    user = request.user
    principals = None
    teachers = None
    students = None
    if user.is_authenticated:
        if hasattr(user, 'principal'):
            principals = principal.objects.get(user=user)
        elif hasattr(user, 'teacher'):
            teachers = Teachers.objects.get(user=user)
        else:
            students = Students.objects.get(user=user)
    form = PostForm(request.POST, request.FILES)
    files = request.FILES.getlist('image')
    share_form = ShareForm()
    follow_requests = FollowRequest.objects.filter(following=request.user, accepted=False)
    follow_request_count = follow_requests.count()
    followers = FollowRequest.objects.filter(following=request.user, accepted=True).values_list('follower', flat=True)
    posts = Post.objects.filter(author__in=followers).order_by('-created_on')
    messages = MessageModel.objects.filter(receiver_user=request.user)
    notifications = Notification.objects.filter(to_user=request.user, notification_type=4, user_has_seen=False)
    threads = ThreadModel.objects.filter(Q(user=request.user) | Q(receiver=request.user))
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.author = request.user
        new_post.save()

        for f in files:
            img = Image(image=f)
            img.save()
            new_post.image.add(img)

        new_post.save()

    context = {
        'post_list': posts,
        'shareform': share_form,
        'follow_request_count': follow_request_count,
        'profile': principals or teachers or students,
        'form': form,
        'messages': messages,
        'notifications': notifications,
        'threads': threads,
        'follow_requests': follow_requests,
    }
    return render(request, 'dashboard.html', context)

@login_required
def add_principal(request):
    PrincipalaboutsFormSet = modelformset_factory(Principalabouts, form=editsPrincipalForm, extra=1)
    if request.method == 'POST':
        principalabout_form = PrincipalForm(request.POST,request.FILES)
        principalabouts_formset = PrincipalaboutsFormSet(request.POST,request.FILES, queryset=Principalabouts.objects.none())

        if principalabout_form.is_valid() and principalabouts_formset.is_valid():
            try:
                principalabout_instance = principalabout_form.save(commit=False)
                principalabout_instance.user_id = request.user.id  # assign the current user's id
                principalabout_instance.save()
                principalabouts = principalabouts_formset.save(commit=False)
                for principalabout in principalabouts:
                    principalabout.principal = principalabout_instance
                    principalabout.save()
                return redirect('hod:manage_principal', principal_id=principalabout_instance.id)
            except Exception as e:
                error_message = str(e)
                context = {'form': principalabout_form, 'principalabouts_formset': principalabouts_formset, 'error_message': error_message}
                return render(request, 'principal/principal-form.html', context)
    else:
        principalabout_form = PrincipalForm()
        principalabouts_formset = PrincipalaboutsFormSet(queryset=Principalabouts.objects.none())
        context = {'form': principalabout_form, 'formset': principalabouts_formset}
        return render(request, 'principal/principal-form.html', context)
    
def manage_principals(request, principal_id):
    try:
        principal_objs = principalabout.objects.filter(id=principal_id)
    except principalabout.DoesNotExist:
        principal_objs = None

    try:
        about = Schoolabout.objects.get(principal=principal_id)
    except Schoolabout.DoesNotExist:
        about = None

    context={
        "principals": principal_objs,
        'about': about,
    }
    return render(request,"principal/principal-detailss.html",context)

def manage_principal(request, principal_id):
    principal_obj = get_object_or_404(principalabout, id=principal_id)
    principals = principal_obj.principalabouts.all()
    context={
        "principal": principal_obj,
        "principals":principals,
    }
    return render(request,"principal/principal-details.html",context)

@login_required
def school_create(request):
    form = SchoolForm(request.POST or None)
    if form.is_valid():
        school_object = form.save(commit=False)
        school_object.user = request.user
        school_object.principal = request.user.principal
        school_object.save()
        return redirect('hod:manage_principals', principal_id=school_object.principal.id) # Use principal_id instead of about_id
    context = {
        'form': form,
        'edit_mode': False,
    }
    return render(request, "about/edit_about.html", context)

@login_required
def school_edit(request, school_id):
    school = get_object_or_404(Schoolabout, id=school_id)
    form = EditSchoolForm(request.POST or None, instance=school)
    if form.is_valid():
        principal_id = school.principal.id 
        school_object = form.save(commit=False)
        school_object.user = request.user
        school_object.principal = request.user.principal
        school_object.save()
        return redirect('hod:manage_principals', principal_id=principal_id)
    context = {
        'form': form,
        'edit_mode': True,
        'school':school
    }
    return render(request, "about/edit_about.html", context)

@login_required
def school_delete(request, school_id):
    school = get_object_or_404(Schoolabout, id=school_id)
    if request.method == "POST":
        principal_id = school.principal.id 
        school.delete()
        return redirect('hod:manage_principals', principal_id=principal_id)
    context = {'item': school}
    return render(request, "about/delete3.html", context)

def school_detail(request, about_id):
    about = Schoolabout.objects.filter(principal__user_id=about_id).first()
    context = {
        'about': about,
    }
    return render(request, 'about/detailss.html', context)

@login_required
def edit_principal(request,principal_id):
    principal_obj = get_object_or_404(principalabout, id=principal_id)
    form2=editPrincipalForm(request.POST or None,instance=principal_obj)
    PrincipalFormset = modelformset_factory(Principalabouts, form=editsPrincipalForm,extra=1,can_delete=True)
    formset = PrincipalFormset(queryset=principal_obj.principalabouts.all())
    context={
        "formset":formset,
        "form2":form2,
        "principals":principal_obj
    }
    if request.method == 'POST':
        form2=editPrincipalForm(request.POST or None,instance=principal_obj)
        formset = PrincipalFormset(request.POST or None,request.FILES or None,queryset=principal_obj.principalabouts.all())
        if form2.is_valid() and formset.is_valid():
            form2.save()
            for form in formset:
                principal_about = form.save(commit=False)
                principal_about.principal = principal_obj
                principal_about.save()
            formset.save()
        return redirect('hod:manage_principal', principal_id=principal_obj.id)
    return render(request,"principal/edit-principal.html",context)

@login_required
def deleteform(request,pk):
    principals=principalabout.objects.get(id=pk)
    if request.method == "POST":
        principal_id = principals.principal.id 
        principals.delete()
        return redirect('hod:manage_principal', principal_id=principal_id)
    context={'item':principals}
    return render(request,"principal/delete.html",context)

class PostListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.filter(author=request.user).order_by('-created_on')
        form = PostForm()
        share_form = ShareForm()

        context = {
            'post_list': posts,
            'shareform': share_form,
            'form': form,
        }

        return render(request, 'post/post_list.html', context)

    def post(self, request, *args, **kwargs):
        posts = Post.objects.filter(author=request.user).order_by('-created_on')
        form = PostForm(request.POST, request.FILES)
        files = request.FILES.getlist('image_or_video')
        share_form = ShareForm()
        if request.method == 'POST':
           form = CommentForm(request.POST)
           if form.is_valid():
            new_post = form.save(commit=False)
            new_post.post = posts
            new_post.author = request.user
            new_post.type = request.POST.get('posttype') # add type of post
            new_post.save()

            new_post.create_tags()

            for f in files:
                img = Post(image_or_video=f)
                img.save()
                new_post.image.add(img)

            new_post.save()

        context = {
            'post_list': posts,
            'shareform': share_form,
            'form': form,
        }
        return render(request, 'post/post_list.html', context)

class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        share_form = ShareForm()
        form = CommentForm()
        comments = Comment.objects.filter(post=post).order_by('-created_on')

        context = {
            'post': post,
            'form': form,
            'comments': comments,
            'shareform': share_form,
        }

        return render(request, 'post/post_detail.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)
        files = request.FILES.getlist('image_or_video')
        share_form = ShareForm()
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.post = post
                new_comment.author = request.user
                new_comment.post = post
                new_comment.type = request.POST.get('posttype') # add type of post
                new_comment.save()
            
            for f in files:
                img = Post(image_or_video=f)
                img.save()
                new_comment.image.add(img)

            new_comment.save()


        comments = Comment.objects.filter(post=post).order_by('-created_on')
        notification = Notification.objects.create(notification_type=2, from_user=request.user, to_user=post.author, post=post)

        context = {
            'post': post,
            'form': form,
            'comments': comments,
            'shareform': share_form,
        }

        return render(request, 'post/post_detail.html', context)

class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post/post_edit.html'
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('hod:post_detail', kwargs={'pk': pk})
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post/post_delete.html'
    success_url = reverse_lazy('hod:dashboard')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
def edit_comment(request, post_pk, comment_pk):
    post = get_object_or_404(Post, id=post_pk)
    comment = get_object_or_404(Comment, id=comment_pk, post=post)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('hod:post_detail', pk=post_pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'post/edit-comment.html', {'form': form})

    
class CommentReplyView(LoginRequiredMixin, View):
    def post(self, request, post_pk, pk, *args, **kwargs):
        post = Post.objects.get(pk=post_pk)
        parent_comment = Comment.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.parent = parent_comment
            new_comment.save()

        notification = Notification.objects.create(notification_type=2, from_user=request.user, to_user=parent_comment.author, comment=new_comment)

        return redirect('hod:post_detail', pk=post_pk)

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'post/comment_delete.html'

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('hod:post_detail', kwargs={'pk': pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

class AddLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            post.dislikes.remove(request.user)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            post.likes.add(request.user)
            notification = Notification.objects.create(notification_type=1, from_user=request.user, to_user=post.author, post=post, follow_request=None)

        if is_like:
            post.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class AddDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            post.likes.remove(request.user)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            post.dislikes.add(request.user)

        if is_dislike:
            post.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class AddCommentLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)

        is_dislike = False

        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            comment.dislikes.remove(request.user)

        is_like = False

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            comment.likes.add(request.user)
            notification = Notification.objects.create(notification_type=1, from_user=request.user, to_user=comment.author, comment=comment)

        if is_like:
            comment.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class AddCommentDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)

        is_like = False

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            comment.likes.remove(request.user)

        is_dislike = False

        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            comment.dislikes.add(request.user)

        if is_dislike:
            comment.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class SharedPostView(LoginRequiredMixin,View):
    def post(self, request, pk, *args, **kwargs):
       original_post = Post.objects.get(pk=pk)
       form = ShareForm(request.POST)

       if form.is_valid():
            new_post = Post(
                shared_body=self.request.POST.get('body'),
                body=original_post.body,
                post_type=original_post.post_type,
                author=original_post.author,
                created_on=original_post.created_on,
                shared_user=request.user,
                shared_on=timezone.now()
            )
            new_post.save()
            notification = Notification.objects.create(notification_type=5, from_user=request.user, to_user=original_post.author, post=original_post)

            if 'image_or_video' in request.FILES:
                image_or_video = request.FILES['image_or_video']
                # If it is a video, check and save the video file
                if image_or_video.content_type == 'video/mp4':
                    new_post.is_video = True
                    new_post.image_or_video = image_or_video
                # If it is an image, check and save the image file
                elif image_or_video.content_type.startswith('image/'):
                    new_post.is_image = True
                    new_post.image_or_video = image_or_video
            else:
                # Otherwise, use the image or video from the original post
                new_post.is_image = original_post.is_image
                new_post.is_video = original_post.is_video
                new_post.image_or_video = original_post.image_or_video

            for img in original_post.image.all():
                new_post.image.add(img)

            new_post.save()

       return redirect('hod:dashboard')


class PostNotification(LoginRequiredMixin,View):
    def get(self, request, notification_pk, post_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        post = Post.objects.get(pk=post_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('hod:post_detail', pk=post_pk)

class FollowNotification(LoginRequiredMixin,View):
    def get(self, request, notification_pk, profile_pk, *args, **kwargs):
        try:
            user = principal.objects.get(pk=profile_pk)
        except principal.DoesNotExist:
            # handle the case where no matching object is found
            return redirect('hod:dashboardfollow')

        follow_requests = FollowRequest.objects.filter(following=user.user, accepted=True)
        followers = [fr.follower for fr in follow_requests]
        notification = Notification.objects.get(pk=notification_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('hod:dashboardfollow')

class ThreadNotification(LoginRequiredMixin,View):
    def get(self, request, notification_pk, object_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        thread = ThreadModel.objects.get(pk=object_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('hod:thread', pk=object_pk)

class RemoveNotification(LoginRequiredMixin,View):
    def delete(self, request, notification_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)

        notification.user_has_seen = True
        notification.save()

        return HttpResponse('Success', content_type='text/plain')

class EditProfile(LoginRequiredMixin,View):
    def get(self, request):
        profile = principal.objects.get(user_id=request.user.id)
        form = EditssprincipalForm(instance=profile)
        return render(request, 'post/edit-profile.html', {'form': form, 'profile': profile})

    def post(self, request):
        profile = principal.objects.get(user_id=request.user.id)
        form = EditssprincipalForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('hod:profiles',pk=profile.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return render(request, 'post/edit-profile.html', {'form': form, 'profile': profile})

class ProfileView(View):
    def get(self, request,pk):
        profile= principal.objects.get(pk=pk)
        posts = Post.objects.filter(author=profile.user)
        follow_requests = FollowRequest.objects.filter(following=profile.user, accepted=True)
        followers = [fr.follower for fr in follow_requests]
        following_requests = FollowRequest.objects.filter(follower=profile.user, accepted=True)
        following = [fr.following for fr in following_requests]

        is_following = False

        if request.user in followers:
            is_following = True

        number_of_followers = len(followers)

        context = {
            'profile': profile,
            'posts': posts,
            'followers': followers,
            'number_of_followers': number_of_followers,
            'is_following': is_following,
            'following': following,
            'follow_request': follow_requests,
        }

        return render(request, 'principal/profile.html', context)

class Manage_principal(LoginRequiredMixin,View):
    def get(self, request, pk):
        profile = principal.objects.get(user=request.user, pk=pk)
        user = profile.user
        posts = Post.objects.filter(author=user)
        follow_requests = FollowRequest.objects.filter(following=profile.user, accepted=True)
        followers = [fr.follower for fr in follow_requests]

        follow_requests = FollowRequest.objects.filter(following=request.user.principal.user, accepted=False)

        is_following = False

        if request.user in followers:
            is_following = True

        number_of_followers = len(followers)

        context = {
            'profile': profile,
            'posts': posts,
            'followers': followers,
            'number_of_followers': number_of_followers,
            'is_following': is_following,
            'follow_requests': follow_requests
        }

        return render(request, 'post/profiles.html', context)

class ListFollowers(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        profile = get_object_or_404(principal, pk=pk)
        follow_requests = FollowRequest.objects.filter(following=profile.user, accepted=True)
        followers = [fr.follower for fr in follow_requests]
        following_requests = FollowRequest.objects.filter(follower=profile.user, accepted=True)
        following = [fr.following for fr in following_requests]

        context = {
            'profile': profile,
            'followers': followers,
            'following': following,
        }

        return render(request, 'followp/followers_list.html', context)
    
class AddFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = principal.objects.get(pk=pk)
        principal_follower = FollowRequest.objects.create(principal=profile, follower=request.user)
        principal_follower.save()

        return redirect('hod:profiles', pk=profile.pk)
    
class DashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        follow_requests = FollowRequest.objects.filter(follower=request.user, accepted=False)
        follow_request_count = follow_requests.count()
        # Follow requests sent by the user
        follow_requests_sent = FollowRequest.objects.filter(follower=request.user, accepted=False)

        # Follow requests received by the user
        follow_requests_received = FollowRequest.objects.filter(following=request.user, accepted=False)

        context = {
            'follow_request_count': follow_request_count,
            'follow_requests_sent': follow_requests_sent,
            'follow_requests_received': follow_requests_received,
        }

        return render(request, 'followp/dashboard.html', context)
    
class AcceptFollowRequestView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        try:
            pk = int(pk)
        except ValueError:
            return redirect('hod:dashboardfollow')

        follow_request = FollowRequest.objects.filter(following=request.user, pk=pk, accepted=False).first()
        if follow_request:
            return render(request, 'followp/follow_request.html', {'follow_request': follow_request})
        else:
            return redirect('hod:dashboardfollow')

    def post(self, request, pk, *args, **kwargs):
        try:
            pk = int(pk)
        except ValueError:
            return redirect('hod:dashboardfollow')

        follow_request = FollowRequest.objects.filter(following=request.user, pk=pk, accepted=False).first()
        if follow_request:
            if 'accept' in request.POST:
                follow_request.accepted = True
                follow_request.save()

                follower = follow_request.follower
                following = follow_request.following

                # Create notification for follower
                Notification.objects.create(
                    notification_type=3,
                    to_user=follower,
                    from_user=following,
                    follow_request=follow_request
                )
            elif 'decline' in request.POST:
                follow_request.delete()
                
            return redirect('hod:dashboardfollow')
        else:
            return redirect('hod:dashboardfollow')

class FollowProfile(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = principal.objects.get(pk=pk)
        follow_request = FollowRequest.objects.create(follower=request.user, following=profile.user)

        # Create notification for profile owner
        Notification.objects.create(
            notification_type=3,
            to_user=profile.user,
            from_user=request.user,
            follow_request=follow_request
        )

        return redirect('hod:profiles', pk=pk)

class UnfollowFollower(LoginRequiredMixin, View):
    def post(self, request, pk, follower_pk, *args, **kwargs):
        profile = get_object_or_404(principal, pk=pk)
        follower = get_object_or_404(CustomUser, pk=follower_pk)
        follow_request = FollowRequest.objects.filter(follower=follower, following=profile.user)
        if follow_request:
            follow_request.delete()

        return redirect('hod:list_followers', pk=pk) 

class UnfollowProfile(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = principal.objects.get(pk=pk)
        follow_request = FollowRequest.objects.filter(follower=request.user, following=profile.user).first()
        if follow_request:
            # Create notification for profile owner
            Notification.objects.create(
                notification_type=3,
                to_user=profile.user,
                from_user=request.user,
                follow_request=follow_request
            )
            follow_request.delete()

        return redirect('hod:profiles', pk=pk)

class ListThreads(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        threads = ThreadModel.objects.filter(Q(user=request.user) | Q(receiver=request.user))

        context = {
            'threads': threads
        }

        return render(request, 'thread/inbox.html', context)

class DeleteThread(LoginRequiredMixin,View):
    def get(self, request, pk, *args, **kwargs):
        thread = get_object_or_404(ThreadModel, pk=pk)
        thread.delete()
        messages.success(request, 'Thread deleted successfully.')
        return redirect('hod:inbox')

class CreateThread(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        form = ThreadForm()

        context = {
            'form': form
        }

        return render(request, 'thread/create_thread.html', context)

    def post(self, request, *args, **kwargs):
        form = ThreadForm(request.POST)

        username = request.POST.get('username')

        try:
            receiver = CustomUser.objects.get(username=username)
            if ThreadModel.objects.filter(user=request.user, receiver=receiver).exists():
                thread = ThreadModel.objects.filter(user=request.user, receiver=receiver)[0]
                return redirect('hod:thread', pk=thread.pk)
            elif ThreadModel.objects.filter(user=receiver, receiver=request.user).exists():
                thread = ThreadModel.objects.filter(user=receiver, receiver=request.user)[0]
                return redirect('hod:thread', pk=thread.pk)

            if form.is_valid():
                thread = ThreadModel(
                    user=request.user,
                    sender=request.user,  # set the sender as the current user
                    receiver=receiver
                    )
                thread.save()

                return redirect('hod:thread', pk=thread.pk)
        except CustomUser.DoesNotExist:
            messages.error(request, 'Invalid username')
            return redirect('hod:create-thread')


class ThreadView(LoginRequiredMixin,View):
    def get(self, request, pk, *args, **kwargs):
        form = MessageForm()
        thread = ThreadModel.objects.get(pk=pk)
        message_list = MessageModel.objects.filter(thread__pk__contains=pk)
        context = {
            'thread': thread,
            'form': form,
            'message_list': message_list,
        }

        now = timezone.now()
        message_list.filter(is_read=False).update(is_read=True, read_timestamp=now)

        return render(request, 'thread/thread.html', context)
        
class DeleteMessageView(LoginRequiredMixin,View):
    def post(self, request, pk, *args, **kwargs):
        message = get_object_or_404(MessageModel, pk=pk)
        if message.sender_user == request.user or message.receiver_user == request.user:
            message.delete()
        return redirect('hod:inbox')

class CreateMessage(LoginRequiredMixin,View):
    def post(self, request, pk, *args, **kwargs):
        form = MessageForm(request.POST, request.FILES)
        thread = ThreadModel.objects.get(pk=pk)
        if thread.receiver == request.user:
            receiver = thread.user
        else:
            receiver = thread.receiver

        if form.is_valid():
            message = form.save(commit=False)
            message.thread = thread
            message.sender_user = request.user
            message.receiver_user = receiver
            message.save()

        return redirect('hod:thread', pk=pk)
    
class PhotoListView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'photo/photos.html'
    context_object_name = 'posts'

    def get_queryset(self):
        hod_profile = principal.objects.get(user=self.request.user)
        user = hod_profile.user
        return Post.objects.filter(
        Q(image__isnull=False) | Q(image_or_video__isnull=False),
        author=user
    ).exclude(shared_user__isnull=False).order_by('-created_on')


class PhotoDetailView(LoginRequiredMixin,DetailView):
    model = Post
    template_name = 'photo/photo_detail.html'
    context_object_name = 'photo'

class PhotoDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('hod:photo')
 
class RatingChartView(LoginRequiredMixin,TemplateView):
    template_name = 'ratings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

    # Retrieve all posts
        profile = principal.objects.get(user=self.request.user)
        user = profile.user
        posts = Post.objects.filter(author=user).order_by('-created_on')

    # Create dictionary to store like and dislike counts by post type
        type_counts = {}

    # Loop through each post
        for post in posts:
        # Determine the post type and increment the count for the corresponding type
            post_type = post.post_type
            if post_type in type_counts:
                type_counts[post_type]['likes'] += post.likes.count()
                type_counts[post_type]['dislikes'] += post.dislikes.count()
            else:
                type_counts[post_type] = {
                    'likes': post.likes.count(),
                    'dislikes': post.dislikes.count()
                }

    # Sort the post types by the total number of likes and dislikes
        sorted_types = sorted(type_counts.keys(), key=lambda x: type_counts[x]['likes'] + type_counts[x]['dislikes'], reverse=True)

    # Create a list of charts to display in the template
        charts = []
        for post_type in sorted_types:
            likes = type_counts[post_type]['likes']
            dislikes = type_counts[post_type]['dislikes']

            total_votes = likes + dislikes
            like_percent = (likes / total_votes) * 100
            dislike_percent = (dislikes / total_votes) * 100

            colors = [(0, 1, 0),(1, 0, 0)]
            names = ['Likes', 'Dislikes']
            values = [like_percent, dislike_percent]

            fig, ax = plt.subplots()
            ax.axis('equal')
            _, texts, autotexts = ax.pie(values, colors=colors, labels=names, autopct='%1.1f%%',startangle=90, radius=1.2, counterclock=False, pctdistance=0.8, labeldistance=1.1, wedgeprops={'edgecolor': 'white', 'linewidth': 2}, textprops={'color': 'white', 'fontsize': 14}, shadow=True)

         # Change font size of labels and percentage values
            plt.setp(texts, size=14)
            plt.setp(autotexts, size=17)

        # Change the color of percentage values
            for autotext in autotexts:
                autotext.set_color('white')

            ax.set_title('Post Type: {} Ratings'.format(post_type))
            plt.tight_layout()

        # Add tooltip to display vote percentage
            mplcursors.cursor(autotexts).connect(
               "add",
                lambda sel: sel.annotation.set_text('{}: {:.1f}%'.format(sel.artist.get_label(), sel.target)))

            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            string = base64.b64encode(buf.read())
            uri = urllib.parse.quote(string)

            charts.append({
                'post_type': post_type,
                'image': uri,
                'likes': likes,
                'dislikes': dislikes
            })

        context['charts'] = charts
        return context
