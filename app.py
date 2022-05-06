from flask import Flask, jsonify, make_response, abort, url_for
from utils import *


STATUS_FILE = "status.txt"

app = Flask(__name__)


# list of packages
@app.route('/api/v1.0/packages', methods=["GET"])
def package_list():
    text_file = read_file(STATUS_FILE)
    packages = get_packages(text_file)
    pkg_dict = convert_to_dict(packages)
    
    pkg_list = {
        "count": len(pkg_dict),
        "packages":[]
    }
    for name in pkg_dict:
        pkg_list["packages"].append(name['package']) 
        
    return jsonify(pkg_list)
    
# package details
@app.route('/api/v1.0/packages/<string:pkg>', methods=["GET"])
def package_details(pkg):
    text_file = read_file(STATUS_FILE)
    packages = get_packages(text_file)
    pkg_dict = convert_to_dict(packages)
    
    reverse_depends = get_reverse_depends(pkg, pkg_dict)
   
    if reverse_depends:
        reverse_depends_list = []
        for rev in reverse_depends:
            reverse_depends_dict = {
                "ref": url_for('package_details', pkg=rev, _external=True),
            }
            reverse_depends_list.append(reverse_depends_dict)
    else:
        reverse_depends_list = None
        
    
    for x in pkg_dict:
        if pkg == x.get("package"):
            if x.get("depends"):
                # check if there are dependencies and alternates
                dep = x.get("depends").replace(" ", "").split("|")
                if len(dep) > 1:
                    depend_to_list = dep[0].split(",")  
                    alternate_to_list = dep[1].split(",")
                else:
                    depend_to_list = dep[0].split(",")
                    alternate_to_list=None
                
                if alternate_to_list:
                    alt_list = []
                    for z in alternate_to_list:
                        t = z.split("(")
                        alternate_name = t[0]
                        alt_dict = {
                            "ref": url_for('package_details', pkg=alternate_name, _external=True),
                        }
                        alt_list.append(alt_dict)
                else: 
                    alt_list = None   
                    
                dep_list = []   
                for i in depend_to_list:
                    y = i.split("(")
                    dependency_name = y[0]
                    dep_dict = {
                        "ref": url_for('package_details', pkg=dependency_name, _external=True),
                    }
                    dep_list.append(dep_dict)
                    
                dependencies = {
                    "dependencies": dep_list,
                    "alternates": alt_list
                }   
            else:
                dependencies = None       

            dictionary_val = {
                "package": x.get("package"),
                "description": x.get("description"),
                "depends": dependencies,
                "reverse_depends": reverse_depends_list,
            }
            return jsonify(dictionary_val)    
    else: 
        abort(404)
   

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)