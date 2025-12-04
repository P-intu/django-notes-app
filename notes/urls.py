from django.urls import path
from . import views
urlpatterns=[
    path('',views.home,name='notes_home'),
    path('/firstpage',views.firstpage,name='firstpage'),
    path('login/',views.login_user,name='login'),
    path('signup/',views.signup_user,name='signup'),
    path('logout/',views.logout_user,name='logout'),
    path('view_note/<int:id>/',views.view_note,name='view'),
    path('add_note/',views.add_note,name='add_note'),
    path('note/<int:id>/edit/',views.edit_note,name='edit_note'),
    path('note/<int:id>/delete/',views.delete_note,name='delete_note'),
    path('note/<int:id>/pin/',views.toggle_pin,name='toggle_pin'),

]