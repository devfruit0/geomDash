import random
import pandas
from selenium import webdriver
import time
from webdriver_manager.firefox import GeckoDriverManager
from pynput.keyboard import Key, Controller
import datetime

browser = webdriver.Firefox(executable_path=GeckoDriverManager().install())
keyboard = Controller()

previous_score = 0
score_card = None
instructions = []
chance_of_jump = 0.35
n_score_death = 7
game_number = 0


def space():
    keyboard.press(Key.space)
    time.sleep(0.05)
    keyboard.release(Key.space)


def setup():
    browser.get('https://scratch.mit.edu/projects/105500895/')

    time.sleep(6)

    start_button = browser.find_element_by_class_name('green-flag_green-flag_1kiAo')
    start_button.click()
    print("Click Play")

    time.sleep(5)
    print("Started Level")

    space()

    time.sleep(5)

    global score_card
    score_card = browser.find_element_by_class_name('monitor_value_3Yexa')
    print("Found Score Card")


def load_instructions(name):
    try:
        df = pandas.read_csv('./instructions/' + name + '.csv', header=None)
        print("Loading " + name + " Instruction")
        return df.values.flatten().tolist()
    except Exception:
        print("Creating New Instruction")
        return []


def save_instructions(name):
    df = pandas.DataFrame(instructions)
    df.to_csv('./instructions/' + name + '.csv', index=False, header=False)
    print("Saving to instructions/" + name + ".csv")


def get_random_move():
    if random.random() <= chance_of_jump:
        return 1
    return 0


def play_game():
    global previous_score
    global game_number

    while True:
        score = int(score_card.text)

        if not score == previous_score:
            while score > len(instructions):
                instructions.append(get_random_move())

            if instructions[score - 2] == 1:
                keyboard.release(Key.space)

            if instructions[score - 1] == 1:
                keyboard.press(Key.space)

            if score == 0:
                print("Attempt: " + str(game_number) + ",  Score: " + str(previous_score))
                try:
                    del instructions[-n_score_death:]
                except Exception:
                    instructions.clear()
                break

        previous_score = score


def main():
    setup()
    global instructions
    instructions = load_instructions("Back_On_Track_D12_H16_N4")
    print(instructions)

    while True:
        score = score_card.text

        if int(score) == 1:
            play_game()
            currentDT = datetime.datetime.now()
            # Make a new save every 15 min
            save_instructions("Back_On_Track_D" + str(currentDT.day) + "_H" + str(currentDT.hour) +
                              "_N" + str(round(currentDT.minute / 15)))


if __name__ == "__main__":
    main()
