import framework.library as library


def build():

    # 构建所有服务实例
    for classes in library.dependencies["Service"]:
        library.resource_dependencies[str(classes)] = library.dependencies["Service"][classes].build()

    for build_method_name in library.build_order:
        library.builder[build_method_name[0]]()



