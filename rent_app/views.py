from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse,Http404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_protect   
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Iha, RentRecord
from .forms import IhaCreateUpdateForm, IhaUpdateForm, IhaRentForm
from .serializers import RentRecordListSerializer, UserSerializer
from rest_framework import status

class WelcomePageView(generic.TemplateView):
    template_name = 'rent/layout.html'

# this view list all the iha.
class HomePageView(generic.ListView):
    template_name = 'rent/homepage.html'
    model = Iha
    context_object_name ='iha'

# this view create user account.
class RegisterView(APIView):
    def get(self, request):
        return render(request,"rent/register.html")
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# this view to login website.
class LoginView(APIView):
    def get(self, request):
        return render(request, "rent/login.html")
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        print(request.data)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            return Response({'message': 'Login successful', 'redirect_url': reverse('home-page')})
        else:
            return Response({'message': 'There is no user'}, status=status.HTTP_400_BAD_REQUEST)

# this view to logout website.
class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'Logout successful','redirect_url': reverse('layout')}, status=200)
    

# this view to create another iha.
class IhaCreateView(CreateView):
    model = Iha
    form_class = IhaCreateUpdateForm
    template_name = 'rent/addIha.html'
    success_url = reverse_lazy('home-page')

# this view to update existing iha.
class IhaUpdateView(UpdateView):
    model = Iha
    form_class = IhaCreateUpdateForm
    template_name = 'rent/updateIha.html'
    success_url = reverse_lazy('home-page')

# this view to delete iha.
def iha_delete_view(request,id):
    posts = Iha.objects.get(id=id)
    posts.delete()
    return redirect("/home")

# this view to create rent record for iha.
class RentalRecordCreateView(CreateView):
    template_name = 'rent/createRent.html'
    form_class = IhaRentForm
    success_url = reverse_lazy('home-page')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.initial['user_rent'] = self.request.user
        return form

# this view to rent list.
class RentRecordListView(generic.ListView):
    template_name = 'rent/rentRecord.html'
    model = RentRecord
    context_object_name ='rent_record'


class RentRecordApiV(ListAPIView):
    
    serializer_class = RentRecordListSerializer
    queryset = RentRecord.objects.all()




# this view to update rent.
class RentRecordUpdateView(UpdateView):
    model = RentRecord
    form_class = IhaRentForm
    template_name = 'rent/rentUpdate.html'
    success_url = reverse_lazy('rent-list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.initial['user_rent'] = self.request.user
        form.fields['user_rent'].disabled = False
        return form
    
# this view to delete rent.
def rent_delete_view(request,id):
    posts = RentRecord.objects.get(id=id)
    posts.delete()
    return redirect("/rent")

# this view list to user's rent.
class UserRentRecordView(LoginRequiredMixin, generic.ListView):
    model = RentRecord
    template_name = 'rent/userRentList.html'
    success_url = reverse_lazy('home-page')
    context_object_name ='user_rent_record'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_rent=self.request.user)
    

