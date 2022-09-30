from roboter.views import console
from roboter.models import ranking

DEFAULT_NAME = '基山'


class Robot(object):
    def __init__(self, restaurant_name=DEFAULT_NAME, user_name='',
                 speaker_color='green'):
        self.restaurant_name = restaurant_name
        self.user_name = user_name
        self.speaker_color = speaker_color

    def hello(self):
        while True:
            template = console.get_template('hello.txt', self.speaker_color)
            user_name = input(template.substitute({
                'restaurant_name': self.restaurant_name
            }))
            if user_name:
                self.user_name = user_name.title()
                break


class RestaurantRobot(Robot):
    def __init__(self, restaurant_name=DEFAULT_NAME):
        super().__init__(restaurant_name=restaurant_name)
        self.ranking_model = ranking.RankingModel()

    def _hello_decorator(func):
        def wrapper(self):
            if not self.user_name:
                self.hello()
            return func(self)
        return wrapper

    @_hello_decorator
    def recommend_menu(self):
        new_recommend_menu = self.ranking_model.get_most_popular()
        if not new_recommend_menu:
            return None

        will_recommend_menus = [new_recommend_menu]
        while True:
            template = console.get_template('greeting.txt', self.speaker_color)
            is_yes = input(template.substitute({
                'restaurant_name': self.restaurant_name,
                'user_name': self.user_name,
                'menu': new_recommend_menu
            }))

            if is_yes.lower() == 'y' or is_yes.lower() == 'yes':
                break

            if is_yes.lower() == 'n' or is_yes.lower() == 'no':
                new_recommend_menu = self.ranking_model.get_most_popular(
                    not_list=will_recommend_menus)
                if not new_recommend_menu:
                    break
                will_recommend_menus.append(new_recommend_menu)

    @_hello_decorator
    def ask_your_favorite(self):
        while True:
            template = console.get_template(
                'which_menu.txt', self.speaker_color)
            menu = input(template.substitute({
                'user_name': self.user_name
            }))
            if menu:
                self.ranking_model.increment(menu, self.user_name)
                break

    @_hello_decorator
    def thank_you(self):
        template = console.get_template('good_by.txt', self.speaker_color)
        print(template.substitute({
            'user_name': self.user_name
        }))
