import ast
import os
import sys
import framework.library as library


def scan_py_files(folder="."):
    files = []
    for root, _, filenames in os.walk(folder):
        for f in filenames:
            if f.endswith(".py") and f != os.path.basename(__file__):
                files.append(os.path.abspath(os.path.join(root, f)))
    return files

def parse_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
    except:
        return []

    dirname = os.path.dirname(filepath)
    if dirname not in sys.path:
        sys.path.insert(0, dirname)

    results = []
    files = []
    for node in ast.walk(tree):
        # 扫描 类 + 函数
        if not isinstance(node, (ast.ClassDef, ast.FunctionDef)):
            continue

        obj_type = "class" if isinstance(node, ast.ClassDef) else "function"
        obj_name = node.name

        # 遍历所有装饰器
        for dec in node.decorator_list:
            dec_name = None
            if isinstance(dec, ast.Name):
                dec_name = dec.id
            elif isinstance(dec, ast.Call) and hasattr(dec.func, 'id'):
                dec_name = dec.func.id

            # 匹配 DECORATOR_MAP
            if dec_name in library.decorator.keys() and filepath not in files:
                results.append((dec_name, obj_type, obj_name, filepath))
                files.append(filepath)
    return results

def safe_register(filepath, obj_name):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
    except:
        return

    try:
        tree = ast.parse(source)
    except:
        return

    # 收集所有顶级函数和类定义（不收集嵌套内部定义，因为会随外部定义一起执行）
    definitions = []
    for node in tree.body:
        print(node)
        if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Import, ast.ImportFrom)):
            definitions.append(node)

    if not definitions:
        return

    # 构建新的 AST 模块，只包含这些定义
    new_tree = ast.Module(body=definitions, type_ignores=[])
    ast.fix_missing_locations(new_tree)

    # 准备安全的执行环境
    namespace = {
        "__builtins__": __builtins__,
        "__name__": "__not_main__",  # 阻止模块内的 if __name__ == "__main__" 块
        "library": library,  # 注入 library 以便访问 resource_dependencies
    }
    
    # 注入所有已注册的 Struct 类（请求模型、响应模型等）
    # 这样 Controller 文件在执行时就能访问到类型注解中的类名
    for struct_name, struct_cls in library.resource_dependencies.items():
        if isinstance(struct_cls, type):  # 只注入类
            namespace[struct_name] = struct_cls

    try:
        code = compile(new_tree, filepath, 'exec')
        # 打印编译后的代码
        exec(code, namespace)
    except Exception:
        import traceback
        traceback.print_exc()
        # 如果执行失败（例如缺少依赖），静默返回
        return

    # 获取目标对象并注册
    obj = namespace.get(obj_name)
    if obj is None:
        return

def run():

    files = scan_py_files()
    
    # 收集所有带装饰器的对象
    all_items = []
    for f in files:
        items = parse_file(f)
        all_items.extend(items)
    
    # 分类：先加载 Struct，再加载其他
    struct_items = []
    other_items = []
    
    for dec_name, obj_type, obj_name, path in all_items:
        if dec_name == "Struct":
            struct_items.append((dec_name, obj_type, obj_name, path))
        else:
            other_items.append((dec_name, obj_type, obj_name, path))
    
    # 第一阶段：加载所有 Struct（请求模型、响应模型等）
    print("=== 第一阶段：加载 Struct（数据结构类） ===")
    for dec_name, obj_type, obj_name, path in struct_items:
        safe_register(path, obj_name)
    
    # 第二阶段：加载其他装饰器（Service、Controller、Method 等）
    print("\n=== 第二阶段：加载其他组件 ===")
    for dec_name, obj_type, obj_name, path in other_items:
        safe_register(path, obj_name)