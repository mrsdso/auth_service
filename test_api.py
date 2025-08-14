
import requests
import json


BASE_URL = "http://localhost:8000"


def test_health():
    """Тест проверки здоровья сервиса"""
    print("=== Тест проверки здоровья ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()


def test_registration():
    """Тест регистрации пользователя"""
    print("=== Тест регистрации ===")
    user_data = {
        "username": "testuser",
        "email": "test@example.com", 
        "password": "testpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()
    
    return response.status_code == 200


def test_login():
    """Тест входа в систему"""
    print("=== Тест входа в систему ===")
    login_data = {
        "username": "testuser",
        "password": "testpassword123"
    }
    
    response = requests.post(
        f"{BASE_URL}/auth/token",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()
    
    if response.status_code == 200:
        return response.json().get("access_token")
    return None


def test_protected_endpoint(token):
    """Тест защищенного endpoint"""
    print("=== Тест защищенного endpoint ===")
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()


def main():
    """Основная функция тестирования"""
    print("Начинаем тестирование API сервиса авторизации...")
    print()
    
    # Проверка здоровья
    test_health()
    
    # Регистрация
    if test_registration():
        # Вход в систему
        token = test_login()
        
        if token:
            # Тест защищенного endpoint
            test_protected_endpoint(token)
        else:
            print("Не удалось получить токен!")
    else:
        print("Регистрация не удалась!")


if __name__ == "__main__":
    main()
