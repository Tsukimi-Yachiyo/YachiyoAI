import os

def check():
    if not os.path.exists("src"):
        os.mkdir("src")
        print("src 目录已创建")

    if not os.path.exists("src\\resource"):
        os.mkdir("src\\resource")
        print("src\\resource 目录已创建")

    if not os.path.exists("src\\resource\\json"):
        os.mkdir("src\\resource\\json")
        print("src\\resource\\json 目录已创建")

    if not os.path.exists("src\\resource\\yaml"):
        os.mkdir("src\\resource\\yaml")
        print("src\\resource\\yaml 目录已创建")

def dependency_check():
    import library

    for check_method in library.dependencies["Check"]:
        check_method()
