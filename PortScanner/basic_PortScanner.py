import socket
import threading
import time
from concurrent.futures import ThreadPoolExecutor
import argparse

class PortScanner:
    def __init__(self, target, timeout=1.0, max_threads=100):
        self.target = target
        self.timeout = timeout
        self.max_threads = max_threads
        self.open_ports = []
        self.scanned_ports = 0
        
    def scan_port(self, port):
        """Scan a single port"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                result = sock.connect_ex((self.target, port))
                
                if result == 0:
                    service_name = self.get_service_name(port)
                    self.open_ports.append((port, service_name))
                    print(f"Port {port} ({service_name}) is OPEN")
                return result == 0
                
        except Exception as e:
            return False
        finally:
            self.scanned_ports += 1
    
    def get_service_name(self, port):
        """Get service name for a port"""
        try:
            return socket.getservbyport(port)
        except:
            return "unknown"
    
    def scan_range(self, start_port, end_port):
        """Scan a range of ports"""
        print(f"Scanning {self.target} from port {start_port} to {end_port}...")
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            # Submit all port scanning tasks
            futures = [executor.submit(self.scan_port, port) 
                      for port in range(start_port, end_port + 1)]
            
            # Wait for all tasks to complete
            for future in futures:
                future.result()
        
        end_time = time.time()
        self.print_results(start_time, end_time)
    
    def scan_common_ports(self):
        """Scan common ports"""
        common_ports = [
            21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 
            445, 993, 995, 1723, 3306, 3389, 5900, 8080
        ]
        
        print(f"Scanning common ports on {self.target}...")
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = [executor.submit(self.scan_port, port) for port in common_ports]
            for future in futures:
                future.result()
        
        end_time = time.time()
        self.print_results(start_time, end_time)
    
    def print_results(self, start_time, end_time):
        """Print scanning results"""
        print("\n" + "="*50)
        print("SCAN RESULTS")
        print("="*50)
        print(f"Target: {self.target}")
        print(f"Scanned ports: {self.scanned_ports}")
        print(f"Open ports found: {len(self.open_ports)}")
        print(f"Scan duration: {end_time - start_time:.2f} seconds")
        
        if self.open_ports:
            print("\nOpen ports:")
            for port, service in sorted(self.open_ports):
                print(f"  Port {port}: {service}")
        else:
            print("\nNo open ports found.")
        print("="*50)

def main():
    parser = argparse.ArgumentParser(description="Python Port Scanner")
    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument("-p", "--ports", help="Port range (e.g., 1-1000)", default="1-1024")
    parser.add_argument("-t", "--timeout", type=float, help="Timeout in seconds", default=1.0)
    parser.add_argument("--threads", type=int, help="Maximum threads", default=100)
    parser.add_argument("--common", action="store_true", help="Scan common ports only")
    
    args = parser.parse_args()
    
    # Parse port range
    if '-' in args.ports:
        start_port, end_port = map(int, args.ports.split('-'))
    else:
        start_port = end_port = int(args.ports)
    
    # Create scanner instance
    scanner = PortScanner(args.target, args.timeout, args.threads)
    
    try:
        if args.common:
            scanner.scan_common_ports()
        else:
            scanner.scan_range(start_port, end_port)
    except KeyboardInterrupt:
        print("\nScan interrupted by user.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()