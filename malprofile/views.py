from django.shortcuts import render
from django.http import HttpResponse
import os
import requests


def index(request):
    return render(request, "malprofile/index.html")


def anime_submit(request):
    anime_name = request.POST['anime_name']
    print(anime_name)
    recommendation = get_recommendation_from_api(anime_name)
    return HttpResponse(recommendation)


def get_recommendation_from_api(anime_name):
    url = os.environ.get("API_URL")
    response = requests.get(f'{url}/recommendation?anime_name={anime_name}')

    if response.status_code == 200:
        # Assuming the response is JSON
        data = response.json()
        return data
    else:
        print(response.__str__())
        print(response.status_code)
        print("Failed to retrieve data")
        return None
