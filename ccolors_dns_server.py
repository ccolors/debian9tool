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
    subprocess.call("mkdir /etc/bind/frd/", shell=True)
    subprocess.call("mkdir /etc/bind/rev/", shell=True)
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
        subprocess.call("touch /etc/resolv.conf", shell=True)
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

        input_forward_zone = input("[-] Nhap domain (bat buoc) VD: cuong.local: ")
        forward_zone_string = """zone \"{0}\" IN {1} 
        type master;
        file \"/etc/bind/frd/{2}\";
        allow-update {3} none; {4};
{5};\n""".format(input_forward_zone, "{", input_forward_zone, "{", "}", "}")
        named_config_local_file = open("/etc/bind/named.conf.local", "r+")
        named_config_local_file.read()
        named_config_local_file.write(forward_zone_string)
        named_config_local_file.close()

        subprocess.call("cp forward.linux {0}".format(input_forward_zone), shell=True)

        while True:
            input_hostname = input("[-] Nhap host server (bat buoc)\n   VD: (sv.cuong.local):   ")
            if input_hostname:
                break
            else:
                os.system("clear")

        replaceAll("{0}".format(input_forward_zone), "localhost_sv", input_hostname)

        i = 0
        for element in input_hostname:
            if element == ".":
                domain_string = input_hostname[i + 1:]
                break
            else:
                i += 1

        replaceAll("{0}".format(input_forward_zone), "root.localhost", "root." + domain_string)

        replace_ttl = input("[-] TTL (default 86400):   ")
        if replace_ttl:
            replaceAll("{0}".format(input_forward_zone), "replace_ttl", replace_ttl)
        else:
            replaceAll("{0}".format(input_forward_zone), "replace_ttl", "86400")

        replace_serial = input("[-] Serial (default 1): ")
        if replace_serial:
            replaceAll("{0}".format(input_forward_zone), "replace_serial", replace_serial)
        else:
            replaceAll("{0}".format(input_forward_zone), "replace_serial", "1")

        replace_refresh = input("[-] Refresh (default 604800):  ")
        if replace_refresh:
            replaceAll("{0}".format(input_forward_zone), "replace_refresh", replace_refresh)
        else:
            replaceAll("{0}".format(input_forward_zone), "replace_refresh", "604800")

        replace_retry = input("[-] Retry (default 86400):   ")
        if replace_retry:
            replaceAll("{0}".format(input_forward_zone), "replace_retry", replace_retry)
        else:
            replaceAll("{0}".format(input_forward_zone), "replace_retry", "86400")

        replace_expire = input("[-] Expire (default 2419200):   ")
        if replace_expire:
            replaceAll("{0}".format(input_forward_zone), "replace_expire", replace_expire)
        else:
            replaceAll("{0}".format(input_forward_zone), "replace_expire", "2419200")

        replace_negative = input("[-] Negative Cache TTL (default 86400):   ")
        if replace_negative:
            replaceAll("{0}".format(input_forward_zone), "replace_negative", replace_negative)
        else:
            replaceAll("{0}".format(input_forward_zone), "replace_negative", "86400")

        i = 0
        hostname_string = ''
        for element in input_hostname:
            if element == ".":
                hostname_string = input_hostname[0:i]
                break
            else:
                i += 1

        move_file("{0}".format(input_forward_zone), "/etc/bind/frd/{0}".format(input_forward_zone))
        print("\n")

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
        file \"/etc/bind/rev/{2}\";
        allow-update {3} none; {4};
{5};\n""".format(input_reverse_zone, "{", input_reverse_zone, "{", "}", "}")
        named_config_local_file = open("/etc/bind/named.conf.local", "r+")
        named_config_local_file.read()
        named_config_local_file.write(reverse_zone_string)
        named_config_local_file.close()

        subprocess.call("cp reverse.linux {0}".format(input_reverse_zone), shell=True)

        while True:
            input_hostname = input("[-] Nhap host server (bat buoc)\n   VD: (sv.cuong.local):   ")
            if input_hostname:
                break
            else:
                os.system("clear")

        replaceAll("{0}".format(input_reverse_zone), "localhost_sv", input_hostname)

        i = 0
        for element in input_hostname:
            if element == ".":
                domain_string = input_hostname[i + 1:]
                break
            else:
                i += 1

        replaceAll("{0}".format(input_reverse_zone), "root.localhost", "root." + domain_string)

        replace_ttl = input("[-] TTL (default 86400):   ")
        if replace_ttl:
            replaceAll("{0}".format(input_reverse_zone), "replace_ttl", replace_ttl)
        else:
            replaceAll("{0}".format(input_reverse_zone), "replace_ttl", "86400")

        replace_serial = input("[-] Serial (default 1): ")
        if replace_serial:
            replaceAll("{0}".format(input_reverse_zone), "replace_serial", replace_serial)
        else:
            replaceAll("{0}".format(input_reverse_zone), "replace_serial", "1")

        replace_refresh = input("[-] Refresh (default 604800):  ")
        if replace_refresh:
            replaceAll("{0}".format(input_reverse_zone), "replace_refresh", replace_refresh)
        else:
            replaceAll("{0}".format(input_reverse_zone), "replace_refresh", "604800")

        replace_retry = input("[-] Retry (default 86400):   ")
        if replace_retry:
            replaceAll("{0}".format(input_reverse_zone), "replace_retry", replace_retry)
        else:
            replaceAll("{0}".format(input_reverse_zone), "replace_retry", "86400")

        replace_expire = input("[-] Expire (default 2419200):   ")
        if replace_expire:
            replaceAll("{0}".format(input_reverse_zone), "replace_expire", replace_expire)
        else:
            replaceAll("{0}".format(input_reverse_zone), "replace_expire", "2419200")

        replace_negative = input("[-] Negative Cache TTL (default 86400):   ")
        if replace_negative:
            replaceAll("{0}".format(input_reverse_zone), "replace_negative", replace_negative)
        else:
            replaceAll("{0}".format(input_reverse_zone), "replace_negative", "86400")

        i = 0
        hostname_string = ''
        for element in input_hostname:
            if element == ".":
                hostname_string = input_hostname[0:i]
                break
            else:
                i += 1

        move_file("{0}".format(input_reverse_zone), "/etc/bind/rev/{0}".format(input_reverse_zone))
        print("\n")

def add_Record():
    while True:
        count_exceed2 = 0
        while True:
            os.system("clear")
            print("""
    |=|====================================================|=|
    |=|                                                    |=| 
    |=|     1. Them A                                      |=|
    |=|     2. Them PTR                                    |=|
    |=|     3. Them MX (mail)                              |=|
    |=|     4. Them CNAME                                  |=|
    |=|     5. Thoat                                       |=|
    |=|                                                    |=|
    |=|====================================================|=|
    """)
            try:
                input_tool_choise = input("[-] Nhap vao lua chon: ")
            except ValueError:
                print("[-] Lua chon khong chinh xac, xin nhap lai.[1]")
            choice_list = ['1', '2', '3', '4', '5']

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
            while True:
                os.system("clear")
                input_continue = input("[+] Ban co muon nhap A Record (N)?: ")
                if  input_continue in ('y', 'Y'):
                    input_domain = input("[-] Nhap domain can them: ")
                    input_hostname2 = input("\t[-] Nhap hostname (VD: server1):  ")
                    input_ip = input("\t[-] Nhap ip cua host: ")
                    forward_file = open("/etc/bind/frd/{0}".format(input_domain), "r+")
                    forward_file.read()
                    forward_file.write("{0}	IN\tA\t{1}\n".format(input_hostname2, input_ip))
                    forward_file.close()
                else:
                    os.system('clear')
                    break

        elif input_tool_choise == '2':
            while True:
                os.system("clear")
                input_continue = input("[+] Ban co muon nhap PTR Record (n)?: ")
                if input_continue in ('y', 'Y'):
                    input_reverseip = input("[-] nhap reverse ip zone (vd: 1.168.192): ")
                    reverse_file = open("/etc/bind/rev/{0}".format(input_reverseip), "r+")
                    reverse_file.read()
                    input_hostname2 = input("\t[-] Nhap host (VD: sv.cuong.local):  ")
                    input_ip = input("\t[-] Nhap ip cua host: ")

                    PTR_ip = ''
                    for i in range(len(input_ip) - 1, 0, -1):
                        if input_ip[i] == '.':
                            PTR_ip = input_ip[i + 1:]
                            os.system("clear")
                            break
                        else:
                            pass

                    reverse_file.write("{0}	IN\tPTR\t{1}.\n".format(PTR_ip, input_hostname2))
                    reverse_file.close()
                else:
                    os.system('clear')
                    break

        elif input_tool_choise == '3':
            while True:
                os.system("clear")
                input_continue = input("[+] Ban co muon nhap MX Record (n)?: ")
                if input_continue in ('y', 'Y'):
                    input_domain = input("[-] Nhap domain can them: ")
                    forward_file = open("/etc/bind/frd/{0}".format(input_domain), "r+")
                    forward_file.read()
                    input_hostname2 = input("\t[-] Nhap host (VD: sv.cuong.local):  ")
                    input_ip = input("\t[-] Nhap ip cua host: ")
                    priority = input("\t[-] Nhap priority(1,2,3...):")
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
                        forward_file.write("@\tIN\tMX\t{0}\t{1}.\n".format(priority, input_hostname2))
                        forward_file.close()
                else:
                    os.system('clear')
                    break
        elif input_tool_choise  == '4':
            while True:
                os.system("clear")
                input_continue = input("[-] Ban co muon nhap CNAME khong (n)? ")
                if input_continue in ('y', 'Y'):
                    input_domain = input("[-] Nhap domain can them CNAME: ")
                    forward_file = open("/etc/bind/frd/{0}".format(input_domain), "r+")
                    forward_file.read()
                    input_hostname2 = input("\t[-] Nhap hostname can them CNAME (VD: server1 ):  ")
                    input_CNAME = input("\t[-] Nhap CNAME (vd: www): ")
                    if input_hostname2 and input_CNAME:
                        forward_file.write("{0}\tIN\tCNAME\t{1}.{2}.\n".format(input_CNAME, input_hostname2, input_domain))
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

def dns_forwarder():
    input_continue = input("[-] Ban co muon nhap ip forwarder (n)? ")
    if input_continue in ('y', 'Y'):
        input_forwarders = input("[-] Forwarder (Khong bat buoc).\n     VD: 8.8.8.8: ")

        if input_forwarders:
            named_conf_options_file = open("named.conf.options")
            search1_string = "//forwarders"
            replace1_string = "     forwarders {0} {1}; {2};".format("{", input_forwarders, "}")
            subprocess.call("cp named.conf.options options.temple", shell=True)
            replaceAll("options.temple", search1_string, replace1_string)
        else:
            pass
        move_file("options.temple", "/etc/bind/named.conf.options")
    else:
        pass

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
|=|     1.  [-] Khoi Dong Lai DNS Server               |=|
|=|     2.  [-] Dung DNS Server                        |=|
|=|     3.  [-] Trang Thai DNS Server                  |=|
|=|     4.  [-] Cho Phep Khoi Dong Cung He Thong       |=|
|=|     5.  [-] Vo Hieu Hoa Khoi Dong Cung He Thong    |=|
|=|     6.  [-] Thay Doi Dia Chi Phan Giai DNS Server  |=|
|=|     7.  [-] Cai Dat DNS Server                     |=|
|=|     8.  [-] Tao Forward Zone                       |=|
|=|     9.  [-] Tao Reverse Zone                       |=|
|=|     10. [+] Them A, CNAME, MX                      |=|
|=|     11. [-] Them IP Forwarder                      |=|
|=|     12. [-] Xem Dia Chi Phan Giai DNS              |=|
|=|     13. [-] Xem Forward Zone                       |=|
|=|     14. [-] Xem Reverse Zone                       |=|
|=|     15. [-] Xem Cau Hinh Zone(named.conf.local)    |=|
|=|     16. [-] Khoi Phuc Mac Dinh                     |=|
|=|     17. [-] Thoat                                  |=|
|=|                                                    |=|
|=|====================================================|=|
        """)
            try:
                input_tool_choise = input("[-] Nhap vao lua chon: ")
            except ValueError:
                print("[-] Lua chon khong chinh xac, xin nhap lai.[1]")
            choice_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17']

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
        elif input_tool_choise =='9':
            create_reverse_zone()
        elif input_tool_choise == '10':
            add_Record()
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '11':
            dns_forwarder()
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '12':
            os.system("clear")
            subprocess.call("cat /etc/resolv.conf", shell=True)
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '13':
            os.system('clear')
            print("Danh sach domain:\n", subprocess.getoutput("ls /etc/bind/frd"), "\n")
            input_forward = input("[-] Nhap forward zone: ")
            subprocess.call("cat /etc/bind/frd/{0}".format(input_forward), shell=True)
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '14':
            os.system('clear')
            print("Danh sach reverse ip :\n", subprocess.getoutput("ls /etc/bind/rev"), "\n")
            input_reverse = input("[-] Nhap reverse zone: ")
            subprocess.call("cat /etc/bind/rev/{0}".format(input_reverse), shell=True)
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '15':
            subprocess.call("cat /etc/bind/named.conf.local", shell=True)
            input_continute_key = input("\n[-] Nhan phim bat ky de tiep tuc chuong trinh[1]")
        elif input_tool_choise == '16':
            print("[-] Tien trinh khoi phuc mac dinh...")
            subprocess.call("rm -rf /etc/bind/", shell=True)
            subprocess.call("cp -r bind/ /etc/", shell=True)
            time.sleep(2)
        else:
            break