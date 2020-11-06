import hashlib
import string
import random

def add_to_env(length):
    with open('.env','w+') as file:
        database_url = 'postgres+psycopg2://{user}:{pw}@{url}/{db}'.format(user ='postgres',pw='enter_your_info_here', url='enter_your_info_here', db ='enter_your_info_here')
        data = file.read()
        file.seek(0)
        all_letters = string.ascii_lowercase
        letter_connect = ''.join(random.choice(all_letters) for i in range(length))
        key = hashlib.sha224(letter_connect[2::].encode('utf-8'))
        file.write(f'SECRET_KEY={key.hexdigest()}\nDATABASE_URL={database_url}'.replace('\n ', '\n'))
        file.truncate()

add_to_env(10)