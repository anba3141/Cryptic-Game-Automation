from cryptic import *

with OpenCryptic("username", "password", "chromedriver path") as cryptic:
    with cryptic.OpenPc(2) as pc:
        with pc.OpenTerminal() as terminal:
            while True:
                spot_cmd = terminal.Command("spot")
                cmd = terminal.Command(f"service bruteforce {spot_cmd.get_device_uuid()} {spot_cmd.get_device_ssh()}")
                timer(19, 23)
                cmd.command = "stop"
                cmd.command = f"connect {spot_cmd.get_uuid()}"
                cmd.command = "miner start c91e8b97-baae-4926-96d4-0d07e5a1c804"
                cmd.command = "miner wallet c91e8b97-baae-4926-96d4-0d07e5a1c804"
                cmd.command = "miner power 100"
                cmd.command = "exit"

