from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm, SearchForm
from django.http import Http404
# Create your views here.

def check_owner(topic, current_user):
    if topic.owner != current_user:
        raise Http404


def index(request):
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """Show all topics"""
    #topics = Topic.objects.order_by('date_added')
    topics = Topic.objects.filter(owner = request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """Show a single topic and all its entries."""
    topic = Topic.objects.get(id =topic_id)
    #Make sure the topic belongs to the current user.
    # if topic.owner != request.user:
    #     raise 
    check_owner(topic, request.user)
    
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """Add a new topic"""
    if request.method != 'POST':
        #No data submitted; create a blank form.
        form = TopicForm()
    else:
        #POST data submitted; process data
        form = TopicForm(data = request.POST)
        if form.is_valid():
            new_topic = form.save(commit= False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')
    #Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Add a new entry for a particular topic"""
    topic = Topic.objects.get(id = topic_id)

    check_owner(topic, request.user)

    if request.method != 'POST':
        #No data submitted; create a blank form.
        form = EntryForm()
    else:
        #POST data submitted; process data
        form  = EntryForm(data= request.POST)
        if form.is_valid():
            new_entry = form.save(commit= False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id = topic_id)
    #Display a blank or invalid form.
    context = {'topic':topic, 'form':form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry"""
    entry = Entry.objects.get(id = entry_id)
    topic = entry.topic

    #Make sure entry is associated to the user
    # if topic.owner != request.user:
    #     raise Http404
    check_owner(topic, request.user)
    if request.method != 'POST':
        #Initial request; pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
        #POST data submitted; process data
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id = topic.id)
    context = {'entry':entry, 'topic':topic, 'form':form}
    return render(request, 'learning_logs/edit_entry.html', context)

def edit_topic(request, topic_id):
    """Edit an existing topic"""
    topic = Topic.objects.get(id = topic_id)
    check_owner(topic, request.user)
    if request.method != 'POST':
        #Initial request; pre-fill form with current topic
        form = TopicForm(instance= topic)
    else:
        #Post data submitted; process data
        form = TopicForm(instance=topic, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id =topic.id)
    context = {'topic':topic, 'form':form}
    return render(request, 'learning_logs/edit_topic.html', context)
        


def search_topic(request, topic_id):
    topic = Topic.objects.get(id= topic_id)
    if topic.ownner != request.user:
        print('No related topic')
    if request.method != 'POST':
        form = SearchForm
    else:
        form = SearchForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id)
    context = {'topic':topic, 'form':form}
    return render(request, 'learning_logs/base.html', context)



