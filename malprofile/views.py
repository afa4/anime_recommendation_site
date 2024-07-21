from django.shortcuts import render
from django.http import HttpResponse
import os
import requests
import json
import re


def index(request):
    return render(request, "malprofile/index.html")


def anime_submit(request):
    profile_name = request.POST['profile_name']
    top_three = get_top_three_profile_animes(profile_name)
    recommendations = []
    top_three_names = []
    for anime in top_three:
        anime_name = anime['node']['title']
        top_three_names.append(anime_name)
        recommendations_from_api = get_recommendation_from_api(anime_name, 5)
        if recommendations_from_api is None:
            continue
        for item in recommendations_from_api:
            recommendations.append({
                "anime_name": item,
            })
    # todo include anime thumb in final list
    response = {
        "top_three": top_three_names,
        "recommendations": recommendations
    }
    return HttpResponse(json.dumps(response), content_type='application/json')


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
        log_error(response)     


def get_recommendation_from_api(anime_name, recommendation_length = 20):
    url = os.environ.get("API_URL")
    response = requests.get(f'{url}/recommendation?anime_name={anime_name}&length={recommendation_length}')

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        log_error(response)
        return None


def get_anime_metadata(anime_name):
    url = os.environ.get("API_URL")
    response = requests.get(f'https://api.myanimelist.net/v2/anime?q={anime}&limit=1')

    if response.status_code == 200:
        data = response.json()['data'][0]
        return data
    else:
        log_error(response)
        return None


def log_error(response):
    print(response.__str__())
    print(response.status_code)
    print("Failed to retrieve data")
