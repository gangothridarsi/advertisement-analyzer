from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import *
from django.urls import reverse
import cv2
from .machinelearning import pipeline_model
from .forms import AdvertisementForm

# Create your views here.

# REGISTER A USER
def CreateUser(request):
    if request.POST:
        # Get the values from HTML file
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email_id = request.POST['email_id']
        password = request.POST['password']
        # check if user is a customer or not
        if customer in request.POST:
            customer = True
        else:
            customer = False
        try:
            # Add user into database
            User.objects.create(first_name=first_name, last_name=last_name,username=username,email_id=email_id,password=password, customer=customer)
            return redirect(reverse('login'))
        except:
            # If we get any errors, then display to signup again.
            return render(request, 'signup.html', {'error': "User already exist or invalid details, please try again!"})
    return render(request, 'signup.html')

# Login Page
def Login(request):
    # Get the username and password to validate
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        try:
            # Check if user exist or not
            user = User.objects.get(username=username)
            if user.username == username and user.password == password:
                webpage = reverse('advapp:main', kwargs={'id':user.id, 'customer' : user.customer})
                return HttpResponseRedirect(webpage)
            else:
                # If user does not exist, then display an alert message
                return render(request, 'login.html', {'error' : "Invalid credentials, plesse login again"})
        except Exception as e:
            # If user does not exist, then display an error message
            return render(request, 'login.html', {'error' : "User does not exist, please signup again!"})
    return render(request, 'login.html')

# Display avalibale advertisements
def displayAds(request, uname):
    user = User.objects.get(username = uname)
    # get all the advertisements to send into template
    imgobj = Advertisement.objects.all()
    return render(request, 'displayAll.html', {'imgobj':imgobj, 'id' : user.id})

# When the user clicks a specific advertisement
def getAdDetails(request,uid, adid):
    ad = Advertisement.objects.get(addId = adid)
    # If form is submitted, then evaluate the facial expression
    if request.POST:
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        ret, frame = cap.read()
        res = pipeline_model(frame)
        cv2.waitKey(0)
        cap.release()
        cv2.destroyAllWindows()
        # Save the results in database
        user = User.objects.get(id = uid)
        adid = Advertisement.objects.get(addId = ad.addId)
        res['emotion_name'] = "happy"
        obj = UserResults(username = user, addId = adid, emotion_name = res['emotion_name'])
        obj.save()
        return render(request, 'adDetail.html', {'ad': ad, 'detected' : "Your emotion has been recorded successfully, Thankyou!"})
    return render(request, 'adDetail.html', {'ad': ad, 'flag' : True})


# Main page
def Main(request, id, customer):
    obj = User.objects.get(id = id)
    if obj.customer == True:
        return render(request, 'main.html', {'id':obj.id, 'username':obj.username, 'name' : obj.first_name + ' ' + obj.last_name, 'customer' : customer})
    return render(request, 'main.html', {'id':obj.id, 'username':obj.username, 'name' : obj.first_name + ' ' + obj.last_name})


# Get the results of their ads for advertisements owners
def manageAds(request,id):
    ads = Advertisement.objects.filter(username = id).all()
    results = {}
    for i in ads:
        users = UserResults.objects.filter(addId = i.addId).all()
        # Initially setting all expressions to 1
        sad = 1
        happy = 1
        angry = 1
        neutral = 1
        for user in users:
            if user.emotion_name == "sad":
                sad += 1
            elif user.emotion_name == "angry":
                angry += 1
            elif user.emotion_name == "neutral":
                neutral += 1
            else:
                happy += 1
        sadPercent = round((sad/(sad + angry + neutral + happy)) * 100,2)
        angryPercent = round((angry/(sad + angry + neutral + happy)) * 100,2)
        neutralPercent = round((neutral/(sad + angry + neutral + happy)) * 100,2)
        happyPercent = round((happy/(sad + angry + neutral + happy)) * 100,2)
        results[i.addId] = {'image' : i.image,'adName' : i.adName, 'adDescription' : i.adDescription, 'adid' : i.addId, 'sadP' : sadPercent, 'angryP' : angryPercent, 'neutralP' : neutralPercent, 'happyP' : happyPercent}
    return render(request, 'manage.html', {'ads':ads, 'id':id, 'results' : results})


# Create an advertisement
def AdCreate(request, id):
    form = AdvertisementForm()
    if request.POST:
        form = AdvertisementForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            s = form.save(commit = True)
            user = User.objects.get(id = id)
            s.username = user
            s.save()
            # If created then redirect into manage.html file
            return redirect(reverse('advapp:manage', kwargs={'id':id}))
    return render(request, 'adCreate.html', {'form':form})