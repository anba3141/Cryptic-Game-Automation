from selenium import webdriver
import time
import random
from typing import Callable, Optional

close_functions = {"Terminal": False, "OpenCryptic": False, "OpenPc": False}


def timer(a: float, b: float):
    time.sleep(random.randint(int(a * 10000), int(b * 10000)) / 10000)


class OpenCryptic:
    def __init__(self, username, password, chromedriver_location):
        self.cryptic = _Cryptic(username, password, chromedriver_location)

    def __enter__(self):
        return self.cryptic

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cryptic.close(exc_type, exc_val, exc_tb)
        if close_functions["OpenCryptic"]:
            close_functions["OpenCryptic"](exc_type, exc_val, exc_tb)


class _Cryptic:
    def __init__(self, username, password, chromedriver_location):
        self.driver = webdriver.Chrome(chromedriver_location)
        self.driver.get("https://cryptic-game.net")
        time.sleep(random.randint(1, 3))
        play_button = self.driver.find_element_by_xpath('//*[@id="__layout"]/div/main/div/nav/div[1]')
        try:
            play_button.click()
        except:
            pass

        timer(1, 3)
        self.driver.find_element_by_xpath('//*[@id="__layout"]/div/main/div/nav/div[2]/div/div/a[2]').click()

        timer(1, 3)

        self.driver.switch_to.window(self.driver.window_handles[-1])

        username_login = self.driver.find_element_by_xpath(
            '//*[@id="animation-container"]/app-login/app-account-page-base/div/div[1]/div/form/label[1]/input')
        passwort_login = self.driver.find_element_by_xpath(
            '//*[@id="animation-container"]/app-login/app-account-page-base/div/div[1]/div/form/label[2]/input')
        timer(1, 5)
        username_login.send_keys(username)
        timer(2, 5)
        passwort_login.send_keys(password)
        timer(2, 5)
        self.driver.find_element_by_xpath(
            '//*[@id="animation-container"]/app-login/app-account-page-base/div/div[1]/div/form/label[3]/input').click()
        time.sleep(2)

    def close(self, exc_type, exc_val, exc_tb):
        self.driver.quit()

    def OpenPc(self, pc: int):
        return self._OpenPc(pc, self.driver)

    class _OpenPc:
        def __init__(self, pc: int, driver):
            self.pc = _Pc(pc, driver)

        def __enter__(self):
            return self.pc

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.pc.close()
            if close_functions["OpenPc"]:
                close_functions["OpenPc"](exc_type, exc_val, exc_tb)

    def exit(self):
        self.driver.close()


class _Pc:
    def __init__(self, pc: int, driver):
        self.driver = driver
        self.driver.find_element_by_xpath('//*[@id="sidebar-container"]/app-control-center-sidebar-menu[1]').click()
        timer(1, 2)
        self.driver.find_element_by_xpath(
            f'//*[@id="sidebar-container"]/app-control-center-sidebar-menu[1]/div/div[2]/div[{pc}]').click()
        timer(1, 2)
        self.driver.find_element_by_xpath(
            '//*[@id="control-center"]/div/div[2]/div/app-control-center-device-page/div[1]/img[1]').click()

    def close(self):
        timer(1, 2)
        self.driver.find_element_by_xpath('//*[@id="cc-button"]').click()
        timer(1, 2)

    def OpenTerminal(self):
        return self._OpenTerminal(self.driver)

    class _OpenTerminal:
        def __init__(self, driver):
            self.terminal = _Terminal(driver)

        def __enter__(self):
            return self.terminal

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.terminal.close()
            if close_functions["Terminal"]:
                close_functions["Terminal"](exc_type, exc_val, exc_tb)


class _Terminal:
    def __init__(self, driver):
        self.driver = driver
        timer(1, 2)
        app_button = self.driver.find_element_by_xpath('//*[@id="startbutton"]')
        app_button.click()
        timer(1, 2)
        terminal_button = self.driver.find_element_by_xpath('//*[@id="linkages"]/div[3]')
        terminal_button.click()

    def close(self):
        timer(1, 2)
        while True:
            try:
                self.Command("exit").send()
            except:
                break
        timer(1, 2)

    def Command(self, command: str, direct_send=True):
        return self._Command(command, self.driver, direct_send)

    class _Command:
        def __init__(self, command: str, driver, direct_send=True):
            self.is_send = False
            self.driver = driver
            self.direct_send = direct_send
            self.response = None
            self.sent = None
            self.command = command

        @property
        def command(self):
            return self._command

        @command.setter
        def command(self, value: str):
            self._command = value
            if self.direct_send:
                self.send()

        def send(self):
            timer(1.5, 2)
            command_line = self.driver.find_element_by_xpath('//*[@id="cmdline"]')
            command_line.send_keys(self.command + "\n")
            self.is_send = True
            timer(7, 8)
            self.response = self.driver.find_element_by_xpath('//*[@id="terminal-history"]').text.split(
                self.driver.find_elements_by_xpath('//*[@id="prompt"]')[-1].text)[-1].split("\n")
            self.sent = self.response.pop(0)

        def get_device_uuid(self):  # cmd has to be send as spot before
            if self.is_send and self.command == "spot":
                return self.response[1].split(" ")[1]
            return None

        def get_device_ssh(self):  # cmd has to be send as spot before
            if self.is_send and self.command == "spot":
                return self.response[3].split(" ")[1][1:-1]
            return None


def terminal_close(f: Callable[..., None]):
    close_functions["Terminal"] = f
    return f


def open_cryptic_close(f: Callable[..., None]):
    close_functions["OpenCryptic"] = f
    return f


def open_pc_close(f: Callable[..., None]):
    close_functions["OpenPc"] = f
    return f
