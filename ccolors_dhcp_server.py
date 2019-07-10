import subprocess
import re
import fileinput
import os
import sys
import time

def install_source():
    subprocess.call("apt-get install -y isc-dhcp-server", shell=True)
    install_result = subprocess.getoutput("apt-get -y install isc-dhcp-server")
    install_result = str(install_result)
    install1_result_search = re.search("Processing triggers for man-db", install_result)
    install2_result_search = re.search("already the newest version", install_result)
    if install1_result_search or install2_result_search:
        return True
    else:
        return False

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

def move_file(source, destination):
    subprocess.call(["mv", source, destination])

def show_dhcpd_conf():
    subprocess.call("cat /etc/dhcp/dhcpd.conf", shell=True)

def dhcp_status():
    output_check_status = subprocess.getoutput("systemctl status isc-dhcp-server")
    output_check_status = str(output_check_status)
    check_result = re.search("Active: active", output_check_status)
    check2_result = re.search("Active: inactive", output_check_status)
    if check_result:
        print("[-] DHCP server ACTIVE")
    elif check2_result:
        print("[-] DHCP Server INACTIVE")
    else:
        print("[-] DHCP Server Failed")

def show_interface_allow():
    search_result = string_search("/etc/default/isc-dhcp-server", "INTERFACESv4=.*")
    interface_search_result = re.search("\".*\"", search_result)
    print(interface_search_result.group(0))

def dhcp_conf():
    print("[-] Dang cai goi...")
    if install_source() == True:
        print("[-] Goi da duoc cai dat")
    else:
        print("""[-] Khong cai duoc goi
Nguyen nhan:
\t1. Khong co interneta
\t2. Source list""")
        input_exit = input("[-] Nhan phim bat ki de thoat chuonng trinh..........")
        sys.exit()

    input_interface_allow = input("[-] Nhap interface cho phep cap dhcp (VD ens33 eth0 eth1): ")

    search_interface_allow_string = "INTERFACESv4=\"\""
    replace_interface_allow_string = "INTERFACESv4=\"{0}\"".format(input_interface_allow)
    subprocess.call("cp isc-dhcp-server isc-dhcp-server.temple", shell=True)
    replaceAll("isc-dhcp-server.temple", search_interface_allow_string, replace_interface_allow_string)
    move_file("isc-dhcp-server.temple", "/etc/default/isc-dhcp-server")

    subprocess.call("cp dhcpd.conf dhcpd.temple", shell=True)
    while True:
        os.system('clear')
        print("[+] Nhap IPv4 zone")
        while True:
            input_subnet = input("\t[-] Nhap subnet (VD: 192.168.1.0) (Bat buoc): ")
            if input_subnet:
                break
            else:
                os.system('clear')

        while True:
            input_netmask = input("\t[-] Nhap subnetmask (VD: 255.255.255.0) (Bat buoc): ")
            if input_netmask:
                break
            else:
                os.system('clear')

        while True:
            print("""\t[-] Nhap range VD:
\tFrom: 192.168.1.2
\tTo:   192.168.1.254 (Bat buoc)""")
            input_from_range = input("\t\t[.] From: ")
            input_to_range = input("\t\t[.] To  : ")
            if input_from_range and input_to_range:
                break
            else:
                os.system('clear')

        input_router = input("\t[-] Nhap gateway: ")
        input_domain_name = input("\t[-] Nhap domain: ")
        input_dns = input("\t[-] Nhap DNS Address: ")
        input_default_lease_time = input("\t[-] Nhap default lease time (default 600): ")
        input_max_lease_time = input("\t[-] Nhap max lease time (default 7200): ")

        dhcp_conf_file = open("dhcpd.temple", 'r+')
        dhcp_conf_file.read()
        dhcp_conf_file.write("subnet {0} netmask {1} {2}".format(input_subnet, input_netmask, "{\n"))
        dhcp_conf_file.write("\trange {0} {1};\n".format(input_from_range, input_to_range))
        if input_router:
            dhcp_conf_file.write("\toption routers {0};\n".format(input_router))
        else:
            pass
        if input_domain_name:
            dhcp_conf_file.write("\toption domain-name \"{0}\";\n".format(input_domain_name))
        else:
            pass
        if input_dns:
            dhcp_conf_file.write("\toption domain-name-servers {0};\n".format(input_dns))
        else:
            pass
        if input_default_lease_time:
            dhcp_conf_file.write("\tdefault-lease-time {0};\n".format(input_default_lease_time))
        else:
            pass
        if input_max_lease_time:
            dhcp_conf_file.write("\tmax-lease-time {0};\n".format(input_max_lease_time))
        else:
            pass

        dhcp_conf_file.write("{0}".format("}\n"))

        dhcp_conf_file.close()

        input_add_choice = input("[-] Ban co muon them dhcp zone khong (n)?")
        if input_add_choice in ('y', 'Y'):
            os.system('clear')
        else:
            break

    move_file("dhcpd.temple", "/etc/dhcp/dhcpd.conf")
    subprocess.call("systemctl restart isc-dhcp-server", shell=True)

    output_check_status = subprocess.getoutput("systemctl status isc-dhcp-server")
    output_check_status = str(output_check_status)
    check_result = re.search("Active: active", output_check_status)
    check2_result = re.search("Active: inactive", output_check_status)
    os.system('clear')
    if check_result:
        print("[-] DHCP server ACTIVE")
        subprocess.call("systemctl enable isc-dhcp-server", shell=True)
        print("[-] DHCP server da khoi dong cung he thong")
    elif check2_result:
        print("[-] DHCP Server INACTIVE")
    else:
        print("[-] DHCP Server Failed")
        print("[-] DHCP Server Failed")


def executable_menu():
    while True:
        count_exceed2 = 0
        while True:
            os.system("clear")
            print("""
        |=|===================================================|=|
        |=|    DEBIAN DEMO TOOLS ARE MADE BY CUONGCOLORS      |=|
        |=|     This software is built for python3.           |=|
        |=|                                                   |=|
        |=|     1. [-] Khoi Dong Lai DHCP Server              |=|
        |=|     2. [-] Dung DHCP Server                       |=|
        |=|     3. [-] Trang Thai DHCP Server                 |=|
        |=|     4. [-] Xem Ipv4 Zone                          |=|
        |=|     5. [-] Cau Hinh DHCP Server                   |=|
        |=|     6. [-] Interface Cho Phep DHCP Server         |=|
        |=|     7. [-] Khoi Phuc Cau Hinh Mac Dinh            |=|
        |=|     8. [-] Thoat                                  |=|
        |=|                                                   |=|
        |=|===================================================|=|
        """)
            try:
                input_tool_choise = input("[-] Nhap vao lua chon: ")
            except ValueError:
                print("[-] Lua chon khong chinh xac, xin nhap lai.[1]")
            choice_list = ['1', '2', '3', '4', '5', '6', '7', '8']

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
            subprocess.call("systemctl restart isc-dhcp-server", shell=True)
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '2':
            subprocess.call("systemctl stop isc-dhcp-server", shell=True)
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '3':
            dhcp_status()
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '4':
            show_dhcpd_conf()
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '5':
            dhcp_conf()
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '6':
            show_interface_allow()
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '7':
            print("[-] Tien trinh khoi phuc mac dinh....")
            time.sleep(2)
            subprocess.call("systemctl stop isc-dhcp-server", shell=True)
            subprocess.call("rm -rf /etc/dhcp", shell=True)
            subprocess.call("cp -r dhcp /etc/", shell=True)
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        else:
            break