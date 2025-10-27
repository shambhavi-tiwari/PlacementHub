from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.contrib import messages
from .threads import *
from .models import *
from .utils import *
import xlrd

context = {}

# ==============================
# HOME & ABOUT
# ==============================
def home_page(request):
    return render(request, "main/home.html")


def about_page(request):
    return render(request, "main/about.html")


# ==============================
# STUDENT LOGIN
# ==============================
def student_login(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')

            student_obj = StudentModel.objects.filter(email=email).first()
            if student_obj is None:
                messages.info(request, 'User does not exist. Please sign up.')
                return redirect('student-login')

            user = authenticate(username=email, password=password)
            if user is None:
                messages.info(request, 'Incorrect password.')
                return redirect('student-login')

            login(request, user)
            messages.success(request, 'Student logged in successfully.')
            return redirect('student-dashboard')

    except Exception as e:
        print(f"Student login error: {e}")

    return render(request, "accounts/student-login.html")


# ==============================
# TPO LOGIN
# ==============================
def tpo_login(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')

            teacher_obj = TeacherModel.objects.filter(email=email).first()
            if teacher_obj is None:
                messages.info(request, 'TPO user does not exist.')
                return redirect('tpo-login')

            user = authenticate(username=email, password=password)
            if user is None:
                messages.info(request, 'Incorrect password.')
                return redirect('tpo-login')

            login(request, user)
            messages.success(request, 'TPO logged in successfully.')
            return redirect('tpo-dashboard')

    except Exception as e:
        print(f"TPO login error: {e}")

    return render(request, "accounts/tpo-login.html")


# ==============================
# STUDENT DASHBOARD & PROFILE
# ==============================
@login_required(login_url='/student-login/')
def student_dashboard(request):
    try:
        student = StudentModel.objects.get(email=request.user)
        context = {'student': student}
        return render(request, "student/dashboard.html", context)
    except Exception as e:
        print(f"Student dashboard error: {e}")
        messages.error(request, "Unable to load student dashboard.")
        return redirect('student-login')


@login_required(login_url='/student-login/')
def student_profile(request):
    context["user"] = StudentModel.objects.get(email=request.user)
    return render(request, "student/profile.html", context)


@login_required(login_url='/student-login/')
def update_student_profile(request):
    try:
        user = StudentModel.objects.get(email=request.user)
        if request.method == 'POST':
            user.resume = request.FILES.get('resume', user.resume)
            user.headshot = request.FILES.get('headshot', user.headshot)
            user.linkedIn_link = request.POST.get("linkedIn_link", user.linkedIn_link)
            user.gitHub_link = request.POST.get("gitHub_link", user.gitHub_link)
            user.bio = request.POST.get("bio", user.bio)
            user.skills = request.POST.get("skills", user.skills)
            user.save()
            messages.success(request, "Profile updated successfully.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        print(f"Profile update error: {e}")
        messages.error(request, "Error updating profile.")
    return render(request, "student/profile.html", context)


# ==============================
# TPO DASHBOARD & STUDENT DATA
# ==============================
@login_required(login_url='/tpo-login/')
def tpo_dashboard(request):
    try:
        tpo = TeacherModel.objects.get(email=request.user)
        students = StudentModel.objects.all()
        context = {'tpo': tpo, 'students': students}
        return render(request, "tpo/dashboard.html", context)
    except Exception as e:
        print(f"TPO dashboard error: {e}")
        messages.error(request, "Unable to load TPO dashboard.")
        return redirect('tpo-login')


@login_required(login_url='/tpo-login/')
def add_student_data(request):
    try:
        if request.method == 'POST':
            file_obj = FileSavingModel.objects.create(file=request.FILES['file'])
            path = str(file_obj.file.path)
            workbook = xlrd.open_workbook(path)
            sheet = workbook.sheet_by_index(0)
            for row in range(1, sheet.nrows):
                name = str(sheet.cell_value(row, 0))
                email = str(sheet.cell_value(row, 1)).lower()
                phone = sheet.cell_value(row, 2)
                pw = get_random_string(8)
                org = StudentModel.objects.create(
                    name=name,
                    email=email,
                    phone=phone
                )
                org.set_password(pw)
                org.save()
                thread_obj = send_credentials_mail(email, pw)
                thread_obj.start()
            messages.success(request, "Student data uploaded successfully.")
    except Exception as e:
        print(f"Add student data error: {e}")
        messages.error(request, "Error uploading student data.")
    return render(request, "tpo/add-students.html")


# ==============================
# LOGOUT
# ==============================
@login_required(login_url='/student-login/')
def student_logout(request):
    logout(request)
    messages.info(request, 'Student logged out.')
    return redirect('student-login')


@login_required(login_url='/tpo-login/')
def tpo_logout(request):
    logout(request)
    messages.info(request, 'TPO logged out.')
    return redirect('tpo-login')


# ==============================
# CREATE SAMPLE TPO USER
# ==============================
def create_tpo(request):
    obj = TeacherModel.objects.create(name="Manisha", email="manisha@gmail.com")
    obj.set_password("password")
    obj.save()
    messages.success(request, "TPO user created successfully.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
