#!/usr/bin/env python
import subprocess
import time
import sys
import os
import ccolors_net_tools
import ccolors_network_card_config
import fileinput
import ccolors_dns_server
import ccolors_dhcp_server
import ccolors_samba_server
import ccolors_domain_controler
import ccolors_web_deploy
import ccolors_backup_restore

while True:
    try:
        count_exceed = 0
        while True:
            os.system("clear")
            print("""
    |=|===================================================|=|
    |=|    DEBIAN DEMO TOOLS ARE MADE BY CUONGCOLORS      |=|
    |=|     This software is built for python3.           |=|
    |=|                                                   |=|
    |=|     1. [-] Cap Nhat He Thong                      |=|
    |=|     2. [-] Nang Cap He Thong                      |=|
    |=|     3. [+] Cong Cu                                |=|
    |=|     4. [+] Mang                                   |=|
    |=|     5. [+] DHCP                                   |=|
    |=|     6. [+] DNS                                    |=|
    |=|     7. [+] Samba                                  |=|
    |=|     8. [+] AD DC                                  |=|
    |=|     9. [+] Web Deploy                             |=|
    |=|     10.[+] Sao Luu Va Khoi Phuc                   |=|
    |=|     11.[-] Thoat                                  |=|
    |=|                                                   |=|
    |=|===================================================|=|
    """)
            try:
                input_choise = input("[-] Nhap vao lua chon: ")
            except ValueError:
                print("[-] Lua chon khong chinh xac, xin nhap lai.[1]")
            choice_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']

            if input_choise in choice_list:
                break
            else:
                print("[-] Lua chon khong chinh xac, xin nhap lai.[2]")
                count_exceed += 1

            if count_exceed > 3:
                print("""[-] Ban nhap qua so lan cho phep
                Chuong trinh se thoat sau 3 giay
                """)
                for i in range(3, 0, -1):
                    print("\t\t", i)
                    time.sleep(1)
                os.system('clear')
                sys.exit()
            else:
                pass
            time.sleep(1)

        if input_choise == '1':
            ccolors_net_tools.update()
        elif input_choise == '2':
            ccolors_net_tools.upgrade()
        elif input_choise == '3':
            ccolors_net_tools.excutable_menu()
        elif input_choise == '4':
            ccolors_network_card_config.executable_menu()
        elif input_choise == '5':
            ccolors_dhcp_server.executable_menu()
        elif input_choise == '6':
            ccolors_dns_server.executable_menu()
        elif input_choise == '7':
            ccolors_samba_server.executable_menu()
        elif input_choise == '8':
            ccolors_domain_controler.ad_menu()
        elif input_choise == '9':
           ccolors_web_deploy.web_deploy_menu()
        elif input_choise == '10':
            ccolors_backup_restore.executable_menu()
        else:
            os.system('clear')
            sys.exit()
    except KeyboardInterrupt:
        print("\n[+] Da phat hien CTRL + C\n\t[-] Chuong trinh thoat ngay lap tuc")
        time.sleep(1)
        os.system('clear')
        sys.exit()

    input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh [2]")

