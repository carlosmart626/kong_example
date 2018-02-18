import os
import requests
import socket

ip_address = socket.gethostbyname(socket.gethostname())
KONG_ADMIN_URL = 'http://localhost:8001/'
SECRET_KEY = os.environ.get('SECRET_KEY')
print(ip_address, SECRET_KEY)


def register_service_kong(service_name, service_url):
    print("register_service_kong")
    API_REGISTER_URL = KONG_ADMIN_URL + 'apis/'
    payload = {
        "hosts": ["localhost"],
        "upstream_url": service_url,
        "name": service_name
    }
    headers = {
        'content-type': "application/json",
    }
    response = requests.post(API_REGISTER_URL, data=payload)
    print(response.text)
    print(response.elapsed.total_seconds())


register_service_kong("django", f"http://{ip_address}:8080/")


def set_plugin_jwt(service_name):
    print("set_plugin_jwt")
    ADD_PLUGIN_URL = KONG_ADMIN_URL + f'apis/{service_name}/plugins/'
    payload = {
        "name": "jwt",
        "config.key_claim_name": "email"
    }
    headers = {
        'content-type': "application/json",
    }
    response = requests.post(ADD_PLUGIN_URL, data=payload)
    print(response.text)
    print(response.elapsed.total_seconds())


set_plugin_jwt("django")


def register_customer(customer_id):
    print("register_customer")
    CREATE_CUSTOMER_URL = KONG_ADMIN_URL + 'consumers/'
    payload = {
        "username": customer_id,
        "custom_id": customer_id
    }
    print(CREATE_CUSTOMER_URL, payload)
    response = requests.post(CREATE_CUSTOMER_URL, data=payload)
    print(response.text)
    print(response.elapsed.total_seconds())


register_customer("carlosmart626@gmail.com")


def create_jwt_authorization(customer_id):
    print("create_jwt_authorization")
    CREATE_JWT_URL = KONG_ADMIN_URL + f'consumers/{customer_id}/jwt/'
    payload = {
        "key": customer_id,
        "secret": SECRET_KEY
    }
    print(CREATE_JWT_URL, payload)
    response = requests.post(CREATE_JWT_URL, data=payload)
    print(response.text)
    print(response.elapsed.total_seconds())


create_jwt_authorization("carlosmart626@gmail.com")
