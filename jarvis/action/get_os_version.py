import platform
# import os

def get_os_version():
    system = platform.system()

    if system == "Darwin":
        # macOS
        return 'macOS ' + platform.mac_ver()[0]
    elif system == "Linux":
        # Linux: 尝试读取 /etc/os-release 文件
        try:
            with open("/etc/os-release") as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith("PRETTY_NAME"):
                        return line.split("=")[1].strip().strip('"')
        except FileNotFoundError:
            pass

        # 如果 /etc/os-release 不存在或无法提供所需信息
        return platform.version()
    else:
        return "Unknown Operating System"
    

def check_os_version(s):
    if "mac" in s or "Ubuntu" in s or "CentOS" in s:
        print("perating System Version:", s)
    else:
        raise ValueError("Unknown Operating System")


if __name__ == "__main__":
    os_version = get_os_version()
    print("Operating System Version:", os_version)