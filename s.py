import subprocess
import re
import fileinput
import os
import sys
import time

def install_source():
    subprocess.call("apt-get install -y bind9 bind9utils bind9-doc dnsutils", shell=True)
    install_result = subprocess.check_output("apt-get -y install isc-dhcp-server", shell=True)
    install_result = str(install_result)
    install_result_search1 = re.search("Processing triggers for man-db", install_result)
    install_result_search2 = re.search("already the newest version", install_result)
    if install_result_search1 or install_result_search2:
        return True
    else:
        return False

def replaceAll(file_name, searchExp, replaceExp):
    for line in fileinput.input(file_name, inplace=1):
        if searchExp in line:
            line = line.replace(searchExp, replaceExp)
        sys.stdout.write(line)

def move_file(source, destination):
    subprocess.call(["mv", source, destination])

def string_search(file_name, str_input):
    file = open(file_name, 'r')
    str_temple = file.read()
    str_target = re.search(str_input, str_temple)
    file.close()
    return str_target.group(0)

def dns_changer():
    input_DNS = input("""[-] Nhap dia chi phan giai DNS (DNS Resolv):   """)
    if input_DNS:
        if subprocess.getoutput("cat /etc/resolv.conf"):
            search_nameserver = "nameserver.*"
            replace_nameserver = "nameserver {0}".format(input_DNS)
            search_namserver_result = string_search("/etc/resolv.conf", search_nameserver)
            if search_namserver_result:
                replaceAll("/etc/resolv.conf", search_namserver_result, replace_nameserver)
            else:
                file_resolv = open("/etc/resolv.conf", "r+")
                file_resolv.read()
                file_resolv.write("nameserver {0}".format(input_DNS))
                file_resolv.close()
        else:
            f = open("/etc/resolv.conf", "w")
            f.write("nameserver {0}".format(input_DNS))
            f.close()

def dns_status():
    output_check_status = subprocess.getoutput("systemctl status bind9")
    output_check_status = str(output_check_status)
    check_result = re.search("Active: active", output_check_status)
    check2_result = re.search("Active: inactive", output_check_status)
    if check_result:
        print("[-] DNS server ACTIVE")
    elif check2_result:
        print("[-] DNS Server INACTIVE")
    else:
        print("[-] DNS Server Failed")

def create_forward_zone():
    while True:
        input_choice = input("[-] Ban co muon them domain khong? (n): ")
        if input_choice in ('y', 'Y'):
            os.system('clear')
        else:
            break

        input_forward_zone = input("[-] Nhap domain (bat buoc) VD: cuong.com :")
        forward_zone_string = """zone \"{0}\" IN {1} 
        type master;
        file \"/etc/bind/{2}.frd\";
        allow-update {3} none; {4};
{5};\n""".format(input_forward_zone, "{", input_forward_zone, "{", "}", "}")
        named_config_local_file = open("/etc/bind/named.conf.local", "r+")
        named_config_local_file.read()
        named_config_local_file.write(forward_zone_string)
        named_config_local_file.close()

        subprocess.call("cp forward.linux {0}.frd".format(input_forward_zone), shell=True)

        while True:
            input_hostname = input("[-] Nhap server hostname (bat buoc)\n   VD: (sv.cuong.local):   ")
            if input_hostname:
                break
            else:
                os.system("clear")

        replaceAll("{0}.frd".format(input_forward_zone), "localhost_sv", input_hostname)

        i = 0
        for element in input_hostname:
            if element == ".":
                domain_string = input_hostname[i + 1:]
                break
            else:
                i += 1

        replaceAll("{0}.frd".format(input_forward_zone), "root.localhost", "root." + domain_string)

        replace_ttl = input("[-] TTL (default 86400):   ")
        if replace_ttl:
            replaceAll("{0}.frd".format(input_forward_zone), "replace_ttl", replace_ttl)
        else:
            replaceAll("{0}.frd".format(input_forward_zone), "replace_ttl", "86400")

        replace_serial = input("[-] Serial (default 1): ")
        if replace_serial:
            replaceAll("{0}.frd".format(input_forward_zone), "replace_serial", replace_serial)
        else:
            replaceAll("{0}.frd".format(input_forward_zone), "replace_serial", "1")

        replace_refresh = input("[-] Refresh (default 604800):  ")
        if replace_refresh:
            replaceAll("{0}.frd".format(input_forward_zone), "replace_refresh", replace_refresh)
        else:
            replaceAll("{0}.frd".format(input_forward_zone), "replace_refresh", "604800")

        replace_retry = input("[-] Retry (default 86400):   ")
        if replace_retry:
            replaceAll("{0}.frd".format(input_forward_zone), "replace_retry", replace_retry)
        else:
            replaceAll("{0}.frd".format(input_forward_zone), "replace_retry", "86400")

        replace_expire = input("[-] Expire (default 2419200):   ")
        if replace_expire:
            replaceAll("{0}.frd".format(input_forward_zone), "replace_expire", replace_expire)
        else:
            replaceAll("{0}.frd".format(input_forward_zone), "replace_expire", "2419200")

        replace_negative = input("[-] Negative Cache TTL (default 86400):   ")
        if replace_negative:
            replaceAll("{0}.frd".format(input_forward_zone), "replace_negative", replace_negative)
        else:
            replaceAll("{0}.frd".format(input_forward_zone), "replace_negative", "86400")

        i = 0
        hostname_string = ''
        for element in input_hostname:
            if element == ".":
                hostname_string = input_hostname[0:i]
                break
            else:
                i += 1

        move_file("{0}.frd".format(input_forward_zone), "/etc/bind/{0}.frd".format(input_forward_zone))

def create_reverse_zone():
    while True:
        input_choice = input("[-] Ban co muon them reverse ip khong? (n): ")
        if input_choice in ('y', 'Y'):
            os.system('clear')
        else:
            break
        input_reverse_zone = input("[-] Nhap reverse ip (bat buoc) VD: 1.168.192 : ")
        reverse_zone_string = """zone \"{0}.in-addr.arpa\" IN {1}
        type master;
        file \"/etc/bind/{2}\";
        allow-update {3} none; {4};
{5};\n""".format(input_reverse_zone, "{", input_reverse_zone, "{", "}", "}")

        named_config_local_file = open("/etc/bind/named.conf.local", "r+")
        named_config_local_file.read()
        named_config_local_file.write(reverse_zone_string)
        named_config_local_file.close()

        while True:
            input_hostname = input("[-] Nhap host server (bat buoc)\n   VD: (sv.cuong.local):   ")
            if input_hostname:
                break
            else:
                os.system("clear")

        replaceAll("reverse.temple", "localhost_sv", input_hostname)

        i = 0
        for element in input_hostname:
            if element == ".":
                domain_string = input_hostname[i + 1:]
                break
            else:
                i += 1

        replaceAll("reverse.temple", "root.localhost", "root." + domain_string)

        replace_ttl = input("[-] TTL (default 86400):   ")
        if replace_ttl:
            replaceAll("reverse.temple", "replace_ttl", replace_ttl)
        else:
            replaceAll("reverse.temple", "replace_ttl", "86400")

        replace_serial = input("[-] Serial (default 1): ")
        if replace_serial:
            replaceAll("reverse.temple", "replace_serial", replace_serial)
        else:
            replaceAll("reverse.temple", "replace_serial", "1")

        replace_refresh = input("[-] Refresh (default 604800):  ")
        if replace_refresh:
            replaceAll("reverse.temple", "replace_refresh", replace_refresh)
        else:
            replaceAll("reverse.temple", "replace_refresh", "604800")

        replace_retry = input("[-] Retry (default 86400):   ")
        if replace_retry:
            replaceAll("reverse.temple", "replace_retry", replace_retry)
        else:
            replaceAll("reverse.temple", "replace_retry", "86400")

        replace_expire = input("[-] Expire (default 2419200):   ")
        if replace_expire:
            replaceAll("reverse.temple", "replace_expire", replace_expire)
        else:
            replaceAll("reverse.temple", "replace_expire", "2419200")

        replace_negative = input("[-] Negative Cache TTL (default 86400):   ")
        if replace_negative:
            replaceAll("reverse.temple", "replace_negative", replace_negative)
        else:
            replaceAll("reverse.temple", "replace_negative", "86400")

        i = 0
        hostname_string = ''
        for element in input_hostname:
            if element == ".":
                hostname_string = input_hostname[0:i]
                break
            else:
                i += 1

        move_file("reverse.temple", "/etc/bind/reverse.linux")

    move_file("options.temple", "/etc/bind/named.conf.options")
    move_file("local.temple", "/etc/bind/named.conf.local")

def add_A_AND_PTR():
    while True:
        count_exceed2 = 0
        while True:
            os.system("clear")
            print("""
    |=|====================================================|=|
    |=|                                                    |=| 
    |=|     1. ADD A                                       |=|
    |=|     2. ADD PTR                                     |=|
    |=|     2. ADD MX (mail) Record                        |=|
    |=|     3. ADD CNAME Record                            |=|
    |=|     4. Exit                                        |=|
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
            input_domain = input("[-] Nhap domain can them: ")
            forward_file = open("/etc/bind/{0}".format(input_domain), "r+")
            forward_file.read()
            while True:
                os.system("clear")
                input_continue = input("[+] Ban co muon nhap A Record (N)?: ")
                hostname2_string = ''
                if  input_continue in ('y', 'Y'):
                    input_hostname2 = input("\t[-] Nhap hostname (VD: sv.cuong.local):  ")
                    i = 0
                    for element2 in input_hostname2:
                        if element2 == ".":
                            hostname2_string = input_hostname2[0:i]
                            break
                        else:
                            i += 1

                    input_ip = input("\t[-] Nhap ip cua hostname: ")
                    forward_file.write("{0}	IN\tA\t{1}\n".format(hostname2_string, input_ip))

                else:
                    os.system('clear')
                    break
            forward_file.close()
        elif input_tool_choise == '2':
            input_reverseip = input("[-] nhap reverse ip zone can them: ")
            reverse_file = open("/etc/bind/{0}".format(input_reverseip), "r+")
            reverse_file.read()
            while True:
                os.system("clear")
                input_continue = input("[+] Ban co muon nhap PTR Record (n)?: ")
                hostname2_string = ''
                if input_continue in ('y', 'Y'):
                    input_hostname2 = input("\t[-] Nhap hostname (VD: sv.cuong.local):  ")
                    i = 0
                    for element2 in input_hostname2:
                        if element2 == ".":
                            hostname2_string = input_hostname2[0:i]
                            break
                        else:
                            i += 1

                    input_ip = input("\t[-] Nhap ip cua hostname: ")

                    PTR_ip = ''
                    for i in range(len(input_ip) - 1, 0, -1):
                        if input_ip[i] == '.':
                            PTR_ip = input_ip[i + 1:]
                            os.system("clear")
                            break
                        else:
                            pass

                    reverse_file.write("{0}	IN\tPTR\t{1}.\n".format(PTR_ip, input_hostname2))

                else:
                    os.system('clear')
                    break
            forward_file.close()
            reverse_file.close()
        elif input_tool_choise == '3':
            forward_file = open("/etc/bind/forward.linux", "r+")
            forward_file.read()
            while True:
                os.system("clear")
                input_continue = input("[+] Ban co muon nhap MX Record (n)?: ")
                if input_continue in ('y', 'Y'):
                    input_hostname2 = input("\t[-] Nhap hostname (VD: sv.cuong.local):  ")
                    input_ip = input("\t[-] Nhap ip cua hostname: ")
                    if input_hostname2 and input_ip:
                        PTR_ip = ''
                        for i in range(len(input_ip) - 1, 0, -1):
                            if input_ip[i] == '.':
                                PTR_ip = input_ip[i + 1:]
                                os.system("clear")
                                break
                            else:
                                pass
                        i = 0
                        domain_string = ''
                        for element in input_hostname2:
                            if element == ".":
                                domain_string = input_hostname2[i + 1:]
                                break
                            else:
                                i += 1
                        forward_file.write("{0}.\tIN\tMX\t{1}\t{2}.\n".format(domain_string, PTR_ip, input_hostname2))

                else:
                    os.system('clear')
                    break
            forward_file.close()
        elif input_tool_choise  == '3':
            forward_file = open("/etc/bind/forward.linux", "r+")
            forward_file.read()
            while True:
                os.system("clear")
                input_continue = input("[+] Ban co muon nhap MX Record (n)?: ")
                if input_continue in ('y', 'Y'):
                    input_hostname2 = input("\t[-] Nhap hostname (VD: sv.cuong.local):  ")
                    input_CNAME = input("\t[-] Nhap CNAME: ")
                    if input_hostname2 and input_CNAME:
                        PTR_ip = ''
                        for i in range(len(input_ip) - 1, 0, -1):
                            if input_ip[i] == '.':
                                PTR_ip = input_ip[i + 1:]
                                os.system("clear")
                                break
                            else:
                                pass

                        forward_file.write("{0}.\tIN\tCNAME\t{1}.\n".format(input_CNAME, input_hostname2))
                else:
                    os.system('clear')
                    break
            forward_file.close()
        else:
            break


def dns_config():
    print("[-] Dang cai goi...")
    if install_source() == True:
        print("[-] Goi da duoc cai dat")
    else:
        print("""[-] Khong cai duoc goi
                Nguyen nhan:
                1. Khong co internet
                2. Source list""")
        input_exit = input("[-] Nhan phim bat ki de thoat chuonng trinh..........")
        sys.exit()

    input_forwarders = input("[-] Forwarder (Khong bat buoc).\n     VD: 8.8.8.8: ")

    if input_forwarders:
        named_conf_options_file = open("named.conf.options")
        search1_string = "//forwarders"
        replace1_string = "     forwarders {0} {1}; {2};".format("{", input_forwarders, "}")
        subprocess.call("cp named.conf.options options.temple", shell=True)
        replaceAll("options.temple", search1_string, replace1_string)
    else:
        pass


    os.system("clear")

    subprocess.call("systemctl restart bind9", shell=True)

    output_check_status = subprocess.getoutput("systemctl status bind9")
    output_check_status = str(output_check_status)
    check_result = re.search("Active: active", output_check_status)
    check2_result = re.search("Active: inactive", output_check_status)
    os.system('clear')
    if check_result:
        print("[-] DNS server ACTIVE")
        subprocess.call("systemctl enable bind9", shell=True)
        print("[-] DNS server da khoi dong cung he thong")
    elif check2_result:
        print("[-] DNS Server INACTIVE")
    else:
        print("[-] DNS Server Failed")

    os.system('clear')

def executable_menu():
    while True:
        count_exceed2 = 0
        while True:
            os.system("clear")
            print("""
|=|====================================================|=|
|=|    DEBIAN DEMO TOOLS ARE MADE BY CUONGCOLORS       |=|
|=|     This software is built for python3.            |=|
|=|                 DNS                                |=|
|=|     1.  [-] Khoi dong lai DNS server               |=|
|=|     2.  [-] Tat dich vu DNS server                 |=|
|=|     3.  [-] Trang thai dich vu                     |=|
|=|     4.  [-] Bat khoi dong cung he thong            |=|
|=|     5.  [-] Tat khoi dong cung he thong            |=|
|=|     6.  [-] Thay doi dia chi DNS server            |=|
|=|     7.  [-] Cai Dat  DNS Server                    |=|
|=|     8.  [-] Tao Froward Zone                       |=|
|=|     9.  [-] Hien thi dia chi DNS server            |=|
|=|     10. [-] Hien thi Forward file                  |=|
|=|     11. [-] Hien thi Reverse file                  |=|
|=|     12. [-] Hien thi named.conf.local file         |=|
|=|     13. [-] Exit                                   |=|
|=|                                                    |=|
|=|====================================================|=|
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
            subprocess.call("systemctl restart bind9", shell=True)
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '2':
            subprocess.call("systemctl stop bind9", shell=True)
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '3':
            dns_status()
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '4':
            subprocess.call("systemctl enable bind9", shell=True)
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '5':
            subprocess.call("systemctl disable bind9", shell=True)
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '6':
            dns_changer()
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '7':
            dns_config()
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '8':
            create_forward_zone()
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '9':
            subprocess.call("cat /etc/resolv.conf", shell=True)
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '10':
            subprocess.call("cat /etc/bind/forward.linux", shell=True)
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '11':
            subprocess.call("cat /etc/bind/reverse.linux", shell=True)
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '12':
            subprocess.call("cat /etc/bind/named.conf.local", shell=True)
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        else:
            break