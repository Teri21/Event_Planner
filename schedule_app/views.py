from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt


# Create your views here.


def index(request):
    return render(request, 'index.html')

 # user is logged in?
 # otherwise it will
    # if it's in session means your logged in


def register(request):
    if request.method == "POST":
        # make validations
        errors = User.objects.validate(request.POST)
        if errors:
            for error in errors.values():
                messages.error(request, error)
            return redirect('/')

# otherwise continue
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        password = request.POST["password"]

        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
# for the password = value field shouldn't be the password but the hash..
        user = User.objects.create(first_name=first_name,
                                   last_name=last_name, email=email, password=pw_hash)
#  sessions saves data
        request.session["user_id"] = user.id
        # using string interpolation(f string) to pass those variables in..
        request.session["user_name"] = f"{user.first_name} {user.last_name}"
    return redirect('/welcome')


def login(request):
    if request.method == "POST":

        email = request.POST["email"]
        password = request.POST["password"]

        logged_user = User.objects.filter(email=email)

        if logged_user:
            logged_user = logged_user[0]

            if bcrypt.checkpw(password.encode(), logged_user.password.encode()):
                request.session["user_id"] = logged_user.id
                request.session["user_name"] = f"{logged_user.first_name} {logged_user.last_name}"
                return redirect('/welcome')

            else:
                messages.error(request, "Password isn't correct. ")
                # if pw isn't correct return to home pg.
                return redirect('/')

        else:
            messages.error(request, "This user doesn't exist")
            return redirect('/')


def welcome(request):

    if "user_id" not in request.session:
        return redirect('/')

    context = {

        "events": Event.objects.all()
    }

    return render(request, "welcome.html", context)


def create_event(request):
    created_by = User.objects.get(id=request.session['user_id'])
    event = Event.objects.create(
        title=request.POST["title"],
        description=request.POST["description"],
        location=request.POST['location'],
        date_time=request.POST['date_time'],
        user=created_by,
    )

    return redirect('/welcome')


def one_event(request, id):
    if "user_id" not in request.session:
        return redirect('/')

    one_event = Event.objects.get(id=id)

    context = {
        'event': one_event
    }
    return render(request, "event.html", context)


def edit(request, id):

    one_event = Event.objects.get(id=id)

    if request.method == "GET":

        context = {
            'event': one_event
        }
        return render(request, "edit.html", context)

    else:
        update = Event.objects.get(id=id)

        update.title = request.POST["title"]
        update.description = request.POST["description"]
        update.location = request.POST["location"]
        update.date_time = request.POST["date_time"]

        update.save()
        return redirect(f'/one_event/{id}')


def add_like(request, id):

    liked_event = Event.objects.get(id=id)
    user = User.objects.get(id=request.session['user_id'])
    liked_event.user_likes.add(user)

    return redirect('/welcome')


def delete_event(request, id):
    destroyed = Event.objects.get(id=id)
    destroyed.delete()
    return redirect('/welcome')


def logout(request):
    request.session.clear()
    return redirect('/')
