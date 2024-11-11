from django.shortcuts import render

from core.models import Course, Job, Region

# Create your views here.
def index(request):
    template = "frontend/landing.html"
    args = {}
    return render(request,template,args)


def register(request):
    template = "frontend/signup.html"
    args = {}
    return render(request,template,args)


def login(request):
    template = "frontend/login.html"
    args = {}
    return render(request,template,args)


# members
def dashboard_profile(request):
    template = "frontend/members/dashboard-profile.html"
    args = {}
    args["regions"] = Region.objects.all()
    return render(request,template,args)


def dashboard_courses(request):
    template = "frontend/members/dashboard-courses.html"
    args = {}
    args["courses"] = Course.objects.all()
    return render(request,template,args)


def dashboard_course(request,id):
    course = Course.objects.get(id=id)
    template = "frontend/members/dashboard-chapter.html"
    args = {}
    args["course"] = course
    first_chapter = course.chapters.first()
    args["first_chapter"] = first_chapter
    return render(request,template,args)

def dashboard_jobs(request):
    template = "frontend/members/dashboard-jobs.html"
    args = {}
    args["jobs"] = Job.objects.filter(is_active=True)
    return render(request,template,args)

def job(request,id):
    template = "frontend/job.html"
    job = Job.objects.get(id=id)
    args = {}
    args["job"] = job
    return render(request,template,args)