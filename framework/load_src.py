import ast
import os
import sys
import library


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
        if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Import, ast.ImportFrom)):
            definitions.append(node)

    if not definitions:
        return

    # 构建新的 AST 模块，只包含这些定义
    new_tree = ast.Module(body=definitions, type_ignores=[])
    ast.fix_missing_locations(new_tree)

    # 准备安全的执行环境
    namespace = {}
    safe_globals = {
        "__builtins__": __builtins__,
        "__name__": "__not_main__",  # 阻止模块内的 if __name__ == "__main__" 块
    }

    try:
        code = compile(new_tree, filepath, 'exec')
        # 打印编译后的代码
        exec(code, safe_globals, namespace)
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

    for f in files:
        items = parse_file(f)
        for _, _, obj_name, path in items:
            safe_register(path, obj_name)