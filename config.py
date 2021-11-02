import os
BOT_TOKEN = os.environ['BOT_TOKEN']


ALLOWED_USERS = ()  # внеси сюда telegram ID пользователя(ей)

def wind_dir(num):
    return {
        8592: f'Восточный {chr(8592)}',
        8593: f'Южный {chr(8593)}',
        8594: f'Западный {chr(8594)}',
        8595: f'Северный {chr(8595)}',
        8598: f'Юго-Восточный {chr(8598)}',
        8599: f'Юго-Западный {chr(8599)}',
        8600: f'Северо-Западный {chr(8600)}',
        8601: f'Северо-Восточный {chr(8601)}',
    }.get(num)


if __name__ == '__main__':
    pass
