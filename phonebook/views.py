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
        users = User.objects.filter(Q(user_name__icontains=search_query) | Q(user_surname__icontains=search_query) | Q(user_email__icontains=search_query) | Q(phonenumber__phonenumber_city__icontains=search_query) | Q(phonenumber__phonenumber_mobile__icontains=search_query) | Q(phonenumber__phonenumber_other__icontains=search_query))
    else:
        users = User.objects.all().order_by("user_name")

    # pagination
    paginator = Paginator(users, 3)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    # next and preview
    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = 'page={}'.format(page.previous_page_number())
    else:
        prev_url = ''
    if page.has_next():
        next_url = 'page={}'.format(page.next_page_number())
    else:
        next_url = ''

    context = {
        'page': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url
    }
    return render(request, 'phonebook/index.html', context=context)


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
        user_form = UserForm(instance=user)
        phonenumber = PhoneNumber.objects.all().values()
        print(phonenumber)
        phonenumber_form_obj = []
        for p in phonenumber:
            if int(p['phonenumber_user_id']) == int(pk):
                phonenumber_obj = get_object_or_404(PhoneNumber, pk=p['id'])
                phonenumber_form = PhoneNumberForm(instance=phonenumber_obj)
                phonenumber_form_obj.append(phonenumber_form)
            else:
                pass
        return render(request, 'phonebook/user_update.html', context={'user_form': user_form, 'user': user, 'phonenumber_form_obj': phonenumber_form_obj})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        phonenumber = PhoneNumber.objects.all().values()
        phonenumber_form_obj = []
        user_form = UserForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()
            i = 0
            for p in phonenumber:
                if int(p['phonenumber_user_id']) == int(pk):
                    phonenumber_obj = get_object_or_404(PhoneNumber, pk=p['id'])
                    phonenumber_form = PhoneNumberForm(request.POST, instance=phonenumber_obj)
                    phonenumber_form_obj.append(phonenumber_form)
                    if phonenumber_form.is_valid():
                        new_phonenumber = phonenumber_form.save(commit=False)
                        phonenumber_city_list = request.POST.getlist('phonenumber_city')
                        new_phonenumber.phonenumber_city = phonenumber_city_list[i]
                        phonenumber_mobile_list = request.POST.getlist('phonenumber_mobile')
                        new_phonenumber.phonenumber_mobile = phonenumber_mobile_list[i]
                        phonenumber_other_list = request.POST.getlist('phonenumber_other')
                        new_phonenumber.phonenumber_other = phonenumber_other_list[i]
                        # print(phonenumber_city_list[0 + i])
                        i += 1
                        new_phonenumber.save()
                        # phonenumber_form.save()
                    else:
                        # UserUpdate.get(PhoneNumber, request, pk)
                        pass
            return redirect('phonebook')
        else:
            return render(request, 'phonebook/user_update.html', context={'user_form': user_form, 'user': user, 'phonenumber_form_obj': phonenumber_form_obj})


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
