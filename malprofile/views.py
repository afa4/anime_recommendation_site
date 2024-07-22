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
    
    top_three_anime_names = []
    for anime in top_three:
        top_three_anime_names.append(anime['node']['title'])

    recommendations = get_recommendations_based_on_list(top_three_anime_names)
        
    if len(recommendations) == 0:
        context = {
            "error_message": "No recommendations found"
        }
        return render(request, "malprofile/error.html", context)
    
    final_recommendations = []
    for recommend in recommendations:
        print(recommend)
        for name in top_three_anime_names:
            if re.search(name, recommend):
                should_include = False
                break
            should_include = True
        if should_include:
            final_recommendations.append(recommend)
    
    final_recommendations = list(dict.fromkeys(final_recommendations))
    
    context = {
        "top_three": top_three_anime_names,
        "recommendations": final_recommendations
    }
    return render(request, "malprofile/recommendation.html", context)


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


def get_recommendations_based_on_list(anime_list):
    recommendations = []
    for anime_name in anime_list:
        recommendations_from_api = get_recommendation_from_api(anime_name, 5)
        if recommendations_from_api is None:
            continue
        for item in recommendations_from_api:
            recommendations.append(item)
    return recommendations


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
