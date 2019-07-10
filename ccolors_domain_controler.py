import subprocess
import re
import os
import sys
import time


def install_source():
    subprocess.call("apt-get install -y samba krb5-config winbind smbclient", shell=True)
    install_result = subprocess.getoutput("apt-get -y install samba krb5-config winbind smbclient")
    install1_result_search = re.search("Processing triggers for man-db", install_result)
    install2_result_search = re.search("already the newest version", install_result)
    install3_result_search = re.search("Could not resolve", install_result)
    if install3_result_search:
        return False
    elif install1_result_search or install2_result_search:
        return True
    else:
        return False

def move_file(source, destination):
    subprocess.call(["mv", source, destination])

def create_user():
    while True:
        os.system('clear')
        input_create_user = input("[-] Ban co muon tao user khong (n)? ")
        if input_create_user in ('y', 'Y'):
            input_user = input("\t[-] Nhap ten user: ")
            subprocess.call("samba-tool user create {0}".format(input_user), shell=True)
            time.sleep(2)
        else:
            break

def delete_user():
    while True:
        os.system('clear')
        input_delete_user = input("[-] Ban co muon xoa user khong (n)? ")
        if input_delete_user in ('y', 'Y'):
            input_user = input("\t[-] Nhap ten user: ")
            subprocess.call("samba-tool user delete {0}".format(input_user), shell=True)
            time.sleep(2)
        else:
            break

def ad_dc_status():
    output_check_status = subprocess.getoutput("systemctl status samba-ad-dc")
    output_check_status = str(output_check_status)
    check_result = re.search("Active: active", output_check_status)
    check2_result = re.search("Active: inactive", output_check_status)
    if check_result:
        print("[-] AD DC Server ACTIVE")
        input_delay = input("---------------STATUS---------------------")
        output_status = subprocess.getoutput("smbclient -L localhost -U%")
        print(output_status)
        input_delay = input("---------Confirm domain level-------------")
        output_level = subprocess.call("samba-tool domain level show", shell=True)
        print(output_level)
    elif check2_result:
        print("[-] AD DC Server INACTIVE")
    else:
        print("[-] AD DC Server Failed")

def string_search(file_name, str_input):
    file = open(file_name, 'r')
    str_temple = file.read()
    str_target = re.search(str_input, str_temple)
    file.close()
    return str_target.group(0)

def domain_conf():
    print("[-] Dang cai goi...")
    if install_source() == True:
        print("[-] Goi da duoc cai dat")
    else:
        print("""[-] Khong cai duoc goi
Nguyen nhan:
\t1. Khong co internet
\t2. Source list""")
        input_exit = input("[-] Nhan phim bat ki de thoat chuonng trinh..........")
        sys.exit()

    subprocess.call("mv /etc/samba/smb.conf /etc/samba/smb.conf.org", shell=True)
    subprocess.call("samba-tool domain provision", shell=True)
    subprocess.call("cp /var/lib/samba/private/krb5.conf /etc/ ", shell=True)
    subprocess.call("systemctl stop smbd nmbd winbind", shell=True)
    subprocess.call("systemctl disable smbd nmbd winbind", shell=True)
    subprocess.call("systemctl unmask samba-ad-dc ", shell=True)
    input_delay = input("----------------------------------")
    subprocess.call("systemctl restart samba-ad-dc", shell=True)
    output_result = subprocess.getoutput("systemctl status samba-ad-dc")
    if re.search("Active: active", output_result):
        subprocess.call("systemctl enable samba-ad-dc", shell=True)
    else:
        pass

    ad_dc_status()
    input_delay = input("------------------------------------------")

def ad_menu():
            while True:
                count_exceed2 = 0
                while True:
                    os.system("clear")
                    print("""
    |=|===================================================|=|
    |=|    DEBIAN DEMO TOOLS ARE MADE BY CUONGCOLORS      |=|
    |=|     This software is built for python3.           |=|
    |=|                                                   |=|
    |=|     1. [-] Khoi Dong Lai AD DC Server             |=|
    |=|     2. [-] Dung AD DC Server                      |=|
    |=|     3. [-] Trang Thai AD DC Server                |=|
    |=|     4. [-] Cai Dat Va Cau Hinh AD DC Server       |=|
    |=|     5. [-] Tao User                               |=|
    |=|     6. [-] Xoa User                               |=|
    |=|     7. [-] Danh Sach User                         |=|
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
                    subprocess.call("systemctl restart samba-ad-dc", shell=True)
                    input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
                elif input_tool_choise == '2':
                    subprocess.call("systemctl stop samba-ad-dc", shell=True)
                    input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
                elif input_tool_choise == '3':
                    ad_dc_status()
                    input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
                elif input_tool_choise == '4':
                    domain_conf()
                    input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
                elif input_tool_choise == '5':
                    create_user()
                    input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
                elif input_tool_choise == '6':
                    delete_user()
                    input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
                elif input_tool_choise == '7':
                    output_result = subprocess.getoutput("samba-tool user list")
                    print(output_result)
                    input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
                else:
                    break