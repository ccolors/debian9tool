import subprocess
import re
import os
import sys
import time

def install_source():
    subprocess.call("apt-get install -y libcups2 samba samba-common cups", shell=True)
    install_result = subprocess.getoutput("apt-get -y install libcups2 samba samba-common cups")
    install1_result_search = re.search("Processing triggers for man-db", install_result)
    install2_result_search = re.search("already the newest version", install_result)
    if install1_result_search or install2_result_search:
        return True
    else:
        return False

def add_group():
    while True:
        input_choice = input("[+] Ban co muon tao group  khong (n)? ")
        if input_choice in ('y', 'Y'):
            input_group_name = input("[-] Nhap ten user group: ")
            subprocess.call("groupadd {0}".format(input_group_name), shell=True)
            os.system('clear')
        else:
            break

def add_user():
    while True:
        input_choice = input("[+] Ban co muon tao users khong (n)? ")
        if input_choice in ('y', 'Y'):
            input_user_name = input("[-] Nhap ten user [bat buoc]: ")
            input_group_name = input("[-] Nhap ten group ma ban muon {0} thuoc: ".format(input_user_name))
            if input_group_name:
                subprocess.call("useradd {0} -m -G {1}".format(input_user_name, input_group_name), shell=True)
                time.sleep(2)
            else:
                subprocess.call("useradd {0}".format(input_user_name), shell=True)

            print("\t[-] Nhap mat khau cho {0} samba".format(input_user_name))
            subprocess.call("smbpasswd -a {0}".format(input_user_name), shell=True)
            time.sleep(2)
            os.system('clear')
        else:
            break

def move_file(source, destination):
    subprocess.call(["mv", source, destination])

def samba_status():
    output_check_status = subprocess.getoutput("systemctl status smbd")
    output_check_status = str(output_check_status)
    check_result = re.search("Active: active", output_check_status)
    check2_result = re.search("Active: inactive", output_check_status)
    if check_result:
        print("[-] Samba Server ACTIVE")
    elif check2_result:
        print("[-] Samba Server INACTIVE")
    else:
        print("[-] Samba Server Failed")

def samba_conf():
    print("[-] Dang cai goi...")
    if install_source() == True:
        os.system("clear")
        print("[-] Goi da duoc cai dat")
    else:
        print("""[-] Khong cai duoc goi
Nguyen nhan:
\t1. Khong co internet
\t2. Source list""")
        input_exit = input("[-] Nhan phim bat ki de thoat chuonng trinh..........")
        sys.exit()

    subprocess.call("cp smb.conf smb.temple", shell=True)
    smb_conf_file = open("smb.temple", 'r+')
    smb_conf_file.write("[global]\n")
    input_workgroup = input("[-] Work Group (default WORKGROUP): ")

    if input_workgroup:
        smb_conf_file.write("workgroup = {0}\n".format(input_workgroup))
    else:
        smb_conf_file.write("workgroup = WORKGROUP\n")

    input_server_string = input("[-] Server string (default Samba Server %v): ")
    if input_server_string:
        smb_conf_file.write("server string = {0}\n".format(input_server_string))
    else:
        smb_conf_file.write("server string = Samba Server %v\n")

    input_netbios_name = input("[-] Netbios name (default Debian): ")
    if input_netbios_name:
        smb_conf_file.write("netbios name = {0}\n".format(input_netbios_name))
    else:
        smb_conf_file.write("netbios name = debian\n")

    input_security = input("[-] Security (default user): ")
    if input_security:
        smb_conf_file.write("security = {0}\n".format(input_security))
    else:
        smb_conf_file.write("security = user\n")

    input_map_guest = input("[-] Map to get (default bad user): ")
    if input_map_guest:
        smb_conf_file.write("map to guest = {0}\n".format(input_map_guest))
    else:
        smb_conf_file.write("map to guest =  bad user\n")

    input_dns_proxy = input("[-] Dns proxy (default no): ")
    if input_dns_proxy:
        smb_conf_file.write("dns proxy = {0}\n".format(input_dns_proxy))
    else:
        smb_conf_file.write("dns proxy = no\n")

    input_home_directory = input("[-] Bam co muon hien thi thu muc Home cua user (n): ")

    if input_home_directory in ('y', 'Y'):
        smb_conf_file.write("""
[homes]
comment = Home directory
browseable = no
valid user = %S
writable = yes
create mask = 0700
ditectory mask = 0700
\n""")
    else:
        pass

    while True:
        os.system('clear')
        input_add_choice = input("[+] Ban co muon chia se them thu muc (n) ?: ")
        if input_add_choice in ('y', 'Y'):
            pass
        else:
            os.system('clear')
            break

        while True:
            input_directory_name = input("\t[-] Nhap ten thu muc [bat buoc]: ")
            if input_directory_name:
                smb_conf_file.write("[{0}]\n".format(input_directory_name))
                break
            else:
                os.system('clear')
                pass

        while True:
            input_path = input("\t[-] Nhap duong dan [bat buoc]\n\t\tpath = ")
            if input_path:
                smb_conf_file.write("path = {0}\n".format(input_path))
                break
            else:
                pass

        input_valid_user = input("\t[-] Gioi han chi cho phep group hoac user truy cap (vd: @users, smbuser1\n\t\tvalid user = ")
        if input_valid_user:
            smb_conf_file.write("valid users = {0}\n".format(input_valid_user))
        else:
            pass

        input_guest_ok = input("\t[-] Cho phep truy cap khong xac thuc (yes or no)\n\t\tguest ok = ")
        if input_guest_ok != 'yes':
            input_read_list = input("\t[-] Danh sach user duoc phep doc (vd: @groupusers, smbuser1)\n\t\tread list =  ")
            if input_read_list:
                smb_conf_file.write("read list = {0}\n".format((input_read_list)))
            else:
                pass

            input_write_list = input("\t[-] Danh sach user duoc phep thay doi noi dung (vd: @groupusers, smbuser1)\n\t\twrite list = ")
            if input_write_list:
                smb_conf_file.write("write list = {0}\n".format(input_write_list))
            else:
                pass

            if input_read_list and  input_write_list:
                pass
            else:
                input_writable = input("\t[-] Cho phep chinh sua noi dung khong (yes or no)\n\twritable = ")
                if input_writable:
                    smb_conf_file.write("writable = {0}\n".format(input_writable))
                else:
                    pass

                if input_writable == 'yes' or input_write_list:
                    input_create_mask = input("\t[-] Phan quyen cho tap tin tao moi (0777 or 0666 ...)[bat buoc]\n\t\tcreate mask = ")
                    if input_create_mask:
                        smb_conf_file.write("create mask = {0}\n".format(input_create_mask))
                    else:
                        pass

                    input_directory_mask = input("\t[-] Phan quyen cho thu muc tao moi (0777 or 0666)[bat buoc]\n\t\tdirectory mask = ")
                    if input_directory_mask:
                        smb_conf_file.write("directory mask = {0}\n".format(input_directory_mask))
                    else:
                        pass

                    input_force_group = input("\t[-] Du lieu tao ra thuoc group (vd: users, groupsmd)\n\t\tforce group = ")
                    if input_force_group:
                        smb_conf_file.write("force group = {0}\n".format(input_force_group))
                    else:
                        pass

            input_browseable = input("\t[-] Cho phep hoac khong cho phep hien thi tren trinh duyet (yes or no)\n\t\tbrowseable = ")
            if input_browseable:
                smb_conf_file.write("browseable = {0}\n".format(input_browseable))
            else:
                pass
        else:
            smb_conf_file.write("browseable = yes\n")
            input_writable = input("\t[-] Cho phep chinh sua noi dung khong (yes or no)\n\t\twritable = ")
            if input_writable:
                smb_conf_file.write("writable = {0}\n".format(input_writable))
            else:
                pass

            if input_writable == 'yes':
                input_create_mask = input("\t[-] Phan quyen cho tap tin tao moi (0777 or 0666 ...)[bat buoc]\n\t\tcreate mask = ")
                if input_create_mask:
                    smb_conf_file.write("create mask = {0}\n".format(input_create_mask))
                else:
                    pass

                input_directory_mask = input("\t[-] Phan quyen cho thu muc tao moi (0777 or 0666)[bat buoc]\n\t\tdirectory mask = ")
                if input_directory_mask:
                    smb_conf_file.write("directory mask = {0}\n".format(input_directory_mask))
                else:
                    pass

                input_force_group = input("\t[-] Du lieu tao ra thuoc group (vd: users, groupsmb)\n\t\tforce group = ")
                if input_force_group:
                    smb_conf_file.write("force group = {0}\n".format(input_force_group))
                else:
                    pass
        smb_conf_file.write("\n")

    smb_conf_file.close()
    move_file("smb.temple", "/etc/samba/smb.conf")

    subprocess.call("systemctl restart smbd", shell=True)
    output_check_status = subprocess.getoutput("systemctl status smbd")
    output_check_status = str(output_check_status)
    check_result = re.search("Active: active", output_check_status)
    check2_result = re.search("Active: inactive", output_check_status)
    if check_result:
        print("[-] SAMBA Server ACTIVE")
    elif check2_result:
        print("[-] SAMBA Server INACTIVE")
    else:
        print("[-] SAMBA Server Failed")

def executable_menu():
    while True:
        count_exceed2 = 0
        while True:
            os.system("clear")
            print("""
    |=|===================================================|=|
    |=|    DEBIAN DEMO TOOLS ARE MADE BY CUONGCOLORS      |=|
    |=|     This software is built for python3.           |=|
    |=|                     SAMBA                         |=|
    |=|     1. [-] Khoi Dong Lai Samba Server             |=|
    |=|     2. [-] Dung Samba Server                      |=|
    |=|     3. [-] Trang Thai Samba Server                |=|
    |=|     4. [-] Cai Dat Va Cau Hinh Samba Server       |=|
    |=|     5. [-] Xem Cau Hinh Samba Server              |=|
    |=|     6. [-] Tao Group                              |=|
    |=|     7. [-] Tao User                               |-|
    |=|     8. [-] Xem Tat Ca Group                       |=|
    |=|     9. [-] Xem Tat Ca User                        |=|
    |=|     10.[-] Xoa Group                              |=|
    |=|     11.[-] Xoa User                               |=|
    |=|     12.[-] Khoi Phuc Mac Dinh                     |=|
    |=|     13.[-] Thoat                                  |=|
    |=|                                                   |=|
    |=|===================================================|=|
    """)
            try:
                input_tool_choise = input("[-] Nhap vao lua chon: ")
            except ValueError:
                print("[-] Lua chon khong chinh xac, xin nhap lai.[1]")
            choice_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']

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
            subprocess.call("systemctl restart smbd", shell=True)
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '2':
            subprocess.call("systemctl stop smbd", shell=True)
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '3':
            samba_status()
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '4':
            samba_conf()
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '5':
            samba_conf_result = subprocess.getoutput("cat /etc/samba/smb.conf")
            print(samba_conf_result)
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '6':
            add_group()
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '7':
            add_user()
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '8':
            os.system("clear")
            print("Tat ca Group: \n--------------------\n")
            print(subprocess.getoutput("awk -F':' '{ print $1}' /etc/passwd"))
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '9':
            os.system("clear")
            print("Tat ca User: \n---------------------\n")
            print(subprocess.getoutput("pdbedit -L"))
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '10':
            os.system("clear")
            while True:
                input_deleteGroup = input("[-] Ban co muon xoa group (n)? ")
                if input_deleteGroup in ('y', 'Y'):
                    input_nameGroup = input("[-] Nhap ten Group: ")
                    subprocess.call("groupdel {0}".format(input_nameGroup), shell=True)
                else:
                    break
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '11':
            os.system("clear")
            while True:
                input_deleteUser = input("[-] Ban co muon xoa user (n)? ")
                if input_deleteUser in ('y', 'Y'):
                    input_nameUser = input("[-] Nhap ten User: ")
                    subprocess.call("userdel -r {0}".format(input_nameUser),shell=True)
                    subprocess.call("pdbedit -x -u {0}".format(input_nameUser), shell=True)
                else:
                    break
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '12':
            os.system("clear")
            print("[-] Tien trinh khoi phuc mac dinh.....")
            time.sleep(2)
            subprocess.call("systemctl stop smbd", shell=True)
            subprocess.call("rm -rf /etc/samba/", shell=True)
            subprocess.call("cp -r samba/ /etc/samba/", shell=True)
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        else:
            break