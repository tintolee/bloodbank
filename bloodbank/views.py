from django.shortcuts import render
from .models import Donors,BRequests,Contact_Us
from django.contrib.auth import login,authenticate,update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .forms import EditProfileForm
from .forms import SignUpForm
from .forms import UserForm
from django.utils.http import urlsafe_base64_encode
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib import messages

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.db import transaction
UserModel = get_user_model()
from .forms import SignUpForm
from .tokens import account_activation_token









# Create your views here.
def the_group(user_blood):
    if user_blood=="O Positive":
        the_group=["O Positive","A Positive","B Positive","AB Positive"]

    elif user_blood=="A Positive":
        the_group=["A Positive","AB Positive"]

    elif user_blood=="B Positive":
        the_group=["B Positive","AB Positive"]

    elif user_blood=="AB Positive":
        the_group=["AB Positive"]

    elif user_blood=="O Negative":
        the_group=["O Positive","A Positive","B Positive","AB Positive","O Negative","A Negative","AB Negative","B Negative"]

    elif user_blood=="A Negative":
        the_group=["A Positive","AB Positive","A Negative","AB Negative"]

    elif user_blood=="B Negative":
        the_group=["B Positive","AB Positive","B Negative","AB Negative"]

    elif user_blood=="AB Negative":
        the_group=["AB Positive","AB Negative"]

    return the_group
        

def home(request):
	return render(request,'index.html',{})



	

def aboutus(request):
	return render(request,'aboutus.html',{})



def eligibility(request):
	return render(request,'eligibility.html',{})	



def tandc(request):
	return render(request,'terms.html',{})	





@login_required
def donor(request):
        if request.method == 'POST':
            post=Donors()
           
            post.name= request.POST.get('person_name')
            post.age= request.POST.get('age')
            post.contact_number= request.POST.get('contact_number')
            post.address= request.POST.get('address')
            post.gender= request.POST.get('sex')
            post.blood_group= request.POST.get('blood_group')
            post.email=request.POST.get('email')
            post.state=request.POST.get('state')
            post.last_donated_date=request.POST.get('last_donated_date')
            post.major_illness=request.POST.get('major_illness')
            post.id=request.user.id
            post.b_request_id=None
            post.save()
           
                
            num=request.user.id
            userr = get_object_or_404(Donors, id=num)
            bg_group=the_group(userr.blood_group)
            args={'user':userr,'requests':BRequests.objects.filter(status=1),'donate_group':bg_group}
            return render(request,'profile.html',args)   

        else:
                return render(request,'donor.html',{'user':request.user.username}) 

@login_required
def profile(request):
    num=request.user.id
    userr = get_object_or_404(Donors, id=num)
    bg_group=the_group(userr.blood_group)
    args={'user':userr,'requests':BRequests.objects.filter(status=1),'donate_group':bg_group}
    return render(request,'profile.html',args)			
@login_required
def detail(request,pk):
    detail=BRequests.objects.get(id=pk)
    return render(request,'detail.html',{'x':detail})
@login_required
def favourite(request):
    c_userr=request.user.id
    c_user=Donors.objects.get(id=c_userr)
    try:
        selected_request=BRequests.objects.get(id=request.POST.get("donate"))
        if c_user.b_request_id !=None:
            prev_selected_request=c_user.b_request_id
    except:
        error=request.POST.get("donate")
        num=request.user.id
        userr = get_object_or_404(Donors, id=num)
        args={'user':userr,'requests':BRequests.objects.all()}
        return HttpResponse("request does not exist")
    else:
        temp=c_user.b_request_id
        c_user.b_request_id=selected_request
        c_user.save()
        d_donors=selected_request.donors_set.all()
        str1=""
        for giver in d_donors:
            str1+=giver.name+" "+giver.contact_number+"\n"
        selected_request.the_donors=str1
        selected_request.save()

        if temp != None:
            prev_selected_request=temp
            d_donors=prev_selected_request.donors_set.all()
            str1=""
            for giver in d_donors:
                str1+=giver.name+" "+giver.contact_number+"\n"
            prev_selected_request.the_donors=str1
            prev_selected_request.save()

        num=request.user.id
        userr = get_object_or_404(Donors, id=num)
        bg_group=the_group(userr.blood_group)
        args={'user':userr,'requests':BRequests.objects.filter(status=1),'donate_group':bg_group}
        return render(request,'profile.html',args)

@login_required
def requests(request):
        if request.method == 'POST':
            post=BRequests()
            post.patient_name= request.POST.get('patientname')
            post.attendant_name= request.POST.get('attendantname')
            post.contact_number= request.POST.get('contactnumber')
            post.blood_group= request.POST.get('bloodgroup')
            post.quantity= request.POST.get('quantity')
            post.hospital_name= request.POST.get('hospital')
            post.deadline=request.POST.get('date')
            post.status=0

            post.save()
            messages.success(request, 'Request submitted. We are commited to getting you a safe blood as soon as possible. Please make your phone number available while we work on getting the blood to your location at the nearest possible time')
            return render(request, 'seek.html')  

        else:
                return render(request,'seek.html')

@login_required                
def update(request):
    if request.method == 'POST':
            post=Donors.objects.get(id=request.user.id)
            post.name= request.POST.get('person_name')
            post.age= request.POST.get('age')
            post.contact_number= request.POST.get('contact_number')
            post.address= request.POST.get('address')
            post.gender= request.POST.get('sex')
            post.blood_group= request.POST.get('blood_group')
            post.email=request.POST.get('email')
            post.district=request.POST.get('district')
            post.pincode=request.POST.get('pincode')
            post.last_donated_date=request.POST.get('last_donated_date')
            post.major_illness=request.POST.get('major_illness')
            post.password=request.POST.get('psw')
            post.save()

            num=request.user.id
            userr = get_object_or_404(Donors, id=num)
            bg_group=the_group(userr.blood_group)
            args={'user':userr,'requests':BRequests.objects.filter(status=1),'donate_group':bg_group}
            return render(request,'new.html',args)
                 

    else:
            num=request.user.id
            userr = get_object_or_404(Donors, id=num)
            bg_group=the_group(userr.blood_group)
            args={'user':userr,'requests':BRequests.objects.filter(status=1),'donate_group':bg_group}
            return render(request,'profile.html',args)


@login_required
def delete(request):
    postt=request.user.id
    post=Donors.objects.get(id=postt)

    temp=post.b_request_id
    post.b_request_id=None
    post.save()
    rrequest=temp
    d_donors=rrequest.donors_set.all()
    str1=" "
    for giver in d_donors:
        str1+=giver.name+" "+giver.contact_number+"\n"
    rrequest.the_donors=str1
    rrequest.save()

    num=request.user.id
    userr = get_object_or_404(Donors, id=num)
    bg_group=the_group(userr.blood_group)
    args={'user':userr,'requests':BRequests.objects.filter(status=1),'donate_group':bg_group}
    return render(request,'profile.html',args)
    
  

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })

def contact_us(request):
        if request.method == 'POST':
            post=Contact_Us()
            post.firstname= request.POST.get('firstname')
            post.lastname= request.POST.get('lastname')
            post.email= request.POST.get('email')
            post.subject= request.POST.get('subject')
            post.save()
            return redirect('contact')   

        else:
            return render(request,'contact.html')   


              


def activation_sent_view(request):
    return render(request, 'activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.signup_confirmation = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'activation_invalid.html')

def signup_view(request):
    if request.method  == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            user.is_active = True
            user.save()
            current_site = get_current_site(request)
            subject = 'Please Activate Your Account'
            message = render_to_string('activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})




@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
       
        if user_form.is_valid() :
            user_form.save()
           
            messages.success(request,('Your profile was successfully updated!'))
            return redirect('settings:profile')
        else:
            messages.error(request,('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        
    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        })