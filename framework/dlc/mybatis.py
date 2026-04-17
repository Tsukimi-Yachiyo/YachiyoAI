import peewee
from peewee import *
import inspect
import functools
import logging
import framework.library as library

logger = logging.getLogger(__name__)


class Main(BaseMain):
    """
    MyBatis Plus 主类
    提供数据库连接、Base 模型和常见数据库操作功能
    """

    init_order = 10
    build_order = 10

    def __init__(self):
        # 支持多种数据库类型
        db_type = library.resource_yaml.get("framework.database.type", "sqlite")
        
        if db_type == "sqlite":
            db_path = library.resource_yaml.get("framework.database.path", "database.db")
            db = SqliteDatabase(db_path)
        elif db_type == "postgresql":
            db = PostgresqlDatabase(
                library.resource_yaml["framework.database.name"],
                user=library.resource_yaml["framework.database.username"],
                password=library.resource_yaml["framework.database.password"],
                host=library.resource_yaml.get("framework.database.host", "localhost"),
                port=library.resource_yaml.get("framework.database.port", 5432),
            )
        elif db_type == "mysql":
            db = MySQLDatabase(
                library.resource_yaml["framework.database.name"],
                user=library.resource_yaml["framework.database.username"],
                password=library.resource_yaml["framework.database.password"],
                host=library.resource_yaml.get("framework.database.host", "localhost"),
                port=library.resource_yaml.get("framework.database.port", 3306),
            )
        else:
            raise ValueError(f"不支持的数据库类型: {db_type}")

        class Base(Model):
            class Meta:
                database = db

        self.db = db
        self.Base = Base

        # 确保 model 结构存在
        if "model" not in library.dependencies:
            library.dependencies["model"] = {}
        
        library.dependencies["model"]["db"] = self.db
        library.dependencies["model"]["Base"] = self.Base
        library.resource["mybatis_db"] = self.db
        library.resource["mybatis_base"] = self.Base
        
        # 把 peewee 模块和所有字段类嵌入到全局命名空间
        __builtins__["peewee"] = peewee
        __builtins__["AutoField"] = AutoField
        __builtins__["CharField"] = CharField
        __builtins__["IntegerField"] = IntegerField
        __builtins__["FloatField"] = FloatField
        __builtins__["DecimalField"] = DecimalField
        __builtins__["BooleanField"] = BooleanField
        __builtins__["DateField"] = DateField
        __builtins__["DateTimeField"] = DateTimeField
        __builtins__["TimeField"] = TimeField
        __builtins__["TextField"] = TextField
        __builtins__["BlobField"] = BlobField
        __builtins__["UUIDField"] = UUIDField
        __builtins__["ForeignKeyField"] = ForeignKeyField
        __builtins__["ManyToManyField"] = ManyToManyField
        __builtins__["SQL"] = SQL
        
        logger.info(f"MyBatis Plus 插件初始化成功，数据库类型: {db_type}")

    @staticmethod
    def check():
        yaml_need = ["framework.database.type"]
        if any(key not in library.resource_yaml for key in yaml_need):
            raise ValueError("mybatis 配置文件中缺少数据库类型配置")
        
        db_type = library.resource_yaml.get("framework.database.type")
        if db_type in ["postgresql", "mysql"]:
            db_need = [
                "framework.database.name", 
                "framework.database.username", 
                "framework.database.password"
            ]
            if any(key not in library.resource_yaml for key in db_need):
                raise ValueError("mybatis 配置文件中缺少数据库连接配置")

    def build(self):
        # 创建所有已注册的表
        try:
            self.db.connect()
            mapper_models = library.dependencies.get("model", {}).get("MapperModels", [])
            self.db.create_tables(mapper_models, safe=True)
            logger.info("数据库表创建成功")
        except Exception as e:
            logger.warning(f"表创建时可能已存在: {e}")
        finally:
            if not self.db.is_closed():
                self.db.close()
        logger.info("MyBatis Plus 插件构建完成")


class Mapper(Decorator):
    """
    Mapper 装饰器
    将类映射为数据库表模型
    """

    def __init__(self, table_name: str = None):
        if table_name is None:
            logger.error("Mapper 装饰器需要 table_name 参数")
        self.table_name = table_name
        # 确保 model 结构存在
        if "model" not in library.dependencies:
            library.dependencies["model"] = {}
        if "MapperModels" not in library.dependencies["model"]:
            library.dependencies["model"]["MapperModels"] = []

    def __call__(self, cls):
        Base = library.dependencies["model"]["Base"]
        attrs = get_class_attrs(cls)

        class BaseModel(Base):
            class Meta:
                database = library.dependencies["model"]["db"]

        class Model(BaseModel):
            class Meta:
                table_name = self.table_name

        for name, attr_type in attrs.items():
            setattr(Model, name, attr_type)
        
        # 确保 Mapper 结构存在
        if "Mapper" not in library.dependencies:
            library.dependencies["Mapper"] = {}
        
        # 存储模型以便创建表
        library.dependencies["model"]["MapperModels"].append(Model)
        library.dependencies["model"][f"Mapper_{cls.__name__}"] = Model
        library.dependencies["Mapper"][cls.__name__] = Model
        logger.info(f"Mapper {cls.__name__} 已映射到表 {self.table_name}")
        
        return Model

    def build(self):
        return Mapper(self.table_name)


def get_class_attrs(cls):
    """
    获取类属性
    """
    attrs = {}
    for name, value in cls.__dict__.items():
        if not name.startswith('__') and not callable(value):
            attrs[name] = value
    return attrs


class QueryWrapper:
    """
    查询包装器 - 类似 MyBatis Plus 的 QueryWrapper
    """

    def __init__(self, model):
        self.model = model
        self.query = model.select()
        self.conditions = []

    def eq(self, field, value):
        """等于"""
        self.query = self.query.where(getattr(self.model, field) == value)
        return self

    def ne(self, field, value):
        """不等于"""
        self.query = self.query.where(getattr(self.model, field) != value)
        return self

    def gt(self, field, value):
        """大于"""
        self.query = self.query.where(getattr(self.model, field) > value)
        return self

    def ge(self, field, value):
        """大于等于"""
        self.query = self.query.where(getattr(self.model, field) >= value)
        return self

    def lt(self, field, value):
        """小于"""
        self.query = self.query.where(getattr(self.model, field) < value)
        return self

    def le(self, field, value):
        """小于等于"""
        self.query = self.query.where(getattr(self.model, field) <= value)
        return self

    def like(self, field, value):
        """模糊查询"""
        self.query = self.query.where(getattr(self.model, field).contains(value))
        return self

    def like_left(self, field, value):
        """左模糊"""
        self.query = self.query.where(getattr(self.model, field).endswith(value))
        return self

    def like_right(self, field, value):
        """右模糊"""
        self.query = self.query.where(getattr(self.model, field).startswith(value))
        return self

    def between(self, field, start, end):
        """区间查询"""
        self.query = self.query.where(
            (getattr(self.model, field) >= start) & 
            (getattr(self.model, field) <= end)
        )
        return self

    def is_null(self, field):
        """为空"""
        self.query = self.query.where(getattr(self.model, field).is_null())
        return self

    def is_not_null(self, field):
        """不为空"""
        self.query = self.query.where(getattr(self.model, field).is_null(False))
        return self

    def order_by(self, field, asc=True):
        """排序"""
        field_obj = getattr(self.model, field)
        if asc:
            self.query = self.query.order_by(field_obj)
        else:
            self.query = self.query.order_by(field_obj.desc())
        return self

    def limit(self, count):
        """限制数量"""
        self.query = self.query.limit(count)
        return self

    def offset(self, count):
        """偏移量"""
        self.query = self.query.offset(count)
        return self

    def page(self, page_num, page_size):
        """分页"""
        self.query = self.query.offset((page_num - 1) * page_size).limit(page_size)
        return self

    def list(self):
        """获取列表"""
        return list(self.query)

    def one(self):
        """获取一条"""
        return self.query.first()

    def count(self):
        """计数"""
        return self.query.count()

    def exists(self):
        """是否存在"""
        return self.query.exists()


def query_wrapper(model):
    """
    创建查询包装器的快捷方法
    """
    return QueryWrapper(model)


def insert_batch(model, data_list):
    """
    批量插入 - 类似 MyBatis Plus 的 saveBatch
    """
    db = library.dependencies.get("model", {}).get("db", library.dependencies.get("db"))
    with db.atomic():
        for data in data_list:
            model.create(**data)
    logger.info(f"批量插入 {len(data_list)} 条记录到 {model._meta.table_name}")


def update_batch(model, data_list, id_field="id"):
    """
    批量更新 - 类似 MyBatis Plus 的 updateBatchById
    """
    db = library.dependencies.get("model", {}).get("db", library.dependencies.get("db"))
    with db.atomic():
        for data in data_list:
            if id_field in data:
                model.update(**data).where(
                    getattr(model, id_field) == data[id_field]
                ).execute()
    logger.info(f"批量更新 {len(data_list)} 条记录到 {model._meta.table_name}")


def remove_by_id(model, id_value, id_field="id"):
    """
    根据 ID 删除 - 类似 MyBatis Plus 的 removeById
    """
    count = model.delete().where(getattr(model, id_field) == id_value).execute()
    logger.info(f"删除 {count} 条记录从 {model._meta.table_name}")
    return count


def remove_by_ids(model, id_list, id_field="id"):
    """
    根据 ID 列表批量删除 - 类似 MyBatis Plus 的 removeByIds
    """
    count = model.delete().where(getattr(model, id_field).in_(id_list)).execute()
    logger.info(f"批量删除 {count} 条记录从 {model._meta.table_name}")
    return count


def get_by_id(model, id_value, id_field="id"):
    """
    根据 ID 查询 - 类似 MyBatis Plus 的 getById
    """
    try:
        return model.get(getattr(model, id_field) == id_value)
    except model.DoesNotExist:
        return None


def list_by_ids(model, id_list, id_field="id"):
    """
    根据 ID 列表查询 - 类似 MyBatis Plus 的 listByIds
    """
    return list(model.select().where(getattr(model, id_field).in_(id_list)))


def save(model, **kwargs):
    """
    保存单条记录 - 类似 MyBatis Plus 的 save
    """
    instance = model.create(**kwargs)
    logger.info(f"保存记录到 {model._meta.table_name}, ID: {instance.id if hasattr(instance, 'id') else 'N/A'}")
    return instance


def update_by_id(model, id_value, data, id_field="id"):
    """
    根据 ID 更新 - 类似 MyBatis Plus 的 updateById
    """
    count = model.update(**data).where(getattr(model, id_field) == id_value).execute()
    logger.info(f"更新 {count} 条记录到 {model._meta.table_name}")
    return count


def count(model, *conditions):
    """
    计数 - 类似 MyBatis Plus 的 count
    """
    query = model.select()
    if conditions:
        query = query.where(*conditions)
    return query.count()


# 注册装饰器和工具函数
library.decorator["Mapper"] = Mapper
library.decorator["QueryWrapper"] = query_wrapper
library.resource["mybatis_query_wrapper"] = query_wrapper
library.resource["mybatis_insert_batch"] = insert_batch
library.resource["mybatis_update_batch"] = update_batch
library.resource["mybatis_remove_by_id"] = remove_by_id
library.resource["mybatis_remove_by_ids"] = remove_by_ids
library.resource["mybatis_get_by_id"] = get_by_id
library.resource["mybatis_list_by_ids"] = list_by_ids
library.resource["mybatis_save"] = save
library.resource["mybatis_update_by_id"] = update_by_id
library.resource["mybatis_count"] = count
