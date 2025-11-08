from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # admin panel
    path('adminhome/', views.adminhome, name='admindashboard'),
    path('base/', views.base, name='base'),
    path('Admin/doctorlist/', views.doctorList, name='viewdoctorlist'),
    path('Admin/pharmacistlist/', views.pharmacistList, name='viewpharmacistlist'),
    path('ViewDoctorDetails/<str:id>', views.ViewDoctorDetails, name='viewdoctordetails'),
    path('Admin/ViewDoctorPatient/<str:id>', views.ViewDoctorPatient, name='viewdoctorpatient'),
    # path('Admin/ViewDoctorPatientDetails/<str:id>', views.ViewDoctorPatientDetails, name='viewdoctorpatientdetails'),
    path('Admin/registeredusers/', views.Registeredusers, name='registeredusers'),
    path('Admin/staffmembers/', views.StaffMembersList, name='staffmemberslist'),
    path('Admin/studentslist/', views.StudentsList, name='studentslist'),
    path('Admin/DoctorAppointmentList/<str:id>',views.ViewDoctorAppointmentList, name='ViewDoctorAppointmentList'),
    path('AdminAppointmentPatientDetails/<str:id>', views.ViewAppointmentPatientsDetails, name='viewappointmentpatientsdetails'),
    path('RegisteredUserAppointment/<str:id>', views.Registered_User_Appointments, name='registeredusersappointments'),
    path('DeleteRegusers/<str:id>', views.DeleteRegUsers, name='deleteusersdetails'),
    path('Admin/insuranceList/', views.InsuranceList, name="insurancelist"),
    path('Admin/insurance/add', views.InsuranceAdd, name="insuranceadd"),
    path('Admin/insurance/Edit/<str:id>', views.InsuranceEdit, name='editinsurance'),
    path('Admin/insurance/delete/<str:id>', views.InsuranceDelete, name='insurancedelete'),
    


    path('login/', views.login_view, name='login'),
    path('logout', views.dologout, name='dologout'),
    path('dologin/', views.dologin, name='dologin'),
    path('profile', views.Profile, name='profile'),
    path('profile/update', views.ProfileUpdate, name='profileupdate'),

    # user panel
    path('userbase/', views.Userbase, name='userbase'),
    path('', views.index, name='index'),
    path('patientregistration/', views.patientregistration, name="patientregistration"),
    path('patienthome/', views.patienthome, name='patienthome'),
    path( 'patientappointment/', views.create_appointment, name='patientappointment'),
    path('get_doctor/', views.get_doctor, name='get_doctor'),
    path('viewAppointmentHistory/', views.view_appointment_history, name='viewappointmenthistory'),
    path('cancelappointment/<str:id>', views.cancel_appointment, name='cancelappointment'),
    path('AppointmentHistoryDetails/', views.appointment_history_details, name='viewappointmenthistorydetails'),
    path('records/<str:id>/', views.records, name='records'),

    # staff panel
    path('staffregistration/', views.staffregistration, name='staffregistration'),
    path('staffhome/', views.staffhome, name='staffdashboard'),
    path('staff/dependantslist/', views.dependantslist, name='dependantslist'),
    path('adddependants/', views.AddDependants, name='adddependants'),
    path('staff/Referrals/', views.Requestreferral, name='referrals'),
    path('staff/referral_history/', views.referral_history, name='referral_history'),

    # pharmacist panel
    path('pharmacistsignup/', views.pharmacistsignup, name='pharmacistsignup'),
    path('pharmacistdashboard/', views.pharmacistdashboard, name='pharmacistdashboard'),
    path('pharmacist/newappointments/', views.newappointments, name='newpharmacistappointments'),
    path('pharmacist/newpatients/', views.newpatients, name='newpharmacistpatients'),
    path('pharmacy/records/', views.pharmacy_records, name='pharmacy_records'),
    path('dispense/<str:id>/', views.mark_as_dispensed, name='mark_as_dispensed'),
    path('notprescribed/<str:id>/', views.mark_as_not_prescribed, name='mark_as_not_prescribed'),

    # doctor panel
    path('docsignup/', views.docsignup, name='docsignup'),
    path('doctorhome/', views.doctorhome, name='doctordashboard'),
    path('doctor/AddPatient', views.Add_Patient, name='addpatient'),
    path('doctor/ManagePatient/', views.Manage_Patient, name='managepatient'),
    path('doctor/ViewPatient/<str:id>', views.view_patient, name='viewpatient'),
    path('doctor/EditPatient', views.edit_patient, name='editpatient'),
    path('doctor/ViewPatientDetails/<str:id>', views.ViewPatientDetails, name='viewpatientdetails'),
    path('doctor/UpdatePatientMedicalRecord', views.update_patient_medical_record, name='updatepatientmedicalrecord'),
    path('doctor/ViewAppointment', views.View_Appointment, name='view_appointment'),
    path('doctor/ViewAppointmentDetails/<str:id>', views.View_Appointment_Details, name="viewappointmentdetails"),
    path('appointmentDetailsRemark/Update', views.Patient_Appointment_Details_Remark, name='PatientAppointmentDetailsRemark'),
    path('doctor/ApprovedAppointment', views.Approved_Appointments, name='approvedappointments'),
    path('doctor/CancelledAppointments', views.Cancelled_Appointments, name="cancelledappointments"), 
    path('doctor/NewAppointments/', views.New_Appointments, name="newappointments"),
    path('doctorPatientListApprovedAppointment', views.Patient_List_Approved_Appointment, name='patientlistappointment'),
    path('doctorAppointmentList/<str:id>', views.DoctorAppointmentList, name='doctorappointmentlist'),
    path('PatientAppointmentPrescription/', views.Patient_Appointment_Prescription,name='PatientAppointmentPrescription'),
    path('PatientAppointmentCompleted/', views.Patient_Appointment_Completed, name='PatientAppointmentCompleted'),
    path('doctor/referralList/', views.doctor_referral_list, name='doctor_referrals'),
    path('BetweenDatePatientReport', views.Between_Date_Report, name='betweendatepatientreport'),
    path('Admin/Allappointment/', views.All_appointment, name="allappointment"),
    path('claim_insurance/<str:id>/', views.claim_insurance, name='claim_insurance'),
    
    # daraja
    path("mpesa/stkpush/", views.stk_push, name="stk_push"),
    path("mpesa/form/", views.stk_form, name="stk_form"),
    path("mpesa/callback/", views.mpesa_callback, name="mpesa_callback"),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)