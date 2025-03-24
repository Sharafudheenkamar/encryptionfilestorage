from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from .form import *

from .models import LoginTable, usertable

# Create your views here.
class Login(View):
    def get(self,request):
        return render(request,"login.html")
    
    def post(self,request):
            username =request.POST.get('username')
            password =request.POST.get('password')

            try:
                obj = LoginTable.objects.get(username=username,password=password)

                request.session['user_id'] = obj.id

                if obj.usertype == 'admin':
                    return render (request,'administrator/admin_home.html')
                elif obj.usertype == 'user':
                    return render(request,'user/user_home.html')
                else:
                    return HttpResponse('''<script>alert('invalid username and password');window.location.href='/'</script>''')
            except LoginTable.DoesNotExist:
                return HttpResponse('''<script>alert('invalid username and password');window.location.href='/'</script>''')
            return redirect('login') 

class admin_home(View):
    def get(self,request):
        return render(request,"administrator/admin_home.html") 

class UserView(View):
    def get(self,request):
        obj=usertable.objects.all()
        print(obj)
        return render(request,"administrator/users.html",{'val':obj}) 
    
class base(View):
    def get(self,request):
        return render(request,"administrator/base.html")  
    
class blockeduser(View):
    def get(self,request):
        return render(request,"administrator/blockeduser.html")  

    

    

class addfiles(View):
    def get(self,request):
        return render(request,"administrator/addfiles.html")
    
class base(View):
    def get(self,request):
        return render(request,"administrator/base.html")
    
class change(View):
    def get(self,request):
        return render(request,"user/change.html")
    def post(self,request):
        try:
            # Ensure user is logged in
            user_id = request.session.get('user_id')
            if not user_id:
                return HttpResponse("<script>alert('Session expired. Please log in again.'); window.location='/login';</script>")

            # Fetch user from the database
            user = LoginTable.objects.get(id=user_id)

            # Get old and new password from POST request
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            # Check if old password matches
            if user.password != old_password:  # Ideally, use hashed passwords
                return HttpResponse("<script>alert('Old password is incorrect!'); window.location='/change';</script>")

            # Validate new password fields
            if not new_password or not confirm_password:
                return HttpResponse("<script>alert('Password fields cannot be empty!'); window.location='/change';</script>")
            
            if new_password != confirm_password:
                return HttpResponse("<script>alert('Passwords do not match!'); window.location='/change';</script>")

            # Update password
            user.password = new_password  # Ideally, hash the password before saving
            user.save()

            return HttpResponse("<script>alert('Password changed successfully!'); window.location='/';</script>")

        except LoginTable.DoesNotExist:
            return HttpResponse("<script>alert('User not found. Please log in again.'); window.location='/login';</script>")

        return render(request, "user/change.html")
    
class edit(View):
    def get(self,request):
        print(request.session['user_id'])
        logind=LoginTable.objects.get(id=request.session['user_id'])
        user=usertable.objects.get(loginid=logind)
        print(user)
        return render(request,"user/edit.html",{'user':user})
    def post(self, request):
        try:
            # Ensure session contains 'user_id'
            user_id = request.session.get('user_id')
            if not user_id:
                return HttpResponse("<script>alert('Session expired. Please log in again.'); window.location='/login';</script>")

            # Fetch login and user details
            logind = LoginTable.objects.get(id=user_id)
            user = usertable.objects.get(loginid=logind)

            # Corrected typo: FIlES → FILES
            form = usertableform(request.POST, request.FILES, instance=user)

            if form.is_valid():
                form.save()
                print("User details updated successfully:", user)
                return HttpResponse("<script>alert('Profile updated successfully.'); window.location='/profile';</script>")

            return render(request, 'edit_profile.html', {'form': form, 'user': user})

        except LoginTable.DoesNotExist:
            return HttpResponse("<script>alert('User does not exist. Please log in again.'); window.location='/login';</script>")

        except usertable.DoesNotExist:
            return HttpResponse("<script>alert('User profile not found. Please contact support.'); window.location='/login';</script>")    
class profile(View):
    def get(self,request):
        print(request.session['user_id'])
        logind=LoginTable.objects.get(id=request.session['user_id'])
        user=usertable.objects.get(loginid=logind)
        print(user)
        return render(request,"user/profile.html",{'user':user})
    
class rating(View):
    def get(self,request):
        ra=Rating.objects.all()
        
        return render(request,"administrator/view-ratings.html",{'ra':ra})
    
class register(View):
    def get(self,request):
        return render(request,"user/register.html")
    def post(self, request):
        if request.method == "POST":
            form = usertableform(request.POST, request.FILES)
            if form.is_valid():
                username = request.POST.get('username')
                password = request.POST.get('password')  # Store securely in production
                email = form.cleaned_data.get('emailid')
                name = form.cleaned_data.get('Name')
                phone_number = form.cleaned_data.get('phone_number')
                place = form.cleaned_data.get('place')
                img = form.cleaned_data.get('img')

                # Check if username already exists
                if LoginTable.objects.filter(username=username).exists():
                    return HttpResponse("<script>alert('User already exists'); window.location='/register';</script>")

                # Save login details
                login_entry = LoginTable.objects.create(username=username, password=password, usertype='user')

                # Save user details
                usertable.objects.create(Name=name, phone_number=phone_number, emailid=email, place=place, img=img, loginid=login_entry)

                return redirect("login")  # Redirect to login on success

        return render(request, 'register.html', {'form': form})
        
           
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from .form import *

from .models import LoginTable, usertable

# Create your views here.
class Login(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            obj = LoginTable.objects.get(username=username, password=password)

            request.session['user_id'] = obj.id

            if obj.usertype == 'admin':
                return render(request, 'administrator/admin_home.html')
            elif obj.usertype == 'user':
                return render(request, 'user/user_home.html')
            else:
                return HttpResponse('''<script>alert('Invalid username and password');window.location.href='/'</script>''')
        except LoginTable.DoesNotExist:
            return HttpResponse('''<script>alert('Invalid username and password');window.location.href='/'</script>''')
        return redirect('login')

class AdminHome(View):
    def get(self, request):
        return render(request, "administrator/admin_home.html")

class UserView(View):
    def get(self, request):
        obj = usertable.objects.all()
        print(obj)
        blockedusers= usertable.objects.filter(loginid__status='rejected').count()
        unblockedusers=usertable.objects.filter(loginid__status='verified').count()
        return render(request, "administrator/users.html", {'val': obj,'blockedusers':blockedusers,'unblockedusers':unblockedusers})

class BaseView(View):
    def get(self, request):
        return render(request, "administrator/base.html")

class BlockedUserView(View):
    def get(self, request):
        return render(request, "administrator/blockeduser.html")

class AddFilesView(View):
    def get(self, request):
        return render(request, "administrator/addfiles.html")

class ChangeView(View):
    def get(self, request):
        return render(request, "administrator/change.html")

class EditView(View):
    def get(self, request):
        return render(request, "administrator/edit.html")

class ProfileView(View):
    def get(self, request):
        return render(request, "administrator/profile.html")

class RatingView(View):
    def get(self, request):
        ra = Rating.objects.all()
        return render(request, "administrator/view-ratings.html", {'ra': ra})

class RegisterView(View):
    def get(self, request):
        return render(request, "user/register.html")

    def post(self, request):
        if request.method == "POST":
            form = usertableform(request.POST, request.FILES)
            if form.is_valid():
                username = request.POST['username']
                password = request.POST['password']  # Hash the password
                email = form.cleaned_data['emailid']
                name = form.cleaned_data['Name']
                phone_number = form.cleaned_data['phone_number']
                place = form.cleaned_data['place']
                img = form.cleaned_data['img']

                # Save login details
                login_entry = LoginTable.objects.create(username=username, password=password, usertype='user')

                # Save user details
                usertable.objects.create(Name=name, phone_number=phone_number, emailid=email, place=place, img=img, loginid=login_entry)

                return redirect("login")

class UserHomeView(View):
    def get(self, request):
        return render(request, "administrator/user_home.html")

class ViewFilesView(View):
    def get(self, request):
        user_id = request.session['user_id']
        print(user_id)
        files = SecureFile.objects.filter(userid__id=user_id).all()
        print(files)
        return render(request, "user/viewfiles.html", {'datas': files})

class BlockedUserListView(View):
    def get(self, request):
        return render(request, "administrator/blockedUsers.html")

class VerifyUserView(View):
    def get(self, request, id):
        user = usertable.objects.get(id=id)
        print(user)
        user.loginid.status = "verified"
        user.loginid.save()
        return redirect('user')

class RejectUserView(View):
    def get(self, request, id):
        user = usertable.objects.get(id=id)
        li = LoginTable.objects.get(id=user.loginid.id)
        li.delete()
        print(user)
        # user.loginid.status="rejected"
        # user.loginid.save()
        return redirect('user')

# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views import View
from .models import SecureFile
from .crypt_utils import decrypt_file, hybrid_encrypt
from django.core.files.storage import default_storage

import os
from django.core.files.base import ContentFile

class UploadFileView(View):
    def get(self, request):
        return render(request, 'user/addfiles.html')

    def post(self, request):
        try:
            user_id = request.session.get('user_id')  # Use .get() to avoid KeyError
            if not user_id:
                return HttpResponse("User not authenticated.", status=403)

            title = request.POST.get('title')
            uploaded_file = request.FILES.get('uploaded_file')  # Avoid KeyError

            if not uploaded_file:
                return HttpResponse("No file uploaded.", status=400)

            file_data = uploaded_file.read()
            print(f"Received file: {uploaded_file.name}")

            user = LoginTable.objects.get(id=user_id)

            # Encrypt the file
            encrypted_data, aes_key, des3_key, blowfish_key = hybrid_encrypt(file_data)

            import base64

            # Convert keys to Base64 before saving them
            encrypted_file_obj = SecureFile(
                userid=user,
                title=title,
                aes_key=base64.b64encode(aes_key).decode(),  # Encode as Base64
                des3_key=base64.b64encode(des3_key).decode(),
                blowfish_key=base64.b64encode(blowfish_key).decode()
            )

            # Save the encrypted file
            encrypted_file_obj.file.save(
                uploaded_file.name, ContentFile(encrypted_data, 'application/octet-stream')
            )

            encrypted_file_obj.save()

            return render(request, 'user/addfiles.html')

        except Exception as e:
            print("Error:", e)
            return render(request, 'user/addfiles.html')

class EditFileView(View):
    def get(self, request, file_id):
        try:
            file_obj = SecureFile.objects.get(id=file_id)
            return render(request, 'administrator/editfile.html', {'file': file_obj})
        except SecureFile.DoesNotExist:
            return HttpResponse("File not found.", status=404)

    def post(self, request, file_id):
        try:
            file_obj = SecureFile.objects.get(id=file_id)

            title = request.POST.get('title')
            uploaded_file = request.FILES.get('file')

            if title:
                file_obj.title = title

            if uploaded_file:
                file_data = uploaded_file.read()
                encrypted_data, aes_key, des3_key, blowfish_key = hybrid_encrypt(file_data)
                filename = default_storage.save('encrypted_files/' + uploaded_file.name, encrypted_data)
                file_obj.file = filename

            file_obj.save()
            return HttpResponse("File updated successfully.")
        except SecureFile.DoesNotExist:
            return HttpResponse("File not found.", status=404)
        except Exception as e:
            print(f"Error: {e}")
            return render(request, 'administrator/editfile.html', {'file': file_obj, 'error': 'Something went wrong.'})

class DeleteFileView(View):
    def post(self, request, file_id):
        try:
            file_obj = SecureFile.objects.get(id=file_id)
            file_obj.delete()
            return HttpResponse("File deleted successfully.")
        except SecureFile.DoesNotExist:
            return HttpResponse("File not found.", status=404)

class FileListView(View):
    def get(self, request):
        userid = request.session['user_id']
        files = SecureFile.objects.filter(userid__id=userid).all()
        return render(request, 'user/viewfiles.html', {'datas': files})

# VIEWS.PY
class DownloadFileView(View):
    def get(self, request, file_id):
        secure_file = get_object_or_404(SecureFile, id=file_id)

        # Get the encrypted file path
        file_path = os.path.join('media', str(secure_file.file))
        try:
            with open(file_path, 'rb') as f:
                encrypted_data = f.read()

            import base64

            # Convert Base64-encoded keys back to bytes before using them
            aes_key = base64.b64decode(secure_file.aes_key)
            des3_key = base64.b64decode(secure_file.des3_key)
            blowfish_key = base64.b64decode(secure_file.blowfish_key)

            # Decrypt the file
            decrypted_data = decrypt_file(encrypted_data, aes_key, des3_key, blowfish_key)

            # Decrypt the file using the stored keys
            # decrypted_data = decrypt_file(encrypted_data, aes_key, des3_key, blowfish_key)

            # Prepare file response for download
            response = HttpResponse(decrypted_data, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{secure_file.file.name}"'
            return response
        except Exception as e:
            return HttpResponse(f"Error decrypting file: {str(e)}", status=500)
    
class user_home(View):
    def get(self,request):
        return render(request,"administrator/user_home.html")
    
class viewfiles(View):
    def get(self,request):
        user_id=request.session['user_id']
        print(user_id)
        files = SecureFile.objects.filter(userid__id=user_id).all()
        print(files)
        return render(request,"user/viewfiles.html",{'datas':files})
    
class blockedUser(View):
    def get(self,request):
        return render(request,"administrator/blockedUsers.html")
class Verifyuser(View):
    def get(self,request,id):
        user=usertable.objects.get(id=id)
        print(user)
        user.loginid.status="verified"
        user.loginid.save()
        return redirect('user')
class Rejectuser(View):
    def get(self,request,id):
        user=usertable.objects.get(id=id)
        li=LoginTable.objects.get(id=user.loginid.id)
        li.delete()
        print(user)
        # user.loginid.status="rejected"
        # user.loginid.save()
        return redirect('user')   
    # views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views import View
from .models import SecureFile
from .crypt_utils import decrypt_file, hybrid_encrypt
from django.core.files.storage import default_storage

import os
from django.core.files.base import ContentFile

class UploadFileView(View):
    def get(self, request):
        return render(request,'user/addfiles.html')

    def post(self, request):
        try:
            user_id = request.session.get('user_id')  # Use .get() to avoid KeyError
            if not user_id:
                return HttpResponse("User not authenticated.", status=403)

            title = request.POST.get('title')
            uploaded_file = request.FILES.get('uploaded_file')  # Avoid KeyError

            if not uploaded_file:
                return HttpResponse("No file uploaded.", status=400)

            file_data = uploaded_file.read()
            print(f"Received file: {uploaded_file.name}")

            user = LoginTable.objects.get(id=user_id)

            # Encrypt the file
            encrypted_data, aes_key, des3_key, blowfish_key = hybrid_encrypt(file_data)

            import base64

            # Convert keys to Base64 before saving them
            encrypted_file_obj = SecureFile(
                userid=user,
                title=title,
                aes_key=base64.b64encode(aes_key).decode(),  # Encode as Base64
                des3_key=base64.b64encode(des3_key).decode(),
                blowfish_key=base64.b64encode(blowfish_key).decode()
            )

            # Save the encrypted file
            encrypted_file_obj.file.save(
                uploaded_file.name, ContentFile(encrypted_data,'application/octet-stream')
            )

            encrypted_file_obj.save()



            return render(request, 'user/addfiles.html')

        except Exception as e:
            print("Error:", e)
            return render(request, 'user/addfiles.html')

class EditFileView(View):
    def get(self, request, file_id):
        try:
            file_obj = SecureFile.objects.get(id=file_id)
            return render(request, 'administrator/editfile.html', {'file': file_obj})
        except SecureFile.DoesNotExist:
            return HttpResponse("File not found.", status=404)

    def post(self, request, file_id):
        try:
            file_obj = SecureFile.objects.get(id=file_id)

            title = request.POST.get('title')
            uploaded_file = request.FILES.get('file')

            if title:
                file_obj.title = title

            if uploaded_file:
                file_data = uploaded_file.read()
                encrypted_data, aes_key, des3_key, blowfish_key = hybrid_encrypt(file_data)
                filename = default_storage.save('encrypted_files/' + uploaded_file.name, encrypted_data)
                file_obj.file = filename

            file_obj.save()
            return HttpResponse("File updated successfully.")
        except SecureFile.DoesNotExist:
            return HttpResponse("File not found.", status=404)
        except Exception as e:
            print(f"Error: {e}")
            return render(request, 'administrator/editfile.html', {'file': file_obj, 'error': 'Something went wrong.'})
class DeleteFileView(View):
    def post(self, request, file_id):
        try:
            file_obj = SecureFile.objects.get(id=file_id)
            file_obj.delete()
            return HttpResponse("File deleted successfully.")
        except SecureFile.DoesNotExist:
            return HttpResponse("File not found.", status=404)

class FileListView(View):
    def get(self, request):
        userid=request.session['user_id']
        files = SecureFile.objects.filter(userid__id=id).all()
        return render(request, 'user/viewfiles.html', {'datas': files})
#VIEWS.PY
class DownloadFileView(View):
    def get(self, request, file_id):
        secure_file = get_object_or_404(SecureFile, id=file_id)
        
        # Get the encrypted file path
        file_path = os.path.join('media', str(secure_file.file))
        try:
            with open(file_path, 'rb') as f:
                encrypted_data = f.read()

            import base64

            # Convert Base64-encoded keys back to bytes before using them
            aes_key = base64.b64decode(secure_file.aes_key)
            des3_key = base64.b64decode(secure_file.des3_key)
            blowfish_key = base64.b64decode(secure_file.blowfish_key)

            # Decrypt the file
            decrypted_data = decrypt_file(encrypted_data, aes_key, des3_key, blowfish_key)

            # Decrypt the file using the stored keys
            # decrypted_data = decrypt_file(encrypted_data, aes_key, des3_key, blowfish_key)

            # Prepare file response for download
            response = HttpResponse(decrypted_data, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{secure_file.file.name}"'
            return response
        except Exception as e:
            return HttpResponse(f"Error decrypting file: {str(e)}", status=500)


    
    
    
    
    