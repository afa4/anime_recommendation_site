from django.shortcuts import render
from django.http import HttpResponse
import os
import requests
import json


def index(request):
    return render(request, "malprofile/index.html")


def anime_submit(request):
    profile_name = request.POST['profile_name']
    print(profile_name)
    get_top_three_profile_animes(profile_name)
    recommendations = []
    for anime in get_top_three_profile_animes(profile_name):
        anime_name = anime['node']['title']
        recommendations.append(get_recommendation_from_api(anime_name, 10))
    
    return HttpResponse(json.dumps(recommendations), content_type='application/json')


def get_top_three_profile_animes(profile_name):
    token = os.environ.get("MAL_API_TOKEN")
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(f'https://api.myanimelist.net/v2/users/{profile_name}/animelist?sort=list_score&status=completed', headers=headers)

    if response.status_code == 200:
        data = response.json()['data']
        top_three_animes = data[:3]
        return top_three_animes
    else:
        return []


def get_recommendation_from_api(anime_name, recommendation_length = 20):
    url = os.environ.get("API_URL")
    response = requests.get(f'{url}/recommendation?anime_name={anime_name}&length={recommendation_length}')

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(response.__str__())
        print(response.status_code)
        print("Failed to retrieve data")
        return None
