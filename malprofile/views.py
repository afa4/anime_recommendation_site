from django.shortcuts import render
from django.http import HttpResponse
import os
import requests
import json
import re


def profile(request):
    return render(request, "malprofile/profile.html")


def anime_submit(request):
    profile_name = request.POST['profile_name']
    best_scored = get_best_scored_watched_animes_form_mal(profile_name)
    best_scored_anime_names = []
    for anime in best_scored:
        best_scored_anime_names.append(anime['node']['title'])

    recommendations = get_recommendations_based_on_list(best_scored_anime_names)
    if len(recommendations) == 0:
        context = {
            "error_message": "No recommendations found"
        }
        return render(request, "malprofile/error.html", context)
    
    recommendations_refined = []
    for recommendation in recommendations:
        recommendations_refined.append(refine_recommendation(recommendation))
        
    context = {
        "recommendations": recommendations_refined
    }
    
    return render(request, "malprofile/recommendation.html", context)
    # return HttpResponse(json.dumps(recommendations_refined), content_type="application/json")


def get_best_scored_watched_animes_form_mal(profile_name):
    token = os.environ.get("MAL_API_TOKEN")
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(f'https://api.myanimelist.net/v2/users/{profile_name}/animelist?sort=list_score&status=completed', headers=headers)

    if response.status_code == 200:
        return response.json()['data']
    else:
        log_error(response)     


# gets at least 3 recommendation lists based on the list of animes
def get_recommendations_based_on_list(anime_list):
    recommendation_length = 5
    recommendations_based_on_list = 0
    recommendations = []
    for anime_name in anime_list:
        if recommendations_based_on_list == 3:
            break
        recommendation_based_on_anime = get_recommendation_from_api(anime_name, recommendation_length)
        if recommendation_based_on_anime is None:
            continue
        recommendations.append({
            'watched_anime': f'{anime_name}',
            'recommendation': recommendation_based_on_anime
        })
        recommendations_based_on_list += 1
    return recommendations


def refine_recommendation(recommendation):
    refined_recommendation = []
    watched_anime = recommendation['watched_anime']
    recommendations_based_on_watched = recommendation['recommendation'].keys()
    for item in recommendations_based_on_watched:
        if re.search(watched_anime, item):
            continue
        refined_recommendation.append({'anime_name': item, 'score': recommendation['recommendation'][item]})
    return {
        'watched_anime': recommendation['watched_anime'],
        'recommendation': refined_recommendation
    }


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
