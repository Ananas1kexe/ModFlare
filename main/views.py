import requests
from django.shortcuts import render, redirect
from django_ratelimit.decorators import ratelimit
from django.conf import settings
import logging

# Create your views here.


logger = logging.getLogger(__name__)

@ratelimit(key='ip', rate='5/s', method=['GET', 'POST'], block=True)
def index(request):
    return render(request, 'main/index.html')

@ratelimit(key='ip', rate='5/s', method=['GET', 'POST'], block=True)
def user_info(request):
    return render(request, 'main/user_info.html')


def discord_login(request):
    discord_auth_url = (
        f'https://discord.com/api/oauth2/authorize'
        
        f'?client_id={settings.DISCORD_CLIENT_ID}'
        f"&redirect_uri={settings.DISCORD_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=identify email guilds guilds.members.read"
    )
    return redirect(discord_auth_url)


def discord_callback(request):
    code = request.GET.get("code")
    
    if not code:
        logger.error("Ошибка: Код авторизации не получен.")
        return redirect("discord_login")

    token_url = f"{settings.DISCORD_API_BASE_URL}/oauth2/token"
    data = {
        "client_id": settings.DISCORD_CLIENT_ID,
        "client_secret": settings.DISCORD_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.DISCORD_REDIRECT_URI,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(token_url, data=data, headers=headers)
    if response.status_code != 200:
        logger.error(f"Ошибка запроса токена: {response.status_code} {response.text}")
        return redirect("discord_login")

    access_token = response.json().get("access_token")
    if not access_token:
        logger.error("Ошибка: Токен авторизации не получен.")
        return redirect("discord_login")

    user_url = f"{settings.DISCORD_API_BASE_URL}/users/@me"
    headers = {"Authorization": f"Bearer {access_token}"}
    user_response = requests.get(user_url, headers=headers)

    if user_response.status_code != 200:
        logger.error(f"Ошибка запроса данных пользователя: {user_response.status_code} {user_response.text}")
        return redirect("discord_login")

    user_data = user_response.json()
    request.session["user"] = {
        "id": user_data["id"],
        "username": user_data["username"],
        "avatar": user_data["avatar"],
        "discriminator": user_data["discriminator"],
        "email": user_data.get("email", ''),
        "guilds ": user_data.get("guilds", []),

    }

    return redirect("/")

def logout_view(request):
    """Выход пользователя (очистка сессии)."""
    request.session.flush()
    return redirect("/")
