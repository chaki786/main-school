from django.contrib.auth import logout,login
from django.views.generic import ListView,View,DetailView,TemplateView
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .EmailBackEnd import EmailBackEnd
from django.db.models import Q
import matplotlib.pyplot as plt
from django.shortcuts import  get_object_or_404
from django.urls import reverse
from django.db.models import Avg
import io
import urllib, base64
import mplcursors
from principal.models import principalabout,Schoolabout
from .models import CustomUser,Students,Teachers,principal,Post,Comment,School,FollowRequest
from .forms import studentregForm,TeacherregForm,principalregForm,ShareForm,CommentForm,SchoolForm
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, F,Sum

class HomeView (ListView):
    def get(self, request):
        return render (self.request,'index.html')
    
class AddFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = CustomUser.objects.get(pk=pk)
        profile.followers.add(request.user)

        return redirect('student:manage_student', pk=profile.pk)

class RemoveFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = CustomUser.objects.get(pk=pk)
        profile.followers.remove(request.user)

        return redirect('student:manage_student', pk=profile.pk)
    
class ListFollowers(View):
    def get(self, request, pk, *args, **kwargs):
        profile = CustomUser.objects.get(pk=pk)
        followers = profile.followers.all()

        if len(followers) == 0:
            is_following = False

        for follower in followers:
            if follower == request.user:
                is_following = True
                break
            else:
                is_following = False

        number_of_followers = len(followers)

        context = {
            'profile': profile,
            'followers': followers,
            'number_of_followers': number_of_followers,
            'is_following': is_following
        }

        return render(request, 'follow/followers_list.html', context)

class Menu(ListView):
    def get(self, request, school_id):
        schools = School.objects.filter(id=school_id)
        principals = principal.objects.filter(school__id=school_id)
        posts = Post.objects.filter(Q(author__principal__school=school_id) |
                                    Q(author__teacher__principal=school_id) |
                                    Q(author__student__principal=school_id)).select_related('author')
        context = {
            'schools': schools,
            'principals': principals,
            'post_list': posts,
        }
        return render(self.request, 'menu.html', context)

def calculate_avg_rating(school_name, principal):
    try:
        school = School.objects.get(schoolname=school_name)
    except ObjectDoesNotExist:
        return None  # or some other value to indicate that the school was not found
    
    posts = Post.objects.filter(Q(author__principal__school=principal) |
                                Q(author__teacher__principal__school=school) |
                                Q(author__student__principal__school=school)).select_related('author')
    return posts.aggregate(Avg('rating'))['rating__avg']

class Menus(ListView):
    template_name = 'menus.html'
    model = School
    context_object_name = 'schools'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(schoolname__icontains=search_query) | 
                Q(schooltype__icontains=search_query) |
                Q(address__icontains=search_query) |
                Q(country__icontains=search_query) |
                Q(state__icontains=search_query) |
                Q(city__icontains=search_query)
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get all the principals from the database
        principals = principal.objects.all()

        # Calculate the average rating for each school and add it to the context
        schools = context['schools']
        for school in schools:
            for principalss in principals:
                if principalss.school == school:
                    school.avg_rating = calculate_avg_rating(school, principalss)
                    break
            # Get all posts for the school and annotate them with like percentage
            posts = Post.objects.filter(Q(author__principal__school=school) |
                                         Q(author__teacher__principal__school=school) |
                                         Q(author__student__principal__school=school)).annotate(
                                             num_likes=Count('likes'),
                                             num_dislikes=Count('dislikes')
                                         ).annotate(
                                             like_percentage=F('num_likes') / (F('num_likes') + F('num_dislikes')) * 100
                                         )
            school.posts = posts

         # Calculate the average like percentage for all posts of the school
            school.avg_like_percentage = posts.aggregate(avg_like_percentage=Avg('like_percentage'))['avg_like_percentage'] or 0

        # Sort the schools by their average like percentage in descending order
        schools = sorted(schools, key=lambda s: s.avg_like_percentage, reverse=True)

    # Loop through the sorted schools and add a ranking attribute to each school
        for i, school in enumerate(schools):
            school.ranking = i + 1

        total_likes = Post.objects.aggregate(num_likes=Sum('likes'), num_dislikes=Sum('dislikes'))
        context['total_like_percentage'] = round((total_likes['num_likes'] or 0) / ((total_likes['num_likes'] or 0) + (total_likes['num_dislikes'] or 0)) * 100)


        context['schools'] = schools
        return context
    
def add_school(request):
    if request.method == "POST":
        form = SchoolForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('polls:principal_reg')
    else:
        form = SchoolForm()
    return render(request, 'add_school.html', {'form2': form})

def principalreg(request):
    if request.method == "POST":
        form = principalregForm(request.POST , request.FILES)
        if form.is_valid():
            # create user and student objects
            user = CustomUser.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
                user_type=1,
            )
            schoolname=form.cleaned_data['school']
            principals = principal.objects.create(
                user=user,
                school=schoolname,
                join=form.cleaned_data['join'],
            )
            messages.success(request,"Successfully Added Principal Register")
            return redirect(reverse("polls:loginn"))
    else:
        form=principalregForm()
    return render (request,"hod_register.html",context={"form":form})

def manage_principals(request, principal_id):
    principal_objs = principalabout.objects.filter(user_id=principal_id)
    school_obj = Schoolabout.objects.filter(principal__user_id=principal_id).first()
    context={
        "about": school_obj,
        "principalss": principal_objs,
    }
    return render(request,"principal/principal-detail.html",context)

def manage_principal(request, principal_id):
    principal_obj = get_object_or_404(principalabout, id=principal_id)
    principals = principal_obj.principalabouts.all()
    context={
        "principal": principal_obj,
        "principals":principals,
    }
    return render(request,"principal/principal-detailssw.html",context)

def teacherreg(request):
    if request.method == "POST":
        form = TeacherregForm(request.POST, request.FILES)
        if form.is_valid():
            # create user and teacher objects
            user = CustomUser.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
                last_name=form.cleaned_data['last_name'],
                first_name=form.cleaned_data['first_name'],
                user_type=2,
            )
            principal = form.cleaned_data['principal']
            teacher = Teachers.objects.create(
                user=user,
                principal=principal,
                last_name=form.cleaned_data['last_name'],
                first_name=form.cleaned_data['first_name'],
                profile_photo=form.cleaned_data['profile_photo'],
                gender=form.cleaned_data['gender'],
                dob=form.cleaned_data['dob'],
                classs=form.cleaned_data['classs'],
                section=form.cleaned_data['section'],
                join=form.cleaned_data['join'],
            )
            messages.success(request, "Successfully added teacher registration")
            return redirect(reverse("polls:loginn"))
    else:
        form = TeacherregForm()
    return render(request, 'teacher register.html', {'form': form})

def manage_teacher(request, principal_id):
    teachers = Teachers.objects.filter(principal__user_id=principal_id)
    return render(request, "teacher/teacher-detail.html", {"teachers": teachers})

def studentreg(request):
    if request.method == "POST":
        form = studentregForm(request.POST, request.FILES)
        if form.is_valid():
            # create user and principal objects
            user = CustomUser.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
                last_name=form.cleaned_data['last_name'],
                first_name=form.cleaned_data['first_name'],
                user_type=3,
            )
            principal = form.cleaned_data['principal']
            student = Students.objects.create(
                user=user,
                principal=principal,
                last_name=form.cleaned_data['last_name'],
                rollno=form.cleaned_data['rollno'],
                first_name=form.cleaned_data['first_name'],
                profile_photo=form.cleaned_data['profile_photo'],
                gender=form.cleaned_data['gender'],
                dob=form.cleaned_data['dob'],
                classs=form.cleaned_data['classs'],
                section=form.cleaned_data['section'],
                join=form.cleaned_data['join'],
            )
            messages.success(request, "Successfully added student registration.")
            return redirect(reverse("polls:loginn"))
    else:
        form = studentregForm()
    return render(request, "student register.html", {'form': form})

def manage_student(request,principal_id):
    students = Students.objects.filter(principal__user_id=principal_id)
    return render(request,"student/student-detail.html",{"students":students})

def loginn(request):
    if request.method=="POST":
        user=EmailBackEnd.authenticate(request,username=request.POST.get("username"),password=request.POST.get("password"))
        if user is not None:
            login(request, user)
            if user.user_type=="1":
                return redirect("hod:dashboard")
            elif user.user_type=="2":
                return redirect("teacher:dashboard")
            else:
                return redirect("student:dashboard")
        else:
            messages.error(request,"Invalid username or password.")
            return redirect("polls:loginn")
    return render(request, 'login.html')

@login_required
def logouts(request):
    if request.method == 'POST':
        logout(request)
        return redirect("polls:home")
    return render(request,"logout.html")

class PostListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        share_form = ShareForm()

        context = {
            'post_list': posts,
            'shareform': share_form,
        }

        return render(request, 'postpol/post_list.html', context)

class PostDetailView( View):
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

        return render(request, 'postpol/post_detail.html', context)
    
class PhotoListView(ListView):
    model = Post
    template_name = 'photopol/photospol.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_id = self.kwargs['school_id']
        posts = Post.objects.filter(Q(author__principal__school=school_id) |
                                    Q(author__teacher__principal=school_id) |
                                    Q(author__student__principal=school_id)).exclude(shared_user__isnull=False).select_related('author')
        context['posts'] = posts
        return context

class PhotoDetailView(DetailView):
    model = Post
    template_name = 'photopol/photo_details.html'
    context_object_name = 'photo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.object
        return context
    
class ListFollowers(View):
    def get(self, request, pk, *args, **kwargs):
        profile = get_object_or_404(principal, pk=pk)
        follow_requests = FollowRequest.objects.filter(following=profile.user, accepted=True)
        followers = [fr.follower for fr in follow_requests]

        context = {
            'profile': profile,
            'followers': followers,
        }

        return render(request, 'followp/followers_lists.html', context)

class FollowToggle(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = principal.objects.get(pk=pk)
        follow_request = FollowRequest.objects.filter(follower=request.user, following=profile.user)

        if follow_request.exists():
            follow_request.delete()  # unfollow
        else:
            FollowRequest.objects.create(follower=request.user, following=profile.user)  # follow

        return redirect(reverse('hod:profile', args=[pk]))
    
class ListFollowerss( View):
    def get(self, request, pk, *args, **kwargs):
        profile = get_object_or_404(Students, pk=pk)
        follow_requests = FollowRequest.objects.filter(following=profile.user, accepted=True)
        followers = [fr.follower for fr in follow_requests]

        context = {
            'profile': profile,
            'followers': followers,
        }

        return render(request, 'followstud/followers_lists.html', context)
    
class FollowToggles(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        student = Students.objects.get(pk=pk)
        follow_request = FollowRequest.objects.filter(follower=request.user, following=student.user)

        if follow_request.exists():
            follow_request.delete()  # unfollow
        else:
            FollowRequest.objects.create(follower=request.user, following=student.user)  # follow

        return redirect('student:profile', student_id=pk)
    
class ListFollowerst(View):
    def get(self, request, pk, *args, **kwargs):
        profile = get_object_or_404(Teachers, pk=pk)
        follow_requests = FollowRequest.objects.filter(following=profile.user.teacher.user, accepted=True)
        followers = [fr.follower for fr in follow_requests]

        context = {
            'profile': profile,
            'followers': followers,
        }

        return render(request, 'followteach/followers_lists.html', context)
    
class FollowTogglet(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = Teachers.objects.get(pk=pk)
        follow_request = FollowRequest.objects.filter(follower=request.user, following=profile.user)

        if follow_request.exists():
            follow_request.delete()  # unfollow
        else:
            FollowRequest.objects.create(follower=request.user, following=profile.user)  # follow

        return redirect('teacher:profile', pk=pk)

class RatingChartView(TemplateView):
    template_name = 'ratingpol.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        school_id = self.kwargs['school_id']

        # Retrieve posts from Menu view
        posts = Post.objects.filter(Q(author__principal__school=school_id) |
                                    Q(author__teacher__principal=school_id) |
                                    Q(author__student__principal=school_id)).select_related('author')

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

        context['school_id'] = school_id
        context['charts'] = charts
        return context