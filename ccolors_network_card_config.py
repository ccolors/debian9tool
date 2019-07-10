import subprocess
import time
import os
import ccolors_net_tools
import sys

def move_file(file_name):
    subprocess.call(['mv', file_name, '/etc/network/interfaces.d/{0}'.format(file_name)])
    subprocess.call(['systemctl', 'restart', 'networking'])
    while True:
        input_reboot = input("""
        (Co the mot so truong hop, yeu cau bat buoc phai khoi dong)
        Ban co muon khoi dong lai hdh khong? (y/n)?""")
        reboot_list = {'y', 'Y', 'n', 'N'}
        if input_reboot in reboot_list:
            if input_reboot in ('y', 'Y'):
                subprocess.call('reboot', shell=True)
            else:
                break
        else:
            pass

def config_static():
    while True:
        interface = input("Interface: ")
        if interface != '':
            break
        else:
            print("interface khong dc de trong!")
            time.sleep(2)
            os.system('clear')
    while True:
        address = input("Address: ")
        if address != '':
            break
        else:
            print("Address khong dc de trong!")
            time.sleep(2)
            os.system('clear')
    while True:
        subnetmask = input("Subnetmask: ")
        if subprocess != '':
            break
        else:
            print("Subnetmask khong dc de trong!")
            time.sleep(2)
            os.system('clear')
    gateway = input("Gateway [gateway]: ")
    dns_nameservers = input("DNS [dns_namservers]: ")
    str_string = '''
auto {0}
iface {1} inet static
\taddress {2}
\tnetmask {3}
'''.format(interface, interface, address, subnetmask)
    if gateway:
        str_string = str_string + '\tgateway {0}\n'.format(gateway)
    else:
        pass
    if dns_nameservers:
        str_string = str_string + '\tdns-nameservers {0}\n'.format(dns_nameservers)
    else:
        pass

    str_string = str_string.lower()
    file_name = interface.lower()
    network_file = open(file_name, 'w')
    network_file.write(str_string)
    network_file.close()
    move_file(file_name)

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
        |=|     1. [-] Xem Thong Tin Tat Ca Interfaces        |=|
        |=|     2. [-] Xem Thong Tin Chi Mot Interfaces       |=|
        |=|     3. [-] Khoi Dong Lai Dich Vu Mang             |=|
        |=|     4. [-] Cau Hinh mang                          |=|
        |=|     5. [+] Hosts                                  |=|
        |=|     6. [-] Cho Phep Chuyen Tiep Luu Luong Mang    |=|
        |=|     7. [-] Tat Chuyen Tiep Luu Luong Mang         |=|
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
            ccolors_net_tools.view_interface()
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '2':
            ccolors_net_tools.view_only_interface()
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '3':
            ccolors_net_tools.net_work_card_restart()
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '4':
            config_static()
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '5':
            while True:
                count_exceed2 = 0
                while True:
                    os.system("clear")
                    print("""
        |=|===================================================|=|
        |=|    DEBIAN DEMO TOOLS ARE MADE BY CUONGCOLORS      |=|
        |=|     This software is built for python3.           |=|
        |=|                                                   |=|
        |=|     1. [-] Them Host                              |=|
        |=|     2. [-] Xem Tep Host                           |=|
        |=|     3. [-] Xoa Host                               |=|
        |=|     4. [-] Exit                                   |=|
        |=|                                                   |=|
        |=|===================================================|=|
        """)
                    try:
                        input2_tool_choise = input("[-] Nhap vao lua chon: ")
                    except ValueError:
                        print("[-] Lua chon khong chinh xac, xin nhap lai.[1]")
                    choice_list = ['1', '2', '3', '4']

                    if input2_tool_choise in choice_list:
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
                if input2_tool_choise == '1':
                    ccolors_net_tools.change_hostname()
                    input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
                elif input2_tool_choise == '2':
                    ccolors_net_tools.show_hosts()
                    input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
                elif input2_tool_choise == '3':
                    ccolors_net_tools.remove_host()
                    input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
                else:
                    break
        elif input_tool_choise == '6':
            ccolors_net_tools.allow_forwarding_traffic()
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '7':
            ccolors_net_tools.disable_forwarding_traffic()
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        else:
            break