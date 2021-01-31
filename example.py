from cryptic import *

login("username", "password")
open_pc(2)
open_terminal()
hacked = 0
while True:
    spot_cmd = Command("spot")
    spot_cmd.send()
    cmd = Command("service bruteforce "+get_uuid(spot_cmd)+" "+get_ssh(spot_cmd))
    cmd.send()
    cmd = Command("stop")
    timer(21, 25)
    cmd.send()
    cmd = Command("connect "+get_uuid(spot_cmd))
    cmd.send()
    cmd = Command("miner start c91e8b97-baae-4926-96d4-0d07e5a1c804")
    cmd.send()
    cmd = Command("miner wallet c91e8b97-baae-4926-96d4-0d07e5a1c804")
    cmd.send()
    cmd = Command("miner power 100")
    cmd.send()
    cmd = Command("exit")
    cmd.send()
    timer(0, 2)
    hacked += 1
    print(hacked, "people Hacked so far")
