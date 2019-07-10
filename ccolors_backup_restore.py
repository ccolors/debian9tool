import subprocess
import re
import os
import sys
import time

def backup_dns():
    input_choice = input("[+] Ban co muon sao luu cau hinh DNS Server khong (n)? ")
    if input_choice in ('y', 'Y'):
        print("\n----------- Cau Hinh Da Sao Luu - DNS--------------\n")
        print(subprocess.getoutput("ls backup/dns/"))
        print("\n----------------------------------------------------\n")
        input_nameconf = input("[-] Nhap ten cau hinh sao luu: ")
        if input_nameconf:
            subprocess.call("mkdir backup/dns/{0}".format(input_nameconf), shell=True)
            subprocess.call("cp -r /etc/bind/ backup/dns/{0}".format(input_nameconf), shell=True)
        else:
            pass
    else:
        pass

def backup_dhcp():
    input_choice = input("[+] Ban co muon sao luu caU hinh DHCP Server khong (n)? ")
    if input_choice in ('y', 'Y'):
        print("\n----------- Cau Hinh Da Sao Luu - DHCP--------------\n")
        print(subprocess.getoutput("ls backup/dhcp/"))
        print("\n----------------------------------------------------\n")
        input_nameconf = input("[-] Nhap ten cau hinh sao luu: ")
        if input_nameconf:
            subprocess.call("mkdir backup/dhcp/{0}".format(input_nameconf), shell=True)
            subprocess.call("cp -r /etc/dhcp/ backup/dhcp/{0}".format(input_nameconf), shell=True)
        else:
            pass
    else:
        pass

def backup_samba():
    input_choice = input("[+] Ban co muon sao luu cau hinh Samba Server khong (n)? ")
    if input_choice in ('y', 'Y'):
        print("\n----------- Cau Hinh Da Sao Luu - Samba --------------\n")
        print(subprocess.getoutput("ls backup/samba/"))
        print("\n----------------------------------------------------\n")
        input_nameconf = input("[-] Nhap ten cau hinh sao luu: ")
        if input_nameconf:
            subprocess.call("mkdir backup/samba/{0}".format(input_nameconf), shell=True)
            subprocess.call("cp -r /etc/samba/ backup/samba/{0}".format(input_nameconf), shell=True)
        else:
            pass
    else:
        pass

def restore_dns():
    input_choice = input("[+] Ban co muon khoi phuc cau hinh DNS Server khong (n)? ")
    if input_choice in ('y', 'Y'):
        print("\n----------- Cau Hinh Da Sao Luu - DNS--------------\n")
        print(subprocess.getoutput("ls backup/dns/"))
        print("\n----------------------------------------------------\n")
        input_nameconf = input("[-] Nhap ten cau hinh can khoi phuc: ")
        if input_nameconf:
            subprocess.call("rm -r /etc/bind/*", shell=True)
            subprocess.call("cp -r backup/dns/{0}/bind/* /etc/bind/".format(input_nameconf), shell=True)
        else:
            pass
    else:
        pass

def restore_dhcp():
    input_choice = input("[+] Ban co muon khoi phuc cau hinh DHCP Server khong (n)? ")
    if input_choice in ('y', 'Y'):
        print("\n----------- Cau Hinh Da Sao Luu - DHCP--------------\n")
        print(subprocess.getoutput("ls backup/dhcp/"))
        print("\n----------------------------------------------------\n")
        input_nameconf = input("[-] Nhap ten file can khoi phuc: ")
        if input_nameconf:
            subprocess.call("rm -r /etc/dhcp/*", shell=True)
            subprocess.call("cp -r  backup/dhcp/{0}/dhcp/ /etc/dhcp/".format(input_nameconf), shell=True)
        else:
            pass
    else:
        pass

def restore_samba():
    input_choice = input("[+] Ban co muon khoi phuc cau hinh Samba Server khong (n)? ")
    if input_choice in ('y', 'Y'):
        print("\n----------- Cau Hinh Da Sao Luu - Samba--------------\n")
        print(subprocess.getoutput("ls backup/samba/"))
        print("\n----------------------------------------------------\n")
        input_nameconf = input("[-] Nhap ten file can khoi phuc: ")
        if input_nameconf:
            subprocess.call("rm -r /etc/samba/*", shell=True)
            subprocess.call("cp -r backup/samba/{0}/samba/ /etc/samba/".format(input_nameconf), shell=True)
        else:
            pass
    else:
        pass

def delete_dns():
    input_choice = input("[+] Ban co muon xoa cau hinh DNS Server khong (n)? ")
    if input_choice in ('y', 'Y'):
        print("\n----------- Cau Hinh Da Sao Luu - DNS--------------\n")
        print(subprocess.getoutput("ls backup/dns/"))
        print("\n----------------------------------------------------\n")
        input_nameconf = input("[-] Nhap ten cau hinh can xoa: ")
        if input_nameconf:
            subprocess.call("rm -rf backup/dns/{0}".format(input_nameconf), shell=True)
        else:
            pass
    else:
        pass

def delete_dhcp():
    input_choice = input("[+] Ban co muon xoa cau hinh DHCP Server khong (n)? ")
    if input_choice in ('y', 'Y'):
        print("\n----------- Cau Hinh Da Sao Luu - DHCP--------------\n")
        print(subprocess.getoutput("ls backup/dhcp/"))
        print("\n----------------------------------------------------\n")
        input_nameconf = input("[-] Nhap ten cau hinh can xoa: ")
        if input_nameconf:
            subprocess.call("rm -rf backup/dhcp/{0}".format(input_nameconf), shell=True)
        else:
            pass
    else:
        pass

def delete_samba():
    input_choice = input("[+] Ban co muon xoa cau hinh Samba Server khong (n)? ")
    if input_choice in ('y', 'Y'):
        print("\n----------- Cau Hinh Da Sao Luu - Samba--------------\n")
        print(subprocess.getoutput("ls backup/samba/"))
        print("\n----------------------------------------------------\n")
        input_nameconf = input("[-] Nhap ten cau hinh can xoa: ")
        if input_nameconf:
            subprocess.call("rm -rf backup/samba/{0}".format(input_nameconf), shell=True)
        else:
            pass
    else:
        pass


def saoLuu_Menu():
    while True:
        count_exceed2 = 0
        while True:
            os.system("clear")
            print("""
|=|====================================================|=|
|=|    DEBIAN DEMO TOOLS ARE MADE BY CUONGCOLORS       |=|
|=|     This software is built for python3.            |=|
|=|                                                    |=|
|=|     1.  [-] Sao Luu Cau Hinh DNS Server            |=|
|=|     2.  [-] Sao Luu Cau Hinh DHCP Server           |=|
|=|     3.  [-] Sao Luu Cau Hinh Samba Server          |=|
|=|     4.  [-] Thoat                                  |=|
|=|                                                    |=|
|=|====================================================|=|
        """)
            try:
                input_tool_choise = input("[-] Nhap vao lua chon: ")
            except ValueError:
                print("[-] Lua chon khong chinh xac, xin nhap lai.[1]")
            choice_list = ['1', '2', '3', '4']

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
            backup_dns()
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '2':
            backup_dhcp()
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '3':
            backup_samba()
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        else:
            break

def khoiPhuc_Menu():
    while True:
        count_exceed2 = 0
        while True:
            os.system("clear")
            print("""
|=|====================================================|=|
|=|    DEBIAN DEMO TOOLS ARE MADE BY CUONGCOLORS       |=|
|=|     This software is built for python3.            |=|
|=|                                                    |=|
|=|     1.  [-] Khoi Phuc Cau Hinh DNS Server          |=|
|=|     2.  [-] Khoi Phuc Cau Hinh DHCP Server         |=|
|=|     3.  [-] Khoi Phuc Cau Hinh Samba Server        |=|
|=|     4.  [-] Thoat                                  |=|
|=|                                                    |=|
|=|====================================================|=|
        """)
            try:
                input_tool_choise = input("[-] Nhap vao lua chon: ")
            except ValueError:
                print("[-] Lua chon khong chinh xac, xin nhap lai.[1]")
            choice_list = ['1', '2', '3', '4']

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
            restore_dns()
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '2':
            restore_dhcp()
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '3':
            restore_samba()
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        else:
            break

def xoa_Menu():
    while True:
        count_exceed2 = 0
        while True:
            os.system("clear")
            print("""
|=|====================================================|=|
|=|    DEBIAN DEMO TOOLS ARE MADE BY CUONGCOLORS       |=|
|=|     This software is built for python3.            |=|
|=|                                                    |=|
|=|     1.  [-] Xoa Cau Hinh Sao Luu DNS Server        |=|
|=|     2.  [-] Xoa Cau Hinh Sao Luu DHCP Server       |=|
|=|     3.  [-] Xoa Cau Hinh Sao Luu Samba Server      |=|
|=|     4.  [-] Thoat                                  |=|
|=|====================================================|=|
        """)
            try:
                input_tool_choise = input("[-] Nhap vao lua chon: ")
            except ValueError:
                print("[-] Lua chon khong chinh xac, xin nhap lai.[1]")
            choice_list = ['1', '2', '3', '4']

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
            delete_dns()
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '2':
            delete_dhcp()
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '3':
            delete_samba()
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        else:
            break

def executable_menu():
    while True:
        count_exceed2 = 0
        while True:
            os.system("clear")
            print("""
|=|====================================================|=|
|=|    DEBIAN DEMO TOOLS ARE MADE BY CUONGCOLORS       |=|
|=|     This software is built for python3.            |=|
|=|                                                    |=|
|=|     1.  [+] Sao Luu Cau Hinh                       |=|
|=|     2.  [+] Khoi Phuc Cau Hinh                     |=|
|=|     3.  [+] Xoa Cau Hinh Sao Luu                   |=|
|=|     4.  [-] Thoat                                  |=|
|=|                                                    |=|
|=|====================================================|=|
        """)
            try:
                input_tool_choise = input("[-] Nhap vao lua chon: ")
            except ValueError:
                print("[-] Lua chon khong chinh xac, xin nhap lai.[1]")
            choice_list = ['1', '2', '3', '4']

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
            saoLuu_Menu()
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '2':
            khoiPhuc_Menu()
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '3':
            xoa_Menu()
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        else:
            break