import socket
import threading
import time
from concurrent.futures import ThreadPoolExecutor
import argparse
import sys

class AdvancedPortScanner:
    def __init__(self, target, timeout=2.0, max_threads=200):
        self.target = target
        self.timeout = timeout
        self.max_threads = max_threads
        self.open_ports = []
        self.banners = {}
        
    def scan_port(self, port):
        """Scan port and attempt banner grabbing"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                result = sock.connect_ex((self.target, port))
                
                if result == 0:
                    banner = self.grab_banner(sock)
                    service = self.get_service_name(port)
                    
                    self.open_ports.append(port)
                    self.banners[port] = banner
                    
                    print(f"Port {port} ({service}) - OPEN")
                    if banner:
                        print(f"  Banner: {banner.strip()}")
                    return True
                return False
                
        except Exception as e:
            return False
    
    def grab_banner(self, sock):
        """Attempt to grab banner from service"""
        try:
            # Send a basic request to trigger response
            sock.send(b"HEAD / HTTP/1.1\r\n\r\n")
            banner = sock.recv(1024)
            return banner.decode('utf-8', errors='ignore')
        except:
            try:
                # Try a different approach
                banner = sock.recv(1024)
                return banner.decode('utf-8', errors='ignore')
            except:
                return None
    
    def get_service_name(self, port):
        """Get service name for port"""
        try:
            return socket.getservbyport(port)
        except:
            return "unknown"
    
    def scan_ports(self, ports):
        """Scan multiple ports"""
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            list(executor.map(self.scan_port, ports))
        
        end_time = time.time()
        return end_time - start_time
    
    def generate_report(self, scan_time):
        """Generate detailed scan report"""
        report = [
            "="*60,
            "PORT SCAN REPORT",
            "="*60,
            f"Target: {self.target}",
            f"Scan time: {scan_time:.2f} seconds",
            f"Open ports: {len(self.open_ports)}",
            "",
            "DETAILS:"
        ]
        
        for port in sorted(self.open_ports):
            service = self.get_service_name(port)
            banner = self.banners.get(port, "No banner")
            report.append(f"Port {port} ({service}):")
            report.append(f"  Banner: {banner.strip() if banner else 'None'}")
        
        return "\n".join(report)

def get_common_ports():
    """Return list of common ports"""
    return [
        # Web Services
        80, 443, 8080, 8443, 8000, 3000,
        # Email
        25, 110, 143, 465, 587, 993, 995,
        # File Transfer
        21, 22, 69,
        # Database
        1433, 1521, 3306, 5432, 27017,
        # Remote Access
        23, 3389, 5900,
        # Network Services
        53, 67, 68, 161,
        # Other Common
        111, 135, 139, 445, 1723, 3306, 3389, 5900, 8080
    ]

def main():
    parser = argparse.ArgumentParser(description="Advanced Port Scanner")
    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument("-p", "--ports", help="Ports to scan (e.g., 80,443 or 1-1000)", default="common")
    parser.add_argument("-t", "--timeout", type=float, default=2.0, help="Timeout in seconds")
    parser.add_argument("--threads", type=int, default=200, help="Number of threads")
    parser.add_argument("-o", "--output", help="Output file for results")
    
    args = parser.parse_args()
    
    # Determine which ports to scan
    if args.ports == "common":
        ports_to_scan = get_common_ports()
    elif '-' in args.ports:
        start, end = map(int, args.ports.split('-'))
        ports_to_scan = list(range(start, end + 1))
    elif ',' in args.ports:
        ports_to_scan = list(map(int, args.ports.split(',')))
    else:
        ports_to_scan = [int(args.ports)]
    
    print(f"Scanning {len(ports_to_scan)} ports on {args.target}...")
    
    scanner = AdvancedPortScanner(args.target, args.timeout, args.threads)
    
    try:
        scan_time = scanner.scan_ports(ports_to_scan)
        report = scanner.generate_report(scan_time)
        
        print("\n" + report)
        
        # Save to file if requested
        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"\nReport saved to {args.output}")
            
    except KeyboardInterrupt:
        print("\nScan interrupted by user.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()