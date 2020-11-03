import subprocess
import os
import npyscreen


def format_data():
    x = station_quantity
    while x > 0:
        ips.append(int(ran)+x)
        x -= 1
    ips.reverse()
    ips.pop()


def ping():
    with open(os.devnull, "wb") as limbo:
        for computer in range(1, station_quantity):
            ip = station_name+str(ips[0]+computer-1)
            ip = "".join(ip.splitlines()).format(computer)
            result = subprocess.Popen(["ping", "-n", "1", "-w", "100", ip],
                                      stdout=limbo, stderr=limbo).wait()
            if result:
                pass
            else:
                s1 = slice(9, 11, 2)
                s2 = slice(10, 11, 2)
                if len(ip) == 10:
                    active_computers.append(ip[s1])
                elif len(ip) == 11:
                    active_computers.append("1"+ip[s2])


def shutdown():
    with open(os.devnull, "wb"):
        for computer in active_computers:
            ip = station_name+str(ips[0]+computer-1)
            ip = "".join(ip.splitlines()).format(computer)
            subprocess.call('shutdown -s -t 0 /m \\\\%s' % ip)


def reboot():
    with open(os.devnull, "wb"):
        for computer in active_computers:
            ip = station_name+str(ips[0]+computer-1)
            ip = "".join(ip.splitlines()).format(computer)
            subprocess.call('shutdown -r -t 0 /m \\\\%s' % ip)


class RatScreen(npyscreen.ActionForm):
    def create(self):
        self.show_aty = 4
        self.add(npyscreen.TitleFixedText, name="Description:", value="Remote Access Tool is small app designed to "
                                                                      "manage machines in local network")
        self.nextrely += 1
        self.add(npyscreen.TitleFixedText, name="Active computers:", value=active_computers,
                 use_two_lines=False, begin_entry_at=19)
        self.add(npyscreen.TitleFixedText, name="LAN station name:", value=station_name,
                 use_two_lines=False, begin_entry_at=19)
        self.add(npyscreen.TitleFixedText, name="Iterate from:", value=ran,
                 use_two_lines=False, begin_entry_at=19)
        self.add(npyscreen.TitleFixedText, name="Stations quantity:", value=station_quantity-1,
                 use_two_lines=False, begin_entry_at=19)
        self.nextrely += 1
        self.option = self.add(npyscreen.TitleSelectOne, max_height=4, name="Choose option",
                               values=["Shutdown", "Reboot"], scroll_exit=True)

    def on_ok(self):
        ok_cancel = npyscreen.notify_ok_cancel("Are you sure you want to execute selected task?", "Warning", editw=2)
        if ok_cancel:
            if self.option.values[self.option.value[0]] == "Shutdown":
                shutdown()
            else:
                reboot()
            self.parentApp.setNextForm(None)
        else:
            self.parentApp.setNextFormPrevious

    def on_cancel(self):
        self.parentApp.setNextForm(None)


class RAT(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', RatScreen, name='Remote Access Tool v1.2', lines=20)


if __name__ == '__main__':
    data = open("data.txt", "r")
    station_name = data.readline()
    station_name = station_name.lower()
    ran = data.readline()
    station_quantity = data.readline()
    station_quantity = int(station_quantity)+1
    data.close()

    ips = []
    format_data()
    active_computers = []
    # ping()
    app = RAT().run()

