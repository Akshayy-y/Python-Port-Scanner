# 🔍 Python Port Scanner

A multi-threaded port scanner written in Python.  
This project contains two versions:

- **Basic Scanner** → Fast multi-threaded scan of single/multiple ports.
- **Advanced Scanner** → Includes banner grabbing for service detection.

⚠️ **Disclaimer**: This project is for **educational and authorized security testing only**.  
Do **NOT** use it against systems without explicit permission.

---

## 🚀 Features
### Basic Scanner
- Multi-threaded port scanning
- Scan single ports, ranges, or common ports
- Detects open ports and associated services

### Advanced Scanner
- All features of the basic scanner
- Service **banner grabbing**
- Export scan results to a file
- Larger set of common ports

---

## 📦 Requirements
Python 3.7 or higher  
No external dependencies (uses Python standard library).

Install requirements (if needed)

🛠 Usage
🔹 Basic Scanner

Run:

python scanners/basic_scanner.py <target> [options]

Examples:

# Scan ports 1–1024 on localhost
python scanners/basic_scanner.py 100.0.0.1

# Scan ports 20–200
python scanners/basic_scanner.py 100.000.0.0 -p 20-200

# Scan common ports only
python scanners/basic_scanner.py example.com --common

🔹 Advanced Scanner

Run:

python scanners/advanced_scanner.py <target> [options]


Examples:

# Scan common ports with banner grabbing
python scanners/advanced_scanner.py 192.168.1.1

# Scan specific range of ports
python scanners/advanced_scanner.py example.com -p 1-1000

# Scan specific ports
python scanners/advanced_scanner.py example.com -p 22,80,443

# Save output to file
python scanners/advanced_scanner.py example.com -p 1-500 -o report.txt
📊 Sample Output
Scanning 127.0.0.1 from port 1 to 1024...
Port 22 (ssh) is OPEN
Port 80 (http) is OPEN
  Banner: HTTP/1.1 200 OK

==================================================
PORT SCAN REPORT
==================================================
Target: 127.0.0.1
Scan time: 2.14 seconds
Open ports: 2

DETAILS:
Port 22 (ssh):
  Banner: None
Port 80 (http):
  Banner: HTTP/1.1 200 OK
==================================================


