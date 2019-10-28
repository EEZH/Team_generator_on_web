MENU_WITHOUT_SESSION = [
    {'name': 'Регистрация', 'ref': '/sign_up/'},
    # {'name': 'Главная', 'ref': '/home/'}
]

MENU_WITH_SESSION = [
    {'name': 'Главная', 'ref': '/'},
    {'name': 'Сформировать команды', 'ref': '/team_gen/'},
    {'name': 'Наши футболисты', 'ref': '/players/'},
    {'name': 'Выйти', 'ref': '/logout/'}
]

MENU_WITH_SESSION_ADMIN = [
    {'name': 'Главная', 'ref': '/'},
    {'name': 'Сформировать команды', 'ref': '/team_gen/'},
    {'name': 'Наши футболисты', 'ref': '/players/'},
    {'name': 'Добавить игрока', 'ref': '%'},
    {'name': 'Выйти', 'ref': '/logout/'}
]