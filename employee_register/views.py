from django.shortcuts import render,HttpResponse, redirect
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .models import BotDetail
from .botforms import BotDetailForm
from django.contrib import messages
from django.http import JsonResponse
from .models import Employee, Staff, Equipment
from .forms import EmployeeForm
from django.db.models import Q
from django.core import serializers
from django.http import JsonResponse
from datetime import datetime
from django.utils import timezone
from django.forms.models import model_to_dict
import requests
import json
import csv

class CustomEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, (datetime, datetime.date, datetime.time)):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        return super().default(obj)

@csrf_protect
def admin_login(request):
    if request.user.is_authenticated:
        return redirect('employee_list')  # Redirect to the homepage if already logged in
    
    if request.method == 'POST':
        username = request.POST.get('user')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/list')  # Redirect to a different page upon successful login
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('/admin_login')  # Redirect back to the login page on failure

    return render(request, 'employee_register/admin_login.html')

def logout_view(request):
    logout(request)
    return redirect('/admin_login')

@login_required
def employee_list(request):
    return render(request,"employee_register/employee_list.html")

@login_required
def employee_staff(request):
    return render(request, "employee_register/staff_list.html")

@login_required
def employee_equipment(request):
    return render(request, "employee_register/asset_list.html")

def send_message(method, data):
    bot_detail = BotDetail.objects.first()
    chat_id = bot_detail.chat_id
     
    data['chat_id'] = chat_id
    if bot_detail:
        TELEGRAM_API_URL = f'https://api.telegram.org/bot{bot_detail.token}/'
        return requests.post(TELEGRAM_API_URL + method, data)

def employee_form(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)

        if form.is_valid():
            emp_id = form.cleaned_data['emp_id']
            fullname = form.cleaned_data['fullname']
            asset_tag = form.cleaned_data['asset_tag']
            duration = form.cleaned_data.get('duration', None)
            form_type = form.cleaned_data['form_type']

            # Handle borrow form
            if form_type == 'borrow':
                
                equipment_instance = Equipment.objects.filter(asset_tag=asset_tag).first()
                model_name = equipment_instance.model if equipment_instance and equipment_instance.model else "Unknown Model"
                
                employee_register = Employee(
                    emp_id=emp_id,
                    fullname=fullname,
                    asset_tag=asset_tag,
                    model=model_name,
                    duration=duration,
                    status="Pending",
                    return_by="N/A",
                    created_at=datetime.now()
                )
                employee_register.save()
                
                message = (
                            "📢 *New Borrow Request*\n"
                            "👤 *Fullname:* _{fullname}_\n"
                            "🆔 *Employee ID:* `{emp_id}`\n"
                            "🔖 *Asset Tag:* `{asset_tag}`\n"
                            "📄 *Model:* _{model_name}_\n"
                            "⏳ *Duration:* _{duration}_\n"
                            "📌 *Status:* *Pending*\n"
                            "🗓️ *Created at:* *{created_at}*"
                            
                        ).format(
                            fullname=fullname,
                            emp_id=emp_id,
                            asset_tag=asset_tag,
                            model_name=model_name,
                            duration=duration,
                            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        )
                
                send_message("sendMessage", {
                    'text': message,
                    'parse_mode': 'Markdown'
                })

            # Handle return form
            elif form_type == 'return':
                equipment_instance = Equipment.objects.filter(asset_tag=asset_tag).first()
                model_name = equipment_instance.model if equipment_instance and equipment_instance.model else "Unknown Model"
                employees_to_update = Employee.objects.filter(asset_tag=asset_tag, status="Pending")
                
                if not employees_to_update.exists():
                    # If no matching pending entry, create a new one
                    employee_register = Employee(
                        emp_id=emp_id,
                        fullname=fullname,
                        asset_tag=asset_tag,
                        model=model_name,
                        duration="N/A",
                        status="Completed",
                        return_by=fullname,
                        created_at=datetime.now()
                    )
                    employee_register.save()
                    
                    message = (
                        "📢 *Return Request Completed (⛔No Borrow⛔)*\n"
                        "👤 *Fullname:* _{fullname}_\n"
                        "🆔 *Employee ID:* `{emp_id}`\n"
                        "🔖 *Asset Tag:* `{asset_tag}`\n"
                        "📄 *Model:* _{model_name}_\n"
                        "⏳ *Duration:* _{duration}_\n"
                        "📌 *Status:* *Completed*\n"
                        "↩️ *Return By:* _{fullname}_\n"
                        "🗓️ *Created at:* *{created_at}*"
                    ).format(
                        fullname=fullname,
                        emp_id=emp_id,
                        asset_tag=asset_tag,
                        model_name=model_name,
                        duration="N/A",
                        created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    )
                    
                    send_message("sendMessage", {
                        'text': message,
                        'parse_mode': 'Markdown'
                    })
                    
                else:
                    # Update the status for each matched pending entry
                    for employee in employees_to_update:
                            employee.status = "Completed"
                            employee.return_by = fullname
                            employee.save()
                            
                            message = (
                                "📢 *Return Request Completed*\n"
                                "👤 *Fullname:* _{fullname}_\n"
                                "🆔 *Employee ID:* `{emp_id}`\n"
                                "🔖 *Asset Tag:* `{asset_tag}`\n"
                                "📄 *Model:* _{model_name}_\n"
                                "⏳ *Duration:* _{duration}_\n"
                                "📌 *Status:* *Completed*\n"
                                "↩️ *Return By:* _{return_by}_\n"
                                "🗓️ *Created at:* *{created_at}*"
                            ).format(
                                fullname=employee.fullname,
                                emp_id=emp_id,
                                asset_tag=asset_tag,
                                model_name=model_name,
                                duration=employee.duration,  # Use existing duration
                                return_by=fullname,
                                created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            )
                            
                            send_message("sendMessage", {
                                'text': message,
                                'parse_mode': 'Markdown'
                            })

            return render(request, "employee_register/employee_form.html", {
                'form': form
            })
        else:
            # Handle form errors
            for error in form.errors.values():
                messages.error(request, error)

    else:
        form = EmployeeForm()  # Create a blank form on GET request

    return render(request, "employee_register/employee_form.html", {
        'form': form
    })

@login_required
def telegram_update(request):
    bot_detail = BotDetail.objects.first()

    if not bot_detail:
        bot_detail = BotDetail.objects.create(token='', chat_id='')

    if request.method == 'POST':
        form = BotDetailForm(request.POST, instance=bot_detail)
        if form.is_valid():
            bot_detail = form.save(commit=False)
            bot_detail.last_modify = datetime.now()
            bot_detail.save()

            user = request.user
            messages.success(request, f"Bot token and chat ID updated by {user.username}.")
            message = f"Welcome to Borrow & Request BOT ( Status -->> Connected)"
            send_message("sendMessage", {
                'text': message
            })
            return redirect('telegram_bot')

        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BotDetailForm(instance=bot_detail)

    context = {
        'form': form,
        'last_modify': bot_detail.last_modify,
        'chat_id': bot_detail.chat_id,
        'username': request.user.username if request.user.is_authenticated else 'Unknown',
    }

    return render(request, 'employee_register/telegram_bot.html', context)

@csrf_protect
def form_search_staff(request):
        search_term = request.GET.get('q', '')
        if search_term:
            staff = Staff.objects.filter(
                Q(fullname__icontains=search_term) | Q(emp_id__icontains=search_term)
            )
        else:
            staff = Staff.objects.all()

        data = list(staff.values('emp_id', 'fullname'))
        return JsonResponse(data, safe=False)

@csrf_protect
def form_search_equipment(request):
        search_term = request.GET.get('q', '')
        if search_term:
            asset = Equipment.objects.filter(
                Q(asset_tag__icontains=search_term) | Q(display_name__icontains=search_term) | Q(model__icontains=search_term)
            )
        else:
            asset = Equipment.objects.all()

        data = list(asset.values('asset_tag', 'display_name', 'model'))
        return JsonResponse(data, safe=False)

def getJson(request):
    json = list(Employee.objects.values())
    return JsonResponse(json,safe=False,encoder=CustomEncoder)

@login_required
def staffJson(request):
    staff_json = list(Staff.objects.values())
    return JsonResponse(staff_json,safe=False)

@login_required
def equipmentJson(request):
    equipment_json = list(Equipment.objects.values())
    return JsonResponse(equipment_json,safe=False)

@login_required
def add_employee(request):
    if request.method == 'POST':
        try:
            body_dict = json.loads(request.body)
            asset_tag = body_dict.get('asset_tag')
            equipment_instance = Equipment.objects.filter(asset_tag=asset_tag).first()
            model_name = equipment_instance.model if equipment_instance and equipment_instance.model else "Unknown Model"
            
            emp_id = body_dict.get('emp_id')
            fullname = body_dict.get('fullname')
            model = model_name
            duration = body_dict.get('duration')
            #created_at = datetime.now()
            created_at = body_dict.get('created_at')

            employee = Employee(emp_id=emp_id, fullname=fullname, asset_tag=asset_tag, model=model, duration=duration, created_at=created_at)
            employee.save()
            print(model_to_dict(employee))
            return JsonResponse(model_to_dict(employee), encoder=CustomEncoder, safe=False)
        except Exception as e:
            return JsonResponse({"error": f"Error saving employee: {str(e)}"}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


@login_required
def edit_employee(request, id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            employee = Employee.objects.get(id=id)
            new_asset_tag = data.get('asset_tag', employee.asset_tag)
            equipment_instance = Equipment.objects.filter(asset_tag=new_asset_tag).first()
            model_name = equipment_instance.model if equipment_instance and equipment_instance.model else "Unknown Model"
            
            # Update fields if provided
            employee.emp_id = data.get('emp_id', employee.emp_id)
            employee.fullname = data.get('fullname', employee.fullname)
            employee.asset_tag = new_asset_tag
            employee.model = model_name
            employee.duration = data.get('duration', employee.duration)
            employee.status = data.get('status', employee.status)
            employee.created_at = data.get('created_at', employee.created_at)
                
            print(f"Updated employee: {employee.created_at}")
            # Save the updated employee
            employee.save()
            # Log the updated fields
            print(f"Updated employee: {model_to_dict(employee)}")
            
            return JsonResponse(model_to_dict(employee), encoder=CustomEncoder, safe=False)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Employee.DoesNotExist:
            return JsonResponse({"error": "Employee not found"}, status=404)
        except Exception as e:
            # Log exception details for debugging
            print(f"Error updating employee: {str(e)}")
            return JsonResponse({"error": f"Error updating employee: {str(e)}"}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

@login_required
def delete_employee(request, id):
    if request.method == 'DELETE':
        try:
            employee = Employee.objects.get(id=id)
            employee.delete()
            return JsonResponse({"message": "Employee deleted successfully"})
        except Employee.DoesNotExist:
            return JsonResponse({"error": "Employee not found"}, status=404)
        
@login_required
def clear_all_data_list(request):
    if request.method == "POST":
        Employee.objects.all().delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

#########################################################################################

@login_required
def add_staff(request):
    if request.method == 'POST':
        try:
            body_dict = json.loads(request.body)
            emp_id = body_dict.get('emp_id')
            fullname = body_dict.get('fullname')
            sex = body_dict.get('sex')
            status = body_dict.get('status')
            #created_at = datetime.now()
            department = body_dict.get('department')

            staff = Staff(emp_id=emp_id, fullname=fullname, sex=sex, status=status, department=department)
            staff.save()
            print(model_to_dict(staff))
            return JsonResponse(model_to_dict(staff), encoder=CustomEncoder, safe=False)
        except Exception as e:
            return JsonResponse({"error": f"Error saving employee: {str(e)}"}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

@login_required
def edit_staff(request, id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            staff = Staff.objects.get(id=id)
            
            # Update fields if provided
            staff.emp_id = data.get('emp_id', staff.emp_id)
            staff.fullname = data.get('fullname', staff.fullname)
            staff.sex = data.get('sex', staff.sex)
            staff.status = data.get('status', staff.status)
            staff.department = data.get('department', staff.department)

            # Save the updated employee
            staff.save()
            # Log the updated fields
            print(f"Updated employee: {model_to_dict(staff)}")
            
            return JsonResponse(model_to_dict(staff), encoder=CustomEncoder, safe=False)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Employee.DoesNotExist:
            return JsonResponse({"error": "Employee not found"}, status=404)
        except Exception as e:
            # Log exception details for debugging
            print(f"Error updating employee: {str(e)}")
            return JsonResponse({"error": f"Error updating employee: {str(e)}"}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
    
    

#########################################################################################


'''def delete_staff(request, id):
    if request.method == 'DELETE':
        try:
            staff = Staff.objects.get(id=id)
            staff.delete()
            return JsonResponse({"message": "Employee deleted successfully"})
        except Employee.DoesNotExist:
            return JsonResponse({"error": "Employee not found"}, status=404)
        '''
        
@login_required
def delete_multiple(request):
    if request.method == 'POST':
        ids = request.POST.getlist('ids[]')
        Staff.objects.filter(id__in=ids).delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def clear_all_data(request):
    if request.method == "POST":
        Staff.objects.all().delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def import_csv(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        for row in data:
            Staff.objects.create(
                fullname=row.get('fullname'),
                emp_id=row.get('emp_id'),
                sex=row.get('sex'),
                status=row.get('status'),
                department=row.get('department')
            )
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})


#########################################################################################

@login_required
def add_equipment(request):
    if request.method == 'POST':
        try:
            body_dict = json.loads(request.body)
            display_name = body_dict.get('display_name')
            asset_tag = body_dict.get('asset_tag')
            internal_reference = body_dict.get('internal_reference')
            model = body_dict.get('model')
            quantity = body_dict.get('quantity')
            asset_type = body_dict.get('asset_type')

            equipment = Equipment(display_name=display_name, asset_tag=asset_tag, internal_reference=internal_reference, model=model, quantity=quantity, asset_type=asset_type)
            equipment.save()
            print(model_to_dict(equipment))
            return JsonResponse(model_to_dict(equipment), encoder=CustomEncoder, safe=False)
        except Exception as e:
            return JsonResponse({"error": f"Error saving employee: {str(e)}"}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

@login_required
def edit_equipment(request, id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            equipment = Equipment.objects.get(id=id)
            
            # Update fields if provided
            equipment.display_name = data.get('display_name', equipment.display_name)
            equipment.asset_tag = data.get('asset_tag', equipment.asset_tag)
            equipment.internal_reference = data.get('internal_reference', equipment.internal_reference)
            equipment.model = data.get('model', equipment.model)
            equipment.quantity = data.get('quantity', equipment.quantity)
            equipment.asset_type = data.get('asset_type', equipment.asset_type)

            # Save the updated employee
            equipment.save()
            # Log the updated fields
            print(f"Updated employee: {model_to_dict(equipment)}")
            
            return JsonResponse(model_to_dict(equipment), encoder=CustomEncoder, safe=False)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Employee.DoesNotExist:
            return JsonResponse({"error": "Employee not found"}, status=404)
        except Exception as e:
            # Log exception details for debugging
            print(f"Error updating employee: {str(e)}")
            return JsonResponse({"error": f"Error updating employee: {str(e)}"}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

#########################################################################################


'''def delete_staff(request, id):
    if request.method == 'DELETE':
        try:
            staff = Staff.objects.get(id=id)
            staff.delete()
            return JsonResponse({"message": "Employee deleted successfully"})
        except Employee.DoesNotExist:
            return JsonResponse({"error": "Employee not found"}, status=404)
        '''
        
@login_required
def delete_multiple_equipment(request):
    if request.method == 'POST':
        ids = request.POST.getlist('ids[]')
        Equipment.objects.filter(id__in=ids).delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def clear_all_data_equipment(request):
    if request.method == "POST":
        Equipment.objects.all().delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def import_csv_equipment(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        for row in data:
            Equipment.objects.create(
                display_name=row.get('display_name'),
                asset_tag=row.get('asset_tag'),
                internal_reference=row.get('internal_reference'),
                model=row.get('model'),
                quantity=row.get('quantity'),
                asset_type=row.get('asset_type')
            )
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})


