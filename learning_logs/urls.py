from django.urls import path
from . import views

app_name = 'learning_logs'
urlpatterns =[
    #Home page
    path('', views.index, name= 'index'),
    #Page that shows all topics
    path('topics/', views.topics, name = 'topics'),
    #Detail page for a single topic
    path('topics/<int:topic_id>/', views.topic, name = 'topic'),

    #Page for adding a new topic
    path('new_topic/', views.new_topic, name ='new_topic'),

    #page for adding a new entry
    path('new_entry/<int:topic_id>/', views.new_entry, name = 'new_entry'),

    #path for editing entry
    path('edit_entry/<int:entry_id>/', views.edit_entry, name = 'edit_entry'),

    #Path for edititng a topic
    path('edit_topic/<int:topic_id>', views.edit_topic, name = 'edit_topic'),

    #path for searching a topic in the search bar
    path('search_topic', views.search_topic, name= 'search_topic')

 ]