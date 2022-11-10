from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import serializers
from rest_framework import status
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .serializers import AppVersionSerializer, AppEnvironmentSerializer, AppNameSerializer, AppVersionDeserializer
from .models import AppVersion, AppEnvironment, AppName

class Item(AppVersion):
    name = AppVersion.name
    version = AppVersion.version
    deploy_date = AppVersion.deploy_date

@api_view(['GET'])
def ApiView(request):
    urls = {
        'AppVersion': 'api/AppVersion',
        'AppEnvironment': 'api/AppEnvironment',
        'AppName': 'api/AppName',
        'AppHistory': 'api/AppHistory',
        'AppCurrentDeploys': 'api/AppCurrentDeploys',
    }
    return Response(urls)



def index(request):
    environments = AppEnvironmentSerializer(AppEnvironment.objects.all(), many=True).data
    app_names = AppNameSerializer(AppName.objects.all(), many=True).data
    versions, slug_versions = get_latest_versions()
    return render(request, 'index.html', {'environments': environments, 'app_names': app_names, 'slug_versions': slug_versions})

@csrf_exempt
def ApiAppVersionView(request):
    if request.method == 'GET':
        items, ignore = get_latest_versions()
        serializer = AppVersionSerializer(items, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AppVersionDeserializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def ApiAppEnvironmentView(request):
    if request.method == 'GET':
        items = AppEnvironment.objects.all()
        serializer = AppEnvironmentSerializer(items, many=True)
        return JsonResponse(serializer.data, safe=False)
    # Intentionally locking post behind django admin view to
    # enable only admin to add new environments

@csrf_exempt
def ApiAppNameView(request):
    if request.method == 'GET':
        items = AppName.objects.all()
        serializer = AppNameSerializer(items, many=True)
        return JsonResponse(serializer.data, safe=False)
    # Intentionally locking post behind django admin view to
    # enable only admin to add new app names

@csrf_exempt
def ApiAppHistoryView(request):
    #returns all deployments for an app_name and environment sorted by deploy_date
    if request.method == 'GET':
        data = JSONParser().parse(request)
        appname = data['name']
        environment = data['environment']
        items = AppVersion.objects.all().filter(name__app_name=appname, environment__env_name=environment).order_by('-deploy_date')
        serializer = AppVersionSerializer(items, many=True)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def ApiAppCurrentDeploysView(request):
    #returns all current deployments for an app_name
    if request.method == 'GET':
        data = JSONParser().parse(request)
        appname = data['name']
        items, ignore = get_latest_versions()
        data = AppVersionSerializer(items, many=True).data
        #filter out all other apps
        data = [item for item in data if item['name'] == appname]
        return JsonResponse(data, safe=False)

# Returns a list of the latest version of each app
# also returns a dictionary of the the latest versions of each app keyed by slugs of app_name + env_name
def get_latest_versions():
    items = AppVersion.objects.all()
    # This is how I would query if I assumed that the database is postgres
    # items = items.order_by('name', 'environment', '-deploy_date').distinct('name', 'environment')
    # But since I am allowing mysql, I have to do it this way
    items = items.order_by('name', 'environment', '-deploy_date')
    # filter out all but newest deploy date for each name and environment combination
    filtered_items = []
    filtered_items_slugs = []
    #since items is already sorted by deploy_date this returns latest version for each name and environment combination
    for item in items:
        slug = item.name.app_name + item.environment.env_name
        if slug not in filtered_items_slugs:
            filtered_items.append(item)
            filtered_items_slugs.append(slug)
    slug_dict = {}
    for item in filtered_items:
        slug = item.name.app_name + item.environment.env_name
        slug_dict[slug] = { 'name': item.name.app_name, 'environment': item.environment.env_name, 'version': item.version, 'deploy_date': item.deploy_date }
    return filtered_items, slug_dict
