from django.shortcuts import render
from .models import Topic


# Create your views here.

def index(request):
    return render(request, "web_apps/index.html")


def topics(request):
    topics_ordered = Topic.objects.order_by("date_added")
    context = {"topics": topics_ordered}
    return render(request=request, context=context, template_name="web_apps/topics.html")


def topic(request, topic_id):
    topic_chosen = Topic.objects.get(id=topic_id)
    entries = topic_chosen.entry_set.order_by("-date_added")
    context = {"topic": topic, "entries": entries}
    return render(request=request, context=context, template_name="web_apps/topic.html")
