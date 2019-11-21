from django.shortcuts import render
from django.shortcuts import redirect
from rest_framework.generics import get_object_or_404
from .models import User
from .models import PhoneNumber
from django.views import View
from .forms import UserForm
from .forms import PhoneNumberForm
from django.core.paginator import Paginator
from django.db.models import Q


def phonebook_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        users = User.objects.filter(Q(user_name__icontains=search_query) | Q(user_surname__icontains=search_query) | Q(user_email__icontains=search_query))
    else:
        users = User.objects.all().order_by("user_name")

    #  in process
    # paginator = Paginator(users, 1)
    # page = paginator.get_page(1)

    return render(request, 'phonebook/index.html', context={'users': users})


class UserDelete(View):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        return render(request, 'phonebook/user_delete.html', context={'user': user})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return redirect('phonebook')


class UserUpdate(View):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        phonenumber = PhoneNumber.objects.filter(phonenumber_user=pk)
        # print(phonenumber)
        user_form = UserForm(instance=user)
        return render(request, 'phonebook/user_update.html', context={'user_form': user_form, 'user': user})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user_form = UserForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form = user_form.save()
            return redirect('phonebook')
        else:
            return render(request, 'phonebook/user_update.html', context={'user_form': user_form, 'user': user})


class UserCreate(View):
    def get(self, request):
        user = UserForm()
        phonenumber = PhoneNumberForm()
        return render(request, 'phonebook/user_create.html', context={'user': user, 'phonenumber': phonenumber})

    def post(self, request):
        user = UserForm(request.POST)
        phonenumber = PhoneNumberForm(request.POST)
        if user.is_valid() and phonenumber.is_valid():
            new_userform = user.save()
            new_phonenumber = phonenumber.save(commit=False)
            new_phonenumber.phonenumber_user = User.objects.get(pk=new_userform.pk)
            # print(new_phonenumber)
            new_phonenumber.save()
            return redirect('phonebook')
        else:
            return render(request, 'phonebook/user_create.html', context={'user': user, 'phonenumber': phonenumber})
