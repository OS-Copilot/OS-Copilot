import platform

def get_os_version():
    """
    Determines the operating system version of the current system.

    This function checks the operating system of the current environments and attempts
    to return a human-readable version string. For macOS, it uses the `platform.mac_ver()`
    method. For Linux, it attempts to read the version information from `/etc/os-release`.
    If the system is not macOS or Linux, or if the Linux version cannot be determined, it
    defaults to a generic version string or "Unknown Operating System".

    Returns:
        str: A string describing the operating system version, or "Unknown Operating System"
             if the version cannot be determined.
    """
    system = platform.system()

    if system == "Darwin":
        # macOS
        return 'macOS ' + platform.mac_ver()[0]
    elif system == "Linux":
        try:
            with open("/etc/os-release") as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith("PRETTY_NAME"):
                        return line.split("=")[1].strip().strip('"')
        except FileNotFoundError:
            pass

        return platform.version()
    else:
        return "Unknown Operating System"
    

def check_os_version(s):
    """
    Checks if the operating system version string matches known supported versions.

    This function examines a given operating system version string to determine if it
    contains known substrings that indicate support (e.g., "mac", "Ubuntu", "CentOS").
    If the version string does not match any of the known supported versions, it raises
    a ValueError.

    Args:
        s (str): The operating system version string to check.

    Raises:
        ValueError: If the operating system version is not recognized as a known
                    supported version.
    """
    if "mac" in s or "Ubuntu" in s or "CentOS" in s:
        print("perating System Version:", s)
    else:
        raise ValueError("Unknown Operating System")


if __name__ == "__main__":
    os_version = get_os_version()
    print("Operating System Version:", os_version)