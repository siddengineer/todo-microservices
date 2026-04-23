import requests

def forward_request(request, service_url):
    token = request.session.get("jwt")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(service_url, headers=headers)

    return response.json()