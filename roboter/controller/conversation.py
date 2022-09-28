from roboter.models import robot

def talk_about_restaurant():
    restaurant_robot = robot.RestaurantRobot()
    restaurant_robot.hello()
    restaurant_robot.recommend_menu()
    restaurant_robot.ask_your_favorite()
    restaurant_robot.thank_you()