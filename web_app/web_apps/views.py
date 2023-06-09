from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404


# Create your views here.

def index(request):
    return render(request, "web_apps/index.html")


@login_required
def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by("date_added")
    context = {"topics": topics}
    return render(request=request, context=context, template_name="web_apps/topics.html")


@login_required
def topic(request, topic_id):
    topic_chosen = Topic.objects.get(id=topic_id)
    if topic_chosen.owner != request.user:
        raise Http404
    entries = topic_chosen.entry_set.order_by("-date_added")
    context = {"topic": topic_chosen, "entries": entries}
    return render(request=request, context=context, template_name="web_apps/topic.html")


@login_required
def new_topic(request):
    if request.method != "POST":
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect("web_apps:topics")
    context = {"form": form}
    return render(request, 'web_apps/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    topic_chosen = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry_data = form.save(commit=False)
            new_entry_data.topic = topic_chosen
            new_entry_data.save()
            return redirect('web_apps:topic', topic_id=topic_id)
    context = {'topic': topic_chosen, 'form': form}
    return render(request, 'web_apps/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    entry_chosen = Entry.objects.get(id=entry_id)
    topic_chosen = entry_chosen.topic
    if topic_chosen.owner != request.user:
        raise Http404

    if request.method != "POST":
        form = EntryForm(instance=entry_chosen)
    else:
        form = EntryForm(instance=entry_chosen, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("web_apps:topic", topic_id=topic_chosen.id)
    context = {"entry": entry_chosen, "topic": topic_chosen, "form": form}
    return render(request, 'web_apps/edit_entry.html', context)
