from django.http import HttpResponse
from rest_framework.decorators import api_view
from .serializer import *
from .SMS import get_phone_number, sms
from .models import DeliveryReport


@api_view(['POST'])
def get_sick_employee_by_hospital(request):
    response_dict = dict()
    if request.method == 'POST':
        serializer = NameSerializer(data=request.data)
        if serializer.is_valid():
            hospital_name = serializer.validated_data.get('name')
            hospital_obj = Hospital.objects.filter(name=hospital_name).first()
            patients = Sick.objects.filter(hospital=hospital_obj)
            patients_list = list()
            for patient in patients:
                try:
                    employee_obj = Employee.objects.get(nationalID=patient.nationalID)
                except:
                    employee_obj = None
                if employee_obj and patient.illName == 'Covid19':
                    patients_list.append((employee_obj.name, employee_obj.nationalID))
            for i, p in enumerate(patients_list):
                response_dict[i] = p

    return response_dict


@api_view(['POST'])
def get_sick_employee_by_company(request):
    response_dict = dict()
    if request.method == 'POST':
        serializer = NameSerializer(data=request.data)
        if serializer.is_valid():
            company_name = serializer.validated_data.get('name')
            company_obj = Company.objects.filter(name=company_name).first()
            employees = Employee.objects.filter(company=company_obj)
            employees_list = list()
            for employee in employees:
                try:
                    patient_obj = Hospital.objects.get(nationalID=employee.nationalID)
                except:
                    patient_obj = None
                if patient_obj and patient_obj.illName == 'Covid19':
                    employees_list.append((patient_obj.name, patient_obj.nationalID))
            for i, p in enumerate(employees_list):
                response_dict[i] = p

    return response_dict


async def sms_link(request):
    # ---- DO NOT REMOVE THIS -----
    request.META['CONTENT_LENGTH'] = 35
    # ---- DO NOT REMOVE THIS -----
    if request.method == 'POST':
        serializer = NationalIDSerializer(data=request.data)
        if serializer.is_valid():
            national_id = serializer.validated_data.get('national_id')
            phone_number = get_phone_number(national_id)
            sms_sent = await sms(phone_number)
            if sms_sent:
                delivery_obj = DeliveryReport.objects.create(phone_number=phone_number)
                delivery_obj.save()
                return HttpResponse(status=200)
