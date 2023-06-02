from django.forms import ValidationError
from django.shortcuts import redirect, render
from django.http import Http404, HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib import messages
from .form import EntryForm, AdminForm
from django.db.models.functions import Now
import csv
from .models import *
from datetime import datetime

# Views of Guest list
def guests_list_view(request):
    sql_query = "SELECT * FROM guests_upcominginput AS A JOIN guests_guest AS B ON A.phone_number = B.phone_number ORDER BY status ASC"
    guest_list = UpcomingInput.objects.raw(sql_query)
    # Paginate existed data, display 25 data
    paginator = Paginator(guest_list, 25)

    # get page number
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context= {
        'list': page_obj
    }
    return render(request, 'all_guests.html', context)
# def guests_list_view(request):
#     # get all data in model Guest
#     guest_list = Guest.objects.all()

#     # Paginate existed data, display 25 data
#     paginator = Paginator(guest_list, 25)

#     # get page number
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     # OBJECT TO CALL IN HTML FILE
#     context = {
#         'list': page_obj
#     }
# return render(request, 'all_guests.html', context)

# Create view for admin file upload   
def admin_page_view(request):
    # INITIAL FORM
    form = AdminForm(request.POST or None, request.FILES or None)

    # VALIDATE IF FORM IS VALID ACCORDING TO REQUIRED
    if form.is_valid():
        form.save()
        form = AdminForm()

        # GET THE LATEST IMPORTED DATA
        obj = Csv.objects.all()[Csv.objects.count()-1]

        # USE PACKAGE 'CSV' TO READ AND OPEN FILE
        with open(obj.file_name.path, 'r') as f:
            reader = csv.reader(f)

            # IGNORE THE FIRST COLON SINCE IT'S JUST HEADER
            next(reader)

            # alist = []
            # LOOP INTO FILE AND STORE DATA ACCORDINGLY
            for row in reader:
                # Remove space
                x = int(row[1].replace(" ", ""))
                
                # WRITE DATA TO DATABASE AND STORE GUESTS INFORMATION
                Guest.objects.update_or_create(
                    name = row[0],
                    phone_number = x,
                )
                UpcomingInput.objects.update_or_create(
                    phone_number = x,
                    status = 2
                )
                print(x)
        messages.success(request, "Successfully upload!")
        # return redirect('/guest_list/')
    return render(request, 'admin_page.html', {"form": form})

# Create view of guest entry and checking for existing data
def check_validate(request):
    form = EntryForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            # FORM VALIDATE FIELD PHONE NUMBER
            new_number = form.clean_message()
            # TRY CATCH ERROR
            try:
                # GET DATA WHERE PHONE NUMBER EQUAL TO NEW INPUT NUMBER
                Guest.objects.get(phone_number = int(new_number))
                # FILTER AND GET VALUE
                data = Guest.objects.filter(phone_number = int(new_number)).values()
                # print(data)
                print("Match")

                # WRITE DATA TO UPCOMINGINPUT MODEL, STATUS=1 MEAN USER IS COMING TO THE EVENT
                msg = messages.success(request,"You're invited! Data match in invitation list")
                # UpcomingInput.objects.filter(phone_number = int(new_number)).update(status=1)
                UpcomingInput.objects.filter(phone_number = int(new_number)).update(status=1, incoming_timestamps = datetime.now())

                return render(request, 'access_granted.html', {"form": form, "data": data, "msg":msg})
            # HANDLE ERROR IF DATA DOESN'T EXIST
            except Guest.DoesNotExist:
                msg = messages.error(request,"Sorry phone number does not match data in invitation list! Please contact an administrator near you!")
                print("Not Match")
                return render(request, 'access_denied.html', {"form": form, "msg":msg})
        # else:
        #     raise ValidationError("Character not allowed")
    return render(request, "guests.html", {"form": form})
    
    