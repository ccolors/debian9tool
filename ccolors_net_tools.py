import subprocess
import re
import sys
import fileinput
#import requests
import time
import os

#def check_internet():
#    url = 'http://google.com'
#    timeout = 5
#    try:
#        _ = requests.get(url, timeout=timeout)
#        return True
#    except requests.ConnectionError:
#        print("Khong the ket noi Internet")
#
#return False

def view_interface():
    subprocess.call("ifconfig", shell=True)

def view_only_interface():
    input_interface = input("[-] Nhap interface: ")
    subprocess.call(["ifconfig", input_interface])

def shutdown():
    subprocess.call('init 0', shell=True)

def reboot():
    subprocess.call('reboot', shell=True)

def net_work_card_restart():
    subprocess.call("systemctl restart networking", shell=True)

def command_input():
    command = input("[-] Nhap lenh: ")
    subprocess.call(command, shell=True)

def string_search(file_name, str_input):
    file = open(file_name, 'r')
    str_temple = file.read()
    str_target = re.search(str_input, str_temple)
    file.close()
    return str_target.group(0)

def replaceAll(file_name, searchExp, replaceExp):
    for line in  fileinput.input(file_name, inplace=1):
        if searchExp in line:
            line = line.replace(searchExp, replaceExp)
        sys.stdout.write(line)

def show_hosts():
    output1_result = subprocess.getoutput("cat /etc/hosts")
    print("""=============================
{0}
=============================""".format(output1_result))

def update_source_list():
    input_require = input("[-] Ban co muon update source list khong (N/y) ?")
    if input_require in ("y", "Y"):
        subprocess.call("cp sources.list /etc/apt/sources.list", shell=True)
        subprocess.call("apt-get update", shell=True)
    else:
        pass

def remove_host():
    while True:
        input_choice = input("[-] Ban co muon xoa them host khong(n)? ")
        if input_choice in ('y', 'Y'):
            input_ip_host = input("[-] Nhap ip host can xoa: ")
            if input_ip_host:
                host_result = string_search("/etc/hosts", "{0}.*".format(input_ip_host))
                replaceAll("/etc/hosts", host_result, '')
                show_hosts()
            else:
                pass
        else:
            break

def change_hostname():
    os.system('clear')
    show_hosts()
    while True:
        input_change_hosts = input("[+] Ban co muon them host khong (n)? ")
        if input_change_hosts in ('y', 'Y'):
            input_hosts = input("\t[-] Nhap host (vd: sv.cuong.local): ")
            i = 0
            for k in input_hosts:
                if k == '.':
                    break
                else:
                    i += 1
            hostname = input_hosts[:i]
            input_ip_host = input("\t[-] Nhap ip cua host (vd: 192.168.1.1): ")
            output_result = string_search("/etc/hosts", "127.*")
            replaceAll("/etc/hosts", output_result, "{0}\n{1}\t{2}\t{3}".format(output_result, input_ip_host, input_hosts, hostname))
        else:
            break

def replaceAll(file_name, searchExp, replaceExp):
    for line in fileinput.input(file_name, inplace=1):
        if searchExp in line:
            line = line.replace(searchExp, replaceExp)
        sys.stdout.write(line)

def string_search(file_name, str_input):
    file = open(file_name, 'r')
    str_temple = file.read()
    str_target = re.search(str_input, str_temple)
    file.close()
    return str_target.group(0)

def allow_forwarding_traffic():
    input_continue = input("[+] Ban co muon chuyen tiep luu luong mang khong (n)?: ")
    if input_continue in ('y', 'Y'):
        output_result = string_search("/etc/sysctl.conf", ".*net.ipv4.ip_forward=1.*")
        replaceAll("/etc/sysctl.conf", output_result, "net.ipv4.ip_forward=1")
        subprocess.call("sysctl -p /etc/sysctl.conf", shell=True)
        subprocess.call("systemctl restart networking", shell=True)
    else:
        pass

def disable_forwarding_traffic():
    input_continue = input("[+] Ban co muon vo hieu hoa chuyen tiep luu luong khong (n)?: ")
    if input_continue in ('y', 'Y'):
        output_result = string_search("/etc/sysctl.conf", ".*net.ipv4.ip_forward=1.*")
        replaceAll("/etc/sysctl.conf", output_result , "#net.ipv4.ip_forward=1")
        subprocess.call("sysctl -p /etc/sysctl.conf", shell=True)
        subprocess.call("systemctl restart networking", shell=True)
    else:
        pass

def update():
    subprocess.call("apt update", shell=True)

def upgrade():
    subprocess.call("apt -y upgrade", shell=True)

def excutable_menu():
    while True:
        count_exceed2 = 0
        while True:
            os.system("clear")
            print("""
        |=|===================================================|=|
        |=|    DEBIAN DEMO TOOLS ARE MADE BY CUONGCOLORS      |=|
        |=|     This software is built for python3.           |=|
        |=|                                                   |=|
        |=|     1. [-] Khoi Dong Lai HDH                      |=|
        |=|     2. [-] Tat He Dieu Hanh                       |=|
        |=|     3  [-] Cap nhat danh sach tai nguyen          |=|
        |=|     4. [-] Lenh                                   |=|
        |=|     5. [-] Thoat                                  |=|
        |=|                                                   |=|
        |=|===================================================|=|
        """)
            try:
                input_tool_choise = input("[-] Nhap vao lua chon: ")
            except ValueError:
                print("[-] Lua chon khong chinh xac, xin nhap lai.[1]")
            choice_list = ['1', '2', '3', '4', "5"]

            if input_tool_choise in choice_list:
                break
            else:
                print("[-] Lua chon khong chinh xac, xin nhap lai.[2]")
                count_exceed2 += 1

            if count_exceed2 > 3:
                print("[-] Ban nhap qua so lan cho phep")
                time.sleep(2)
                sys.exit()
            else:
                pass
            time.sleep(1)

        if input_tool_choise == '1':
            reboot()
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '3':
            update_source_list()
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '2':
            shutdown()
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '4':
            command_input()
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        else:
            break
