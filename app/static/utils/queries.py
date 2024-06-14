from django.db.models import Q
from django.db.models import Value as V
from django.db.models.functions import Concat   


def ItemQuery(searched, searchby, Item):
    if (searched is None or searched == ""):
        queryset = Item.objects.all().order_by('-alert', 'title')
    elif searchby=="all":
        # add other featuers
        queryset = Item.objects.annotate(full_search=Concat('title', V(' '), 'part_number')).\
                filter(full_search__icontains=searched).order_by('-alert', 'title')
        # queryset = Item.objects.filter(Q(title__icontains=searched) | Q(part_number__icontains=searched)).order_by('-alert', 'title')
    elif searchby=="name":
        queryset = Item.objects.filter(title__icontains=searched).order_by('-alert', 'title')
    elif searchby=="part":
        queryset = Item.objects.filter(part_number__icontains=searched).order_by('-alert', 'title')
    return queryset

def PersonQuery(searched, searchby, Person):
    if (searched is None or searched == ""):
        queryset = Person.objects.all().order_by('username', 'first_name')
    elif searchby=="all":
        # add other featuers
        queryset = Person.objects.filter(Q(title__icontains=searched) | Q(title__icontains=searched)).order_by('username', 'first_name')
    elif searchby=="name":
        queryset = Person.objects.filter(title__icontains=searched).order_by('username', 'first_name')
    elif searchby=="part":
        queryset = Person.objects.filter(part_number__icontains=searched).order_by('-alert', 'title')
    return queryset