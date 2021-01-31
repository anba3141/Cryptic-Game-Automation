from selenium import webdriver
import time
import random


driver = webdriver.Chrome('/chromedriver')
driver.get("https://cryptic-game.net")


def timer(a: float, b: float):
    time.sleep(random.randint(int(a*10000), int(b*10000))/10000)


def login(username, password):
    time.sleep(random.randint(1, 3))
    play_button = driver.find_element_by_xpath('//*[@id="__layout"]/div/main/div/nav/div[1]')
    try:
        play_button.click()
    except:
        pass

    timer(1, 3)
    driver.find_element_by_xpath('//*[@id="__layout"]/div/main/div/nav/div[2]/div/div/a[2]').click()

    timer(1, 3)

    driver.switch_to.window(driver.window_handles[-1])

    username_login = driver.find_element_by_xpath('//*[@id="animation-container"]/app-login/app-account-page-base/div/div[1]/div/form/label[1]/input')
    passwort_login = driver.find_element_by_xpath('//*[@id="animation-container"]/app-login/app-account-page-base/div/div[1]/div/form/label[2]/input')
    timer(1, 5)
    username_login.send_keys(username)
    timer(2, 5)
    passwort_login.send_keys(password)
    timer(2, 5)
    driver.find_element_by_xpath('//*[@id="animation-container"]/app-login/app-account-page-base/div/div[1]/div/form/label[3]/input').click()
    time.sleep(2)


def open_pc(pc: int):
    driver.find_element_by_xpath('//*[@id="sidebar-container"]/app-control-center-sidebar-menu[1]').click()
    timer(1, 2)
    driver.find_element_by_xpath(f'//*[@id="sidebar-container"]/app-control-center-sidebar-menu[1]/div/div[2]/div[{pc}]').click()
    timer(1, 2)
    driver.find_element_by_xpath('//*[@id="control-center"]/div/div[2]/div/app-control-center-device-page/div[1]/img[1]').click()


def open_terminal():
    timer(1, 2)
    app_button = driver.find_element_by_xpath('//*[@id="startbutton"]')
    app_button.click()
    timer(1, 2)
    terminal_button = driver.find_element_by_xpath('//*[@id="linkages"]/div[3]')
    terminal_button.click()


class Command:
    def __init__(self, command: str):
        self.command = command
        self.is_send = False
        self.response = None
        self.sent = None

    def send(self):
        timer(4, 6)
        command_line = driver.find_element_by_xpath('//*[@id="cmdline"]')
        command_line.send_keys(self.command+"\n")
        self.is_send = True
        timer(0.5, 1)
        self.response = driver.find_element_by_xpath('//*[@id="terminal-history"]').text.split(
            driver.find_elements_by_xpath('//*[@id="prompt"]')[-1].text)[-1].split("\n")
        self.sent = self.response.pop(0)


def close_terminal():
    timer(1, 2)
    while True:
        try:
            Command("exit").send()
        except:
            break
    timer(1, 2)


def get_uuid(cmd :Command):  # cmd has to be send as spot before
    return cmd.response[1].split(" ")[1]


def get_ssh(cmd :Command):  # cmd has to be send as spot before
    return cmd.response[3].split(" ")[1][1:-1]
