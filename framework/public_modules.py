import functools
import library

import logging
import inspect


logger = logging.getLogger(__name__)

"""
    服务装饰器
"""
class Service:
    def __init__(self, cls):
        self.cls = cls

        library.dependencies["Service"][self.cls.__name__] = self
        logger.info(f"Service {self.cls.__name__} 已加入库")

    def __call__(self, *args, **kwargs):
        logger.info(f"Service {self.cls.__name__} 已调用, 这是不推荐的用法, 请使用 auto_inject")
        return self.cls(*args, **kwargs)

    def __str__(self):
        return self.cls.__name__

    def build(self):
        return self.cls

"""
    方法修饰器
    将方法入库的自动注入修饰器
"""
def Method(*same_name_args, **customize_args):
    def decorator(func):
        wrapped_func = auto_inject(*same_name_args, **customize_args)(func)
        library.dependencies["Method"][func.__name__] = wrapped_func
        logger.info(f"Method {func.__name__} 已加入库")
        return wrapped_func
    return decorator


"""
    自动注入装饰器
    :param same_name_args: 同名参数
        例如: same_name_args = ("model", "compress_model")
    :param customize_args: 自定义参数
        例如: customize_args = {"model": "model", "compress_model": "compress_model"}
    :return: 装饰器
    
    当调用函数时, 会自动注入同名参数和自定义参数
"""
def auto_inject(*same_name_args, **customize_args):
    def decorator(func):
        nonlocal same_name_args
        param_types = get_param_types(func)

        # 检查参数数量是否正确
        len_param_types = len(param_types)
        len_args = len(same_name_args)+len(customize_args)
        if len_args == 0:
            # 自动注入同名参数
            same_name_args = param_types.keys()
        elif len_args != len_param_types:
            logger.error(f"调用函数 {func.__name__}, 参数数量错误, 应该是 {len_param_types}")
            raise ValueError(f"参数数量错误, 应该是 {len_param_types}")

        # 检测自定义参数是否存在
        for param_item in customize_args.keys():
            if param_item not in param_types.keys():
                logger.error(f"调用函数 {func.__name__}, 参数 {param_item} 不存在")
                raise ValueError(f"参数 {param_item} 不存在")

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            args_len = len(args)
            kwargs_len = len(kwargs)

            # 检查参数数量是否正确
            if args_len + kwargs_len > len_param_types:
                logger.error(f"调用函数 {func.__name__}, 参数数量错误, 最多是 {len_param_types}")
                raise ValueError(f"参数数量错误, 最多是 {len_param_types}")

            # 检查参数类型是否正确
            for param_item_ in kwargs.keys():
                try :
                    if type(kwargs[param_item_]) != param_types[param_item_] and type(kwargs[param_item_]) is not None:
                        logger.error(f"调用函数 {func.__name__}, 参数 {param_item_} 类型错误, 应该是 {param_types[param_item_]}")
                        raise TypeError(f"参数 {param_item_} 类型错误, 应该是 {param_types[param_item_]}")
                except KeyError:
                    logger.error(f"调用函数 {func.__name__}, 参数 {param_item_} 不存在")
                    raise ValueError(f"参数 {param_item_} 不存在")
            for index, arg in enumerate(args):
                param_type = list(param_types.values())[index]
                if type(arg) != param_type and type(arg) is not None:
                    logger.error(f"调用函数 {func.__name__}, 第 {index} 个参数 类型错误, 应该是 {param_type}")

            # 开始自动注入参数
            inject_args = [x for x in list(param_types.keys())[args_len:] if x not in kwargs.keys()]
            for param_item_ in inject_args:
                if param_item_ not in same_name_args:
                    param_item_ = customize_args[param_item_]
                try:
                    match param_types[param_item_]:
                        # 字符串, 整数, 浮点数, 布尔类型, 从 resource_yaml 中获取
                        case type() as t if t in (str, int, float, bool):
                            kwargs[param_item_] = library.resource_yaml[param_item_.replace("_", ".")]
                        # 字典, 列表类型, 从 resource_json 中获取
                        case type() as t if t in (dict, list):
                            kwargs[param_item_] = library.resource_json[param_item_]
                        # 其他类型, 从 resource_dependencies 中获取
                        case _:
                            kwargs[param_item_] = library.resource_dependencies[param_item_]
                except KeyError:
                    try:
                        # 如果 找不到 尝试从 resource 中获取
                        kwargs[param_item_] = library.resource[param_item_]
                    except KeyError:
                        logger.error(f"调用函数 {func.__name__}, 参数 {param_item_} 不存在")
                        raise ValueError(f"参数 {param_item_} 不存在")
            return func(*args, **kwargs)
        return wrapper
    return decorator

def get_param_types(func):
    sig = inspect.signature(func)
    param_types = {}
    for name, param in sig.parameters.items():
        param_types[name] = param.annotation
    return param_types

library.decorator["Service"] = Service
library.decorator["auto_inject"] = auto_inject
library.decorator["Method"] = Method

