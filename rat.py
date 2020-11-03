import subprocess
import os
import re


def format_data():
    # returns list of IPs of stations (for example [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18])
    x = station_quantity
    while x > 0:
        ips.append(int(ran)+x)
        x -= 1
    ips.reverse()
    ips.pop()


def ping_all():
    with open(os.devnull, "wb") as limbo:
        for computer in range(1, station_quantity):
            ip = station_name+str(ips[0]+computer-1)
            ip = "".join(ip.splitlines()).format(computer)
            result = subprocess.Popen(["ping", "-n", "1", "-w", "100", ip],
                                      stdout=limbo, stderr=limbo).wait()
            if result:
                print(ip + " - off")
            else:
                print(ip + " - ACTIVE")
                s1 = slice(9, 11, 2)
                s2 = slice(10, 11, 2)
                if len(ip) == 10:
                    active_computers.append(ip[s1])
                elif len(ip) == 11:
                    active_computers.append("1"+ip[s2])
    print("Task complete\n")


def ping_selected(computer):
    with open(os.devnull, "wb"):
        ip = station_name + str(ips[0] + int(computer) - 1)
        ip = "".join(ip.splitlines()).format(computer)
        subprocess.call('ping -n 1 -w 100 %s' % ip)
    print("Task complete\n")


def shutdown_all():
    with open(os.devnull, "wb"):
        for computer in range(1, station_quantity):
            ip = station_name+str(ips[0]+computer-1)
            ip = "".join(ip.splitlines()).format(computer)
            subprocess.call('shutdown -s -t 0 /m \\\\%s' % ip)
    print("Task complete\n")


def shutdown_selected(computer):
    with open(os.devnull, "wb"):
        ip = station_name + str(ips[0] + int(computer) - 1)
        ip = "".join(ip.splitlines()).format(computer)
        subprocess.call('shutdown -s -t 0 /m \\\\%s' % ip)
    print("Task complete\n")


def reboot_all():
    with open(os.devnull, "wb"):
        for computer in range(1, station_quantity):
            ip = station_name+str(ips[0]+computer-1)
            ip = "".join(ip.splitlines()).format(computer)
            subprocess.call('shutdown -r -t 0 /m \\\\%s' % ip)
    print("Task complete\n")


def reboot_selected(computer):
    with open(os.devnull, "wb"):
        ip = station_name + str(ips[0] + int(computer) - 1)
        ip = "".join(ip.splitlines()).format(computer)
        subprocess.call('shutdown -r -t 0 /m \\\\%s' % ip)
    print("Task complete\n")


def main():
    print("Remote Access Tool (v1.0) is small app designed to check status of machines in local "
          "network and able to turn off or reboot selected machines.")
    print("\nStartup process initializing: \nPINGING")
    # ping_all()
    print(active_computers)
    print("\nFor more information type 'help'")
    while True:
        mode = input()
        if mode == 'exit':
            break
        elif mode == 'help':
            print("Usage:\n\texit: quit program\n\tping:\n\t\t-all - pings all machines in local network\n\t\t-ip "
                  "<station number> - pings selected machine\n\tshutdown:\n\t\t-all - turns off all machines in local "
                  "network\n\t\t-ip <station number> - shutdown selected machine\n\treboot:\n\t\t-all - reboot all "
                  "machines in local network\n\t\t-ip <station number> - reboot selected machine")
        elif mode == "ping":
            print("Please enter additional argument")
        elif mode == "ping -all":
            ping_all()
        elif mode[:8] == 'ping -ip':
            match = re.search(r'\d+', mode)
            if match:
                ip = match.group()
                ping_selected(ip)
            else:
                print("Wrong ip. Please enter valid ip")
        elif mode == "shutdown":
            print("Please enter additional argument")
        elif mode == "shutdown -all":
            shutdown_all()
        elif mode[:12] == 'shutdown -ip':
            match = re.search(r'\d+', mode)
            if match:
                ip = match.group()
                shutdown_selected(ip)
            else:
                print("Wrong ip. Please enter valid ip")
        elif mode == "reboot":
            print("Please enter additional argument")
        elif mode == "reboot -all":
            reboot_all()
        elif mode[:10] == 'reboot -ip':
            match = re.search(r'\d+', mode)
            if match:
                ip = match.group()
                reboot_selected(ip)
            else:
                print("Wrong ip. Please enter valid ip")
        else:
            print("Wrong mode. Type valid command.")


if __name__ == '__main__':
    data = open("data.txt", "r")
    station_name = data.readline()
    ran = data.readline()
    station_quantity = data.readline()
    station_quantity = int(station_quantity)+1
    data.close()

    ips = []
    active_computers = []
    format_data()
    main()