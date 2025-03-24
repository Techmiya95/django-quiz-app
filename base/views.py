from django.shortcuts import render
from django.contrib.auth.models import User
from account.models import Profile
from quizes.models import UserRank, Quiz, QuizSubmission, Question
from django.contrib.auth.decorators import login_required, user_passes_test
import datetime


def home(request):
    

    leaderboard_users = UserRank.objects.order_by('rank')[:4]

    if request.user.is_authenticated:
        user_object = User.objects.get(username=request.user)

        # Use .filter().first() to avoid "DoesNotExist" error
        user_profile = Profile.objects.filter(user=user_object).first()

        context = {"user_profile": user_profile, "leaderboard_users":leaderboard_users}


    else:
        context = {"leaderboard_users":leaderboard_users}
    return render(request, "welcome.html", context)



@login_required(login_url="login")
def leaderboard_view(request):
    leaderboard_users = UserRank.objects.order_by('rank')

    user_object = User.objects.get(username=request.user)

        # Use .filter().first() to avoid "DoesNotExist" error
    user_profile = Profile.objects.filter(user=user_object).first()
    context = {"leaderboard_users":leaderboard_users, "user_profile": user_profile}

    return render(request,"leaderboard.html", context)


def is_superuser(user):
    return user.is_superuser


@user_passes_test(is_superuser)
@login_required(login_url='login')
def dashboard_view(request):
    user_object =User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user=user_object)


    total_users = User.objects.all().count()
    total_quizzes = Quiz.objects.all().count()
    total_quiz_submit = QuizSubmission.objects.all().count()
    total_questions = Question.objects.all().count()


    today_users = User.objects.filter(date_joined__date=datetime.date.today()).count()
    today_quizzes_objs = Quiz.objects.filter(created_at__date=datetime.date.today())
    today_quizzes = Quiz.objects.filter(created_at__date=datetime.date.today()).count()
    today_quiz_submit = QuizSubmission.objects.filter(submitted_at__date=datetime.date.today()).count()
    today_questions = 0


    context = {"user_profile":user_profile, 
               "total_users":total_users,
               "total_quizzes":total_quizzes,
               "total_quiz_submit":total_quiz_submit,
               "total_questions":total_questions,
               "today_users":today_users,
                "today_quizzes":today_quizzes,
                "today_quiz_submit":today_quiz_submit,
                "today_questions":today_questions,}
    return render(request, "dashboard.html", context)