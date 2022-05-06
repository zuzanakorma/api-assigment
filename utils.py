import re


def get_raw_info(text):
    # Extract package keys and values
    split_regex = re.compile(r"^[A-Za-z-]+:\s", flags=re.MULTILINE)
    keys = [key[:-2].lower() for key in split_regex.findall(text)]
    values = [value.strip() for value in re.split(split_regex, text)[1:]]

    # Composing initial package info dict
    if len(values) > 0:
        pkg_details = dict(zip(keys[0:], values[0:]))
        return pkg_details
    else:
        raise ValueError("Not a dpkg file!")
    
def read_file(filename):
    with open(filename, "r") as f:
        content = f.read().strip()
    return content
 
def get_packages(text):
    packages = text.split("\n\n")
    return packages
    
def convert_to_dict(package_list):   
    pkg_info = []
    for pkg in package_list:
        pkg_info.append(get_raw_info(pkg))
        
    return pkg_info

def get_reverse_depends(pkg_name, pkg_dict_list):
    r_depends = []
    for pkg in pkg_dict_list:
        pkg_depends = pkg.get("depends")
        if pkg_depends is not None:
            if pkg_name in pkg_depends:
                r_depends.append(pkg["package"])

    return None if len(r_depends) == 0 else r_depends
