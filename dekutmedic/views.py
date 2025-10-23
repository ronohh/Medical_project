from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
import random
from datetime import datetime
from django.utils import timezone
from dekutmedic.models import CustomUser
from .models import DoctorRegistration, PatientReg, Appointment,AddPatient, MedicalHistory, ReferralAppointment, Payment, Insurance
from django.core.paginator import Paginator,EmptyPage
from .forms import PatientReferralForm
import requests
import base64
import json
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from requests.auth import HTTPBasicAuth
from decimal import Decimal

# Create your views here.

def base(request):

    return render(request, 'base.html')

def Userbase(request):
    """
    Render the index page.
    """
    return render(request, 'userbase.html')

# admin panel
def adminhome(request):
    doctor_count=DoctorRegistration.objects.all().count
    students_count = CustomUser.objects.filter(user_type=3).count
    staff_count = CustomUser.objects.filter(user_type=4).count
    context = {
        'doctor_count':doctor_count,
        'students_count': students_count,
        'staff_count': staff_count,
    }
    return render(request, 'admin/adminhome.html', context)

def doctorList(request):
    doctorlist = DoctorRegistration.objects.all()
    context = {'doctorlist':doctorlist}
    
    return render(request, 'admin/doctor-list.html', context)

def ViewDoctorDetails(request,id):
    doctorlist1 = DoctorRegistration.objects.filter(id=id)
    context = {
        'doctorlist1': doctorlist1
    }
    return render(request, 'admin/doctor-details.html', context)

def ViewDoctorPatient(request,id):
    patde = AddPatient.objects.filter(doctor_id=id)
    context = {
        'patde':patde
    }
    return render(request, 'admin/doctor_patient.html', context)

# def ViewDoctorPatientDetails(request,id):
#     patient_data = AddPatient.objects.get(id=id)
#     medrec_data = MedicalHistory.objects.filter(pat_id=id)
#     context = {
#         "pd": patient_data,
#         "mrd": medrec_data,
#     }
#     return render(request, 'admin/doctor_patient_details.html',context)

def ViewDoctorAppointmentList(request,id):
    patientdetails = Appointment.objects.filter(doctor_id=id)
    context = {
        'patientdetails': patientdetails
    }
    return render(request, 'admin/doctor_appointment_list.html',context)

def ViewAppointmentPatientsDetails(request,id):
    patientdetails = Appointment.objects.filter(id=id)
    context={'patientdetails':patientdetails}

    return render(request, 'admin/appointment_patient_details.html',context)
def Registeredusers(request):
    staff_count = CustomUser.objects.filter(user_type=4).count
    students_count = CustomUser.objects.filter(user_type=3).count
    context = {
        'students_count': students_count,
        'staff_count': staff_count
    }
    return render(request, 'admin/regusers.html', context)
def StaffMembersList(request):
    staffmembers = PatientReg.objects.filter(admin__user_type=4)
    context = {
        "staffmembers": staffmembers
    }
    return render(request, 'admin/staff_members_list.html', context)
def StudentsList(request):
    students = PatientReg.objects.filter(admin__user_type=3)
    context = {
        "students": students
    }
    return render(request, 'admin/student_list.html', context)
# def RegisteredUsersDetails(request):
#     regusers = PatientReg.objects.all()
#     context = {
#         "regusers": regusers
#         }
#     return render(request, 'admin/registered-users.html', context)

def DeleteRegUsers(request,id):
    try:
        patreg = PatientReg.objects.get(id=id)
        custom_user =patreg.admin
        patreg.delete()
        custom_user.delete()
        messages.success(request, 'Record deleted successfully!')
    except PatientReg.DoesNotExist:
        messages.error(request, f'patient does not exist.')
    except Exception as e:
        messages.error(request, f'error deleting record: {e}')
    return redirect('regusers')

def Registered_User_Appointments(request,id):
    pat_admin = PatientReg.objects.get(id=id)
    userapptdetails = Appointment.objects.filter(pat_id= pat_admin)

    context = {
        'vah': userapptdetails
    }
    return render(request, 'admin/registered_users_appointment.html', context)


def index(request):
    """
    Render the index page.
    """
    return render(request, 'index.html',)


def login_view(request):

    return render(request, 'login.html')

def dologout(request):
    logout(request)
    return redirect('login')

def dologin(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user = authenticate(request, username=username, password=password)
                                         
        if user!= None:
            login(request, user)
            user_type = user.user_type
            if user_type == 1 :
                return redirect('admindashboard')
            elif user_type == 2 :
                return redirect('doctordashboard')
            elif user_type == 3 :
                return redirect('patienthome')
            elif user_type == 4:
                return redirect('staffdashboard')
            
            else:
                return redirect('patienthome')
            

        else:
            messages.error(request, 'Email or Password is not valid')
            return redirect('login')
    else:
        messages.error(request, 'Email or Password is not valid')
        return redirect('login')
def Profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    context = {
        "user": user
    }
    return render(request, 'profile.html', context)
def ProfileUpdate(request):
    if request.method == "POST":
        profile_pic = request.FILES.get("profile_pic")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        mobilenumber = request.POST.get("mobilenumber")
        print("POSTed mobile number:", mobilenumber)
        print(profile_pic)

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            customuser.mobilenumber = mobilenumber
            
            if profile_pic != None and profile_pic != "":
                customuser.profile_pic = profile_pic
            customuser.save()
            messages.success(request, "your Profile has been updated successfully")
            return redirect('profile')
        except:
            messages.error(request, "Your profile updation has failed")
    return render(request, 'profile.html')
    
def InsuranceList(request):
    insurances = Insurance.objects.all()
    context = {
        "insurances": insurances
    }
    return render(request, "admin/Insurance_list.html",context)

def InsuranceAdd(request):
    patients = PatientReg.objects.filter(admin__user_type=4)
    if request.method == "POST":
        patient_id = request.POST.get("patient")
        total_cover = request.POST.get("total_cover")
        balance = request.POST.get("balance") or total_cover

        try:
            patient = PatientReg.objects.get(id=patient_id)
            insurance = Insurance.objects.create(
                patient = patient,
                total_cover = Decimal(total_cover),
                balance = Decimal(balance)
            )
            messages.success(request, f"Insurance created for {patient.admin.first_name} {patient.admin.last_name}")
            return redirect('insurancelist')
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
    context = {
        "patients": patients
    }
    return render(request, 'admin/Insurance_add.html', context)

def InsuranceEdit(request, id):
    insurance = Insurance.objects.filter(id=id)
    if request.method == "POST":
        insurance.total_cover = request.POST.get("total_cover")
        insurance.balance = request.POST.get("balance")
        insurance.save()
        messages.success(request, "Insurance updated successfully")
        return redirect('insurancelist')
    context = {
        "insurance" : insurance
    }
    
    return render(request, 'admin/insurance_edit.html', context)

def InsuranceDelete(request, id):
    insurance = Insurance.objects.filter(id=id)
    insurance.delete()
    messages.success(request, "Insurance deleted sucessfully")
    redirect("insurancelist")
def claim_insurance(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    try:
        insurance = Insurance.objects.get(patient=appointment.pat_id)
        if insurance.deduct_fee(appointment.consultancy_fee):
            appointment.paid_by_insurance = True
            appointment.save(update_fields=["paid_by_insurance"])
            messages.success(request, "Consultancy fee paid through insurance")
        else:
            messages.error(request, "Insufficient insurance balance")
    except Insurance.DoesNotExist:
        messages.error(request, "No insurance found for this patient")

    return redirect('approvedappointments')


# staff
def staffregistration(request):
    if request.method == "POST":
        pic = request.FILES.get('pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        mobno = request.POST.get('mobno')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email already exists')
            return redirect('staffregistration')
        
        elif CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'username already exists')
            return redirect('staffregistration')
        
        else:
            user = CustomUser(
                first_name = first_name,
                last_name= last_name,
                username=username,
                email=email,
                user_type=4,
                profile_pic=pic,
                mobilenumber=mobno
            )
            user.set_password(password)
            user.save()

            staff = PatientReg(
                admin = user,
                gender = gender
            )
            staff.save()
            messages.success(request, 'Signup successfully')
            return redirect('login')

        

    return render(request, 'staff/staff-register.html')

def staffhome(request):

    return render(request, 'staff/staffhome.html')

def Requestreferral(request):
    try:
        patient = PatientReg.objects.get(admin= request.user)
    except PatientReg.DoesNotExist:
        messages.error(request, "Patient profile not found")
        return redirect("staffdashboard")
    if request.method == "POST":
        form = PatientReferralForm(request.POST)
        if form.is_valid():
            referral = form.save(commit=False)
            referral.pat_id = patient
            referral.save()
            messages.success(request, "Referral request sent")
            return redirect("staffdashboard")
        else:
            messages.error(request, "referral request not succesfull,retry.")
    else:
        form = PatientReferralForm()
    context = {
        "form": form,
        "patient": patient
    }
    return render(request, 'staff/referral.html',context)

# patient

def patientregistration(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name =request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        gender= request.POST.get('gender')
        username = request.POST.get('username')
        mobno = request.POST.get('mobno')
        password = request.POST.get('password')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('patientregistration')
        if CustomUser.objects.filter(username=username).exists():
            messages.success(request, 'username already exists')
            return redirect('patientregistration')
        
        else:
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                user_type=3,
                profile_pic = profile_pic,
                mobilenumber = mobno,
            )
            user.set_password(password)
            user.save()

            patient = PatientReg(
                admin=user,
                gender = gender
            )
            patient.save()
            messages.success(request, 'Signup successful')
            return redirect('login')

    return render(request, 'patient/register.html')

def patienthome(request):
    doctor_count = DoctorRegistration.objects.all().count
    context= {
        'doctor_count': doctor_count,
    }

    return render(request, 'patient/patienthome.html',context)

def Index(request):
    doctorview =DoctorRegistration.objects.all()
    first_page = Page.objects.first()

    context = {
        'doctorview':doctorview,
        'page': first_page
    }

    return render(request, 'index.html', context)

def get_doctor(request):
    if request.method == 'GET':
        doctors = DoctorRegistration.objects.all()
        data = [
            {"id": doc.id, "name":f"{doc.admin.first_name}"}
            for doc in doctors if doc.admin
        ]
        
        return JsonResponse({'doctors': data })

def create_appointment(request):
    if request.method == "POST":
        try:
            appointmentnumber= random.randint(100000000, 999999999)
            doctor_id = request.POST.get('doctor_id')
            date_of_appointment = request.POST.get('date_of_appointment')
            time_of_appointment = request.POST.get('time_of_appointment')
            additional_msg = request.POST.get('additional_msg')

            doc_instance = DoctorRegistration.objects.get(id = doctor_id)

            patient_instance = PatientReg.objects.get(admin= request.user)

            try:
                appointment_date = datetime.strptime(date_of_appointment,'%Y-%m-%d').date()
                today_date = timezone.now().date()

                if appointment_date <= today_date:
                    messages.error(request, "please select a date in the future for your appointment")
                    return redirect('patientappointment')
            except ValueError:
                messages.error(request, "invalid date format")
                return redirect('patientappointment')
            
            Appointment.objects.create(
                appointmentnumber= appointmentnumber,
                pat_id = patient_instance,
                doctor_id = doc_instance,
                date_of_appointment = date_of_appointment,
                time_of_appointment = time_of_appointment,
                additional_msg = additional_msg
            )
            messages.success(request, "Appointment booked successfully")

        except DoctorRegistration.DoesNotExist:
            messages.error(request, "selected doctor does not exists.")
        except PatientReg.DoesNotExist:
            messages.error(request, "Patient informtion could not be retrieved.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
        return redirect('patientappointment')

    return render(request, 'patient/appointment.html')

def view_appointment_history(request):
    pat_reg = request.user
    pat_admin = PatientReg.objects.get(admin= pat_reg)
    userapptdetails = Appointment.objects.filter(pat_id=pat_admin)
    context = {
        'vah': userapptdetails
    }
    return render(request, 'patient/appointment-history.html',context)

def cancel_appointment(request,id):
    try:
        appointment = Appointment.objects.get(id=id, pat_id=request.user.patientreg)
        if appointment.status !='Approved':
            appointment.status = 'Canceled'
            appointment.save()
            messages.success(request, "Your appointment has been canceled successfully.")
        else:
            messages.error(request, "you cannot cancel this appointment")
    except Appointment.DoesNotExist:
        messages.error(request, "Appointment not found")
    return redirect('view_appointment_history')

def appointment_history_details(request):
    patientdetails=Appointment.objects.filter(id=id)
    context={
        'patientdetails':patientdetails
    }
    return render(request, 'UserAppointmentDetails.html',context)
def records(request,id):
    patientdetails=Appointment.objects.filter(id=id)
    context={
        'patientdetails':patientdetails
    }
    return render(request, 'patient/Records.html', context)

# doctor
def docsignup(request):
    if request.method == "POST":
        pic = request.FILES.get('pic')
        first_name =request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        mobno = request.POST.get('mobile')
        password = request.POST.get('password')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email already exists')
            return redirect('docsignup')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'username already exists')
            return redirect('docsignup')
        else:
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                user_type=2,
                profile_pic = pic,
                mobilenumber = mobno,
            )
            user.set_password(password)
            user.save()
            doctor = DoctorRegistration(
                admin = user,
            )
            doctor.save() 
            messages.success(request, 'Doctor registered successfully')
            return redirect('login')

    return render(request, 'doctor/docregister.html')

def doctorhome(request):
    doctor_admin =request.user
    try:
        doctor_reg = DoctorRegistration.objects.get(admin=doctor_admin)
    except DoctorRegistration.DoesNotExist:
        messages.error(request, "Doctor profile not found. Please complete your registration.")
        return redirect('docsignup')
    allaptcount = Appointment.objects.filter(doctor_id=doctor_reg).count
    newaptcount = Appointment.objects.filter(status='0',doctor_id=doctor_reg).count
    appaptcount = Appointment.objects.filter(status='Approved', doctor_id=doctor_reg).count
    canaptcount = Appointment.objects.filter(status='canceled', doctor_id=doctor_reg).count
    doctor_admin = request.user
    doct_id = DoctorRegistration.objects.get(admin=doctor_admin)
    patcount = AddPatient.objects.filter(doctor_id=doct_id).count
    context= {
        'newaptcount':newaptcount,
        'allaptcount':allaptcount,
        'appaptcount':appaptcount,
        'canaptcount':canaptcount,
        'patcount':patcount 
    }
    
    return render(request, 'doctor/doctorhome.html',context)

def Add_Patient(request):
    if request.method == "POST":
        name = request.POST.get('name')
        mobilenumber = request.POST.get('mobilenumber')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        medhistory = request.POST.get('medhistory')

        doctor_admin = request.user
        try:
            doct_id = DoctorRegistration.objects.get(admin=doctor_admin)
        except DoctorRegistration.DoesNotExist:
            messages.error(request, "Doctor not found")
            return redirect('addpatient')
        
        if AddPatient.objects.filter(email=email).exists():
            messages.warning(request, 'Email already exists')
            return redirect('addpatient')
        if AddPatient.objects.filter(mobilenumber=mobilenumber).exists():
            messages.warning(request, 'Mobile number already exists')
            return redirect('addpatient')
        
        addpatient = AddPatient(
            name= name,
            mobilenumber= mobilenumber,
            email=email,
            gender=gender,
            medicalhistory= medhistory,
            doctor_id=doct_id,
        )
        addpatient.save()
        messages.success(request, 'Data added successfully')
        return redirect('addpatient')
    
    return render(request, 'doctor/add_patient.html')

def Manage_Patient(request):
    doctor_admin= request.user
    doct_id = DoctorRegistration.objects.get(admin=doctor_admin)
    patde = AddPatient.objects.filter(doctor_id=doct_id)
    context={
        'patde':patde
    }

    return render(request, 'doctor/manage_patient.html',context)

def ViewPatientDetails(request,id):
    patient_data = AddPatient.objects.get(id=id)
    medrec_data = MedicalHistory.objects.filter(pat_id=id)
    context = {
        "pd": patient_data,
        "mrd":medrec_data,
    }
    
    return render(request, 'doctor/update_patient_medical_record.html',context)

def update_patient_medical_record(request):
    if request.method == 'POST':
        patient_id =request.POST.get('p_id')
        bloodpressure = request.POST.get('bloodpressure')
        weight = request.POST.get('weight')
        bodytemp = request.POST.get('bodytemp')
        diagnosis = request.POST.get('diagnosis')
        prescription = request.POST.get('prescription')

        try:
            patient_instance = AddPatient.objects.get(id=patient_id)
        except AddPatient.DoesNotExist:
            messages.error(request, "patient does not exist")
            return redirect('managepatient')
        
        medical_history = MedicalHistory(
            pat_id = patient_instance,
            bloodpressure=bloodpressure,
            weight=weight,
            bodytemp=bodytemp,
            diagnosis = diagnosis,
            prescription=prescription
        )
        medical_history.save()
        messages.success(request, "Medical record added successfully")
        return redirect('managepatient')
    
    return render(request, 'doctor/update_patient_medical_record.html')

def view_patient(request, id):
    patient_data = AddPatient.objects.get(id=id)
    context = {
        "pd":patient_data,
    }

    return render(request, 'doctor/edit_patient.html',context)

def edit_patient(request):
    if request.method == "POST":
        pat_id = request.POST.get('pid')
        try:
            patient_edit = AddPatient.objects.get(id=pat_id)
        except AddPatient.DoesNotExist:
            messages.error(request,"Patient details do not exist ")
            return redirect('managepatient')
        
        updated_patient = {
            'name': request.POST.get('name'),
            'mobilenumber': request.POST.get('mobilenumber'),
            'email':request.POST.get('email'),
            'gender':request.POST.get('gender'),
            'age':request.POST.get('age'),
            'medicalhistory':request.POST.get('medhistory')
        }

        for field, value in updated_patient.items():
            if value:
                setattr(patient_edit,field,value)

        patient_edit.save()
        messages.success(request, "Patient details have been updated successfully")
        return redirect('managepatient')

    return render(request, 'edit_patient.html')

def All_appointment(request):
    patientdetails = Appointment.objects.all()

    context = {
        'patientdetails': patientdetails
    }
    return render(request, 'doctor/all_appointment.html',context)
        

def View_Appointment(request):
    try:
        doctor_admin = request.user
        doctor_reg = DoctorRegistration.objects.get(admin= doctor_admin)
        View_Appointment = Appointment.objects.filter(doctor_id=doctor_reg)

        #pagination
        paginator = Paginator(View_Appointment, 10 )
        page = request.GET.get('page')
        try:
            view_appointment = paginator.page(page)
        except EmptyPage:
            view_appointment = Paginator.page(paginator.num_pages)

        context = {'view_appointment': view_appointment}
    except Exception as e:
        context = {'error_message': str(e)}
    

    return render(request, 'doctor/view_appointment.html', context)

def View_Appointment_Details(request, id):
    patientdetails= Appointment.objects.filter(id=id)
    context= {
        'patientdetails': patientdetails
          }

    return render(request, 'doctor/view_appointment_details.html',context)

def Patient_Appointment_Details_Remark(request):
    if request.method == 'POST':
        patient_id = request.POST.get('pat_id')
        diagnosis= request.POST['diagnosis']
        prescription = request.POST.get('prescription')
        consultancyfee= request.POST['consultancy fee']
        status = request.POST['status']
        patientaptdet = Appointment.objects.get(id=patient_id)
        patientaptdet.diagnosis = diagnosis
        patientaptdet.prescription = prescription
        patientaptdet.status = status
        patientaptdet.consultancy_fee= consultancyfee
        patientaptdet.save()
        messages.success(request,"status Update successfully")
        return redirect('view_appointment')
    
    return render(request, 'doctor/view_appointment.html')

def Approved_Appointments(request):
    doctor_admin = request.user
    doctor_reg = DoctorRegistration.objects.get(admin=doctor_admin)
    patientdetails1 = Appointment.objects.filter(status= 'Approved',doctor_id=doctor_reg)
    context = {'patientdetails1':patientdetails1}

    return render(request, 'doctor/appointments.html', context)

def Cancelled_Appointments(request):
    doctor_admin = request.user
    doctor_reg = DoctorRegistration.objects.get(admin=doctor_admin)
    patientdetails1 = Appointment.objects.filter(status= 'Canceled',doctor_id=doctor_reg)
    context = {'patientdetails1': patientdetails1 }

    return render(request, 'doctor/appointments.html', context)

def New_Appointments(request):
    doctor_admin = request.user
    doctor_reg = DoctorRegistration.objects.get(admin=doctor_admin)
    patientdetails1 = Appointment.objects.filter(status="0", doctor_id= doctor_reg)

    context = { 'patientdetails1' : patientdetails1 }

    return render(request, 'doctor/appointments.html', context )

def Patient_List_Approved_Appointment(request):
    doctor_admin =request.user
    doctor_reg = DoctorRegistration.objects.get(admin=doctor_admin)
    patientdetails1 = Appointment.objects.filter(status='Approved',doctor_id=doctor_reg)
    context = {'patientdetails1': patientdetails1 }
    return render(request, 'doctor/patient_list_approved_appointment.html', context)

def DoctorAppointmentList(request,id):
    patientdetails= Appointment.objects.filter(id=id)
    context = {'patientdetails': patientdetails}
    
    return render(request, 'doctor/doctor_appointment_list_details.html',context)

def Patient_Appointment_Prescription(request):
    if request.method == 'POST':
        patient_id = request.POST.get('pat_id')
        prescription = request.POST['prescription']
        recommendedtest = request.POST['recommendedtest']
        status = request.POST['status']
        patientaptdet = Appointment.objects.get(id=patient_id)
        patientaptdet.prescription = prescription
        patientaptdet.recommendedtest = recommendedtest
        patientaptdet.status = status
        patientaptdet.save()
        messages.success(request, 'status update successfully')
        return redirect('view_appointment')
    return render(request, 'doctor/patient_list_approved_appointment.html')

def Patient_Appointment_Completed(request):
    doctor_admin=request.user
    doctor_reg= DoctorRegistration.objects.get(admin=doctor_admin)
    patientdetails1 = Appointment.objects.filter(status='Completed',doctor_id=doctor_reg)
    context = {
        'patientdetails1': patientdetails1
        }
    return render(request, 'doctor/patient_list_approved_appointment.html',context)

def doctor_referral_list(request):
    doctor_admin = request.user
    doctor_reg= DoctorRegistration.objects.get(admin=doctor_admin)
    if request.method == 'POST':
        referral_id = request.POST.get("referral_id")
        action = request.POST.get("action")
        remark = request.POST.get("remark","")

        referral = get_object_or_404(ReferralAppointment, id=referral_id, doctor_id =doctor_reg)
        if action == "accept":
            referral.status="Accepted"
            referral.remark = remark
            messages.success(request, "Referral has been accepted")
        elif action == "reject":
            referral.status = "Rejected"
            referral.remark = remark
            messages.error(request, "Referral has been rejected")
        referral.save()
        return redirect("doctor_referrals")

    referrals = ReferralAppointment.objects.filter(doctor_id=doctor_reg)
    context= {
        'referrals':referrals
    }
    return render(request, "doctor/referral_list.html", context)

def Between_Date_Report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    patient = []
    doctor_admin = request.user
    doctor_reg = DoctorRegistration.objects.get(admin=doctor_admin)

    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return render(request, 'doctor/between_dates_report.html', {'patient':patient, 'error_message':'Invalid date format'})
        patient = Appointment.objects.filter(created_at__range=(start_date, end_date) & Appointment.objects.filter(doctor_id=doctor_reg))
    return render(request, 'doctor/between_dates_report.html',{'patient':patient, 'start_date':start_date, 'end_date': end_date})


# DARAJA
def get_access_token():
    url = f"{settings.DARAJA_API_BASE}/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(
        url,
        auth = HTTPBasicAuth(settings.DARAJA_CONSUMER_KEY, settings.DARAJA_CONSUMER_SECRET),
    )
    if response.status_code != 200:
        raise Exception("Failed to obtain access token" f"status: {response.status_code}, Response: {response.text}")
    data = response.json()
    return data.get("access_token")

def stk_form(request):
    appointment_id = request.GET.get("appointment")
    appointment = None
    if appointment_id:
        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            appointment =None

    return render(request, "staff/payment.html", {"appointment": appointment})

def stk_push(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        amount = request.POST.get("amount")
        appointment_id = request.POST.get("appointment_id")
        patient_id =request.POST.get("patient_id")

        appointment = None
        patient = None

        if appointment_id:
            appointment = Appointment.objects.get(id = appointment_id)
            patient = appointment.pat_id
        elif patient_id:
            patient = PatientReg.objects.get(id = patient_id)
        elif phone:
            patient = PatientReg.objects.get(admin__mobilenumber = phone)

        payment = Payment.objects.create(
            appointment = appointment,
            patient = patient,
            phone_number = phone,
            amount= amount,
            status = "pending"
        )

        try:
            access_token = get_access_token()
        except Exception as e:
            messages.error(request, f"Access token error: {e}")
            return redirect(request.META.get("HTTP_REFERER", "stk_form"))
        
        headers = {"Authorization": f"Bearer {access_token}"}

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        password_str = f"{settings.DARAJA_SHORTCODE}{settings.DARAJA_PASSKEY}{timestamp}"
        password = base64.b64encode(password_str.encode()).decode("utf-8")

        payload = {
            "BusinessShortCode": settings.DARAJA_SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(float(amount)),
            "PartyA":phone,
            "PartyB": settings.DARAJA_SHORTCODE,
            "PhoneNumber": phone,
            "CallBackURL": settings.DARAJA_CALLBACK_URL,
            "AccountReference": "DeKUTmedcentre",
            "TransactionDesc": "Patient Payment",
        }
        url = f"{settings.DARAJA_API_BASE}/mpesa/stkpush/v1/processrequest"
        response = requests.post(url, json=payload, headers= headers)

        try:
            resp_data = response.json()
        except ValueError:
            messages.error(request, f"Invalid Safaricom response: {response.text}")
            return redirect(request.META.get("HTTP_REFERER","stk_form"))
        
        if "CheckoutRequestID" in resp_data:
            payment.checkout_request_id = resp_data["CheckoutRequestID"]
            payment.save()

        if resp_data.get("ResponseCode") == "0":
            messages.success (request, "payment request sent to your phone. please enter M-PESA PIN")
        else:
            messages.error (request, f"Failed : {resp_data.get('errorMessage', 'unknown error')}")
        return redirect(request.META.get("HTTP_REFERER","stk_form"))
        
    return render(request, "staff/payment.html")
@csrf_exempt
def mpesa_callback(request):
    data = json.loads(request.body.decode("utf-8"))
    print("MPESA CALLBACK:", json.dumps(data, indent=4))

    callback = data.get("Body", {}).get("stkCallback",{})
    checkout_request_id = callback.get("CheckoutRequestID")
    result_code = callback.get("ResultCode")

    try:
        payment =Payment.objects.get(checkout_request_id=checkout_request_id)
    except Payment.DoesNotExist:
        return HttpResponse("Payment record not found")
    
    if result_code == 0:
        items = callback["CallbackMetadata"]["Item"]
        for item in items:
            if item["Name"] == "MpesaReceiptNumber":
                payment.mpesa_code = item["Value"]
        payment.status = "success"

    else:
        payment.status = "failed"
    payment.save()

    return HttpResponse("Callback received")