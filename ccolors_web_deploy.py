import subprocess
import ccolors_net_tools
import re
import sys
import time
import os

def install_source():
    subprocess.call("apt-get install -y git net-tools sudo wget curl bash-completion apache2 libapache2-mod-php7.0 php7.0 php7.0-gd php7.0-xml php7.0-curl php7.0-mbstring php7.0-mcrypt php7.0-mysql mariadb-server mariadb-client php-curl php-gd php-mbstring php-xml php-xmlrpc php-soap php-intl php-zip", shell=True)
    install_result1 = subprocess.getoutput("apt-get install -y net-tools sudo wget curl bash-completion apache2 libapache2-mod-php7.0 php7.0 php7.0-gd php7.0-xml php7.0-curl php7.0-mbstring php7.0-mcrypt php7.0-mysql mariadb-server mariadb-client php-curl php-gd php-mbstring php-xml php-xmlrpc php-soap php-intl php-zip")
    install1_result_search = re.search("Processing triggers for man-db", install_result1)
    install2_result_search = re.search("already the newest version", install_result1)
    if install1_result_search or install2_result_search:
        return True
    else:
        return False

def restart_apache2_service():
    subprocess.call("systemctl restart apache2", shell=True)

def disable_apache2_service():
    subprocess.call("systemctl disable apache2", shell=True)

def enable_apache_service():
    subprocess.call("systemctl enable apache2", shell=True)

def service_apache2_status():
    # khoi dong lai dich vu apache2
    output_check_status = subprocess.getoutput("systemctl status apache2")
    output_check_status = str(output_check_status)
    check_result = re.search("Active: active", output_check_status)
    check2_result = re.search("Active: inactive", output_check_status)
    os.system('clear')
    if check_result:
        print("[-] apache2 ACTIVE")
        subprocess.call("systemctl enable apache2", shell=True)
        print("[-] apache2 da khoi dong cung he thong")
    elif check2_result:
        print("[-]apache2 INACTIVE")
    else:
        print("[-] apache2 Failed")

def web_deploy():
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

    subprocess.call("mkdir /temple", shell=True)
    url_git_input = input("\n------------------------------------------\n[-] Nhap reposity git url vd(user@domain.com:repo.git: ")

    # tai source web tu git server
    subprocess.call("git clone {0} /temple/".format(url_git_input), shell=True)

    # xoa file index va sao chep source file vao thu muc /var/www/html
    subprocess.call("rm -rf /var/www/html/*", shell=True)
    subprocess.call("cp -r /temple/* /var/www/html/", shell=True)

    # dat quyen cho thu muc html
    subprocess.call("chmod 777 -R /var/www/html/", shell=True)

    # xoa thu muc temple
    subprocess.call("rm -rf /temple/", shell=True)

    # khoi dong lai dich vu apache2
    output_check_status = subprocess.getoutput("systemctl status apache2")
    output_check_status = str(output_check_status)
    check_result = re.search("Active: active", output_check_status)
    check2_result = re.search("Active: inactive", output_check_status)
    os.system('clear')
    if check_result:
        print("[-] apache2 ACTIVE")
        subprocess.call("systemctl enable apache2", shell=True)
        print("[-] apache2 da khoi dong cung he thong")
    elif check2_result:
        print("[-]apache2 INACTIVE")
    else:
        print("[-] apache2 Failed")

def default_restore():
    print("[-] Tien trinh khoi phuc mac dinh........")
    time.sleep(2)
    subprocess.call("rm -rf /var/www/", shell=True)
    subprocess.call("cp -r www/ /var/", shell=True)

def web_deploy_menu():
    while True:
        count_exceed2 = 0
        while True:
            os.system("clear")
            print("""
               |=|=================================================================|=|
               |=|    DEBIAN DEMO TOOLS ARE MADE BY CUONGCOLORS                    |=|
               |=|     This software is built for python3.                         |=|
               |=|                                                                 |=|
               |=|     1. [-] Khoi Dong Lai Dich Vu Web                            |=|
               |=|     2. [-] Dung Dich Vu Web                                     |=|
               |=|     3. [-] Cho Phep Dịch Vu Web Khoi Dong Cung He Thong         |=|
               |=|     4. [-] Khong Cho Phep Dịch Vu Web Khoi Dong Cung He Thong   |=|
               |=|     5. [-] Trang Thai Dich Vu Web                               |=|
               |=|     6. [-] Trien Khai Web                                       |=|
               |=|     7. [-] Khoi Phuc Mac Dinh                                   |=|
               |=|     8. [-] Thoat                                                |=|
               |=|                                                                 |=|
               |=|=================================================================|=|
               """)
            try:
                input_tool_choise = input("[-] Nhap vao lua chon: ")
            except ValueError:
                print("[-] Lua chon khong chinh xac, xin nhap lai.[1]")
            choice_list = ['1', '2', '3', '4', "5", '6', '7', '8']

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
            restart_apache2_service()
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '2':
            subprocess.call("systemctl stop apache2", shell=True)
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '3':
            enable_apache_service()
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '4':
            disable_apache2_service()
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '5':
            service_apache2_status()
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '6':
            web_deploy()
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '7':
            default_restore()
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        else:
            break