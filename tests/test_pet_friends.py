from api import PetFriends
from settings import valid_email, valid_password, not_valid_password, not_valid_email
import os


pf = PetFriends()


# Тест получения ключа API
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


# Тест проверки списка питомцев
def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


# Тест создания питомца
def test_add_new_pet_with_valid_data(name='Граф', animal_type='дог',
                                     age='2', pet_photo='images/foto1.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

# Тест удаления питомца
def test_successful_delete_self_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Барон", "пес", "3", "images/foto1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()


# Тест обновления информации о питомце
def test_successful_update_self_pet_info(name='Бади', animal_type='питбуль', age=5):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


# Тест создания питомца без фото
def test_add_new_pet_without_photo_valid_data (name='Рик', animal_type='стаффорд', age='1'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


# Тест добавления фото питомца
def test_post_add_new_photo_of_pet (pet_photo='images/foto2.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.post_add_new_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 200
        assert 'pet_photo' in result
    else:
        raise Exception("There is no my pets")


# Тест авторизации с неверным Email
def test_authorization_with_not_correct_email(email=not_valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result


# Тест авторизации с неверным паролем
def test_authorization_with_not_correct_password(email=valid_email, password=not_valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result


# Тест создания питомца с отрицательным возрастом
def test_creating_a_pet_with_negative_age(name='Чарли', animal_type='такса', age='-5', pet_photo='images/foto1.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert age<'0'


# Тест создания питомца с слишком большим возрастом
def test_creating_a_pet_that_is_too_old (name='Дон', animal_type='терьер', age='999', pet_photo='images/foto1.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert age>'99'


# Тест создания питомца без имени
def test_creating_a_pet_without_a_name(name='', animal_type='терьер', age='2', pet_photo='images/foto1.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == ''


# Тест создания питомца с именем из символов
def test_creating_a_pet_with_a_name_from_symbols (name='!"№%;', animal_type='терьер', age='2', pet_photo='images/foto1.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == '!"№%;'


# Тест создания питомца без возроста
def test_creating_a_pet_without_age(name='Джон', animal_type='дог', age='', pet_photo='images/foto1.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['age'] == ''


# Тест создания питомца без породы
def test_creating_a_pet_without_a_breed(name='Бьерк', animal_type='', age='5', pet_photo='images/foto1.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['animal_type'] == ''