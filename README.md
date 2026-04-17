# Python Spring Framework

一个模仿 Spring 框架风格设计的 Python 轻量级开发框架，提供依赖注入、注解开发、资源管理、插件扩展和 MyBatis Plus 风格的 ORM 功能。

## 快速开始

### 项目启动

使用 `main.py` 启动项目。

### 安装依赖

```bash
pip install -r requirements.txt
```

### 项目结构

```
text/
├── main.py                # 项目启动文件
├── requirements.txt       # 依赖包列表
├── framework/             # 框架核心目录
│   ├── __init__.py        # 框架初始化
│   ├── run.py            # 框架运行主入口
│   ├── build.py          # 服务构建
│   ├── library.py        # 核心库管理
│   ├── check.py          # 环境检查
│   ├── load_src.py       # 源文件加载
│   ├── load_dlc.py       # DLC插件加载
│   ├── public_modules.py # 公共模块
│   ├── default.py        # 默认配置
│   ├── dlc/              # DLC插件目录
│   │   ├── web.py        # Web服务插件
│   │   ├── embed.py      # 嵌入插件
│   │   ├── langgraph.py  # LangGraph插件
│   │   └── mybatis.py    # MyBatis Plus插件
│   └── resource/         # 资源管理目录
│       ├── config.py     # 环境变量配置
│       ├── json.py       # JSON资源加载
│       ├── logging.py    # 日志配置
│       └── yml.py        # YAML资源加载
└── src/                   # 用户代码目录
    └── resource/         # 资源文件目录
        ├── json/         # JSON资源文件
        └── yaml/         # YAML资源文件
```

## 核心功能

### 1. 服务注册 (@Service)

使用 `@Service` 装饰器将类注册为服务：

```python
@Service
class MyService:
    def __init__(self):
        self.value = "Hello World"
    
    def do_something(self):
        return self.value
```

### 2. 依赖注入 (@auto_inject, @Method)

使用 `@auto_inject` 装饰器自动注入依赖：

```python
@auto_inject()
def my_function(service: MyService, config: str):
    return service.do_something() + config
```

使用 `@Method` 装饰器将方法注册为服务方法，用法和 `@auto_inject` 相同：

```python
@Method()
def get_user(userId: int):
    return db.query(f"SELECT * FROM users WHERE id = {userId}")
```

支持两种参数注入方式：
- **同名参数注入**：`@auto_inject("param1", "param2")`
- **自定义参数注入**：`@auto_inject(custom_name="original_name")`

### 3. 资源管理

框架支持多种资源加载方式：

#### YAML 配置

在 `src/resource/yaml/` 目录下放置 YAML 文件，支持 `${key}` 占位符引用。

```python
# 获取 YAML 配置
from framework.library import get_resource_yaml
value = get_resource_yaml("config.key")
```

#### JSON 配置

在 `src/resource/json/` 目录下放置 JSON 文件。

```python
# 获取 JSON 配置
from framework.library import get_resource_json
data = get_resource_json("filename")
```

#### 环境变量

```python
# 获取环境变量
from framework.library import get_resource_config
value = get_resource_config("ENV_VAR")
```

#### 自定义资源

```python
# 设置资源
from framework.library import set_resource, get_resource
set_resource("my_key", "my_value")
value = get_resource("my_key")
```

## DLC 插件系统

框架支持通过 DLC（Downloadable Content）插件扩展功能。

### MyBatis Plus 插件 (mybatis.py)

提供类似 MyBatis Plus 的 ORM 功能，基于 Peewee 实现。

#### 配置文件

在 `src/resource/yaml/` 下创建 `framework.yaml`：

```yaml
framework:
  database:
    type: sqlite  # 支持 sqlite, mysql, postgresql
    path: test.db  # sqlite 专用
    # MySQL/PostgreSQL 配置
    # name: database_name
    # username: root
    # password: password
    # host: localhost
    # port: 3306
```

#### Mapper 定义

使用 `@Mapper` 装饰器定义数据库表模型：

```python
@Mapper(table_name="users")
class User:
    id = AutoField()
    username = CharField(unique=True)
    password = CharField()
    email = CharField(null=True)
    created_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
```

#### 常用数据库操作

```python
# 保存单条记录 - save
save(User, username="admin", password="123456", email="admin@example.com")

# 批量插入 - insertBatch
insert_batch(User, [
    {"username": "user1", "password": "pass1"},
    {"username": "user2", "password": "pass2"}
])

# 根据 ID 查询 - getById
user = get_by_id(User, 1)

# 根据 ID 列表查询 - listByIds
users = list_by_ids(User, [1, 2, 3])

# 根据 ID 更新 - updateById
update_by_id(User, 1, {"password": "new_password"})

# 批量更新 - updateBatchById
update_batch(User, [
    {"id": 1, "email": "new1@example.com"},
    {"id": 2, "email": "new2@example.com"}
])

# 根据 ID 删除 - removeById
remove_by_id(User, 1)

# 根据 ID 列表批量删除 - removeByIds
remove_by_ids(User, [1, 2, 3])

# 计数 - count
user_count = count(User)
```

#### QueryWrapper 查询包装器

提供类似 MyBatis Plus 的 QueryWrapper 链式查询：

```python
# 创建查询包装器
qw = query_wrapper(User)

# 链式查询
users = qw.eq("username", "admin") \
         .like("email", "@example.com") \
         .between("id", 1, 10) \
         .order_by("created_at", asc=False) \
         .page(1, 10) \
         .list()

# 获取单条
user = qw.eq("id", 1).one()

# 计数
count = qw.like("username", "user").count()

# 是否存在
exists = qw.eq("username", "admin").exists()
```

QueryWrapper 支持的方法：
- `eq(field, value)` - 等于
- `ne(field, value)` - 不等于
- `gt(field, value)` - 大于
- `ge(field, value)` - 大于等于
- `lt(field, value)` - 小于
- `le(field, value)` - 小于等于
- `like(field, value)` - 模糊查询
- `like_left(field, value)` - 左模糊
- `like_right(field, value)` - 右模糊
- `between(field, start, end)` - 区间查询
- `is_null(field)` - 为空
- `is_not_null(field)` - 不为空
- `order_by(field, asc=True)` - 排序
- `limit(count)` - 限制数量
- `offset(count)` - 偏移量
- `page(page_num, page_size)` - 分页
- `list()` - 获取列表
- `one()` - 获取一条
- `count()` - 计数
- `exists()` - 是否存在

### Web 插件 (web.py)

提供 FastAPI Web 服务功能。

#### 配置文件

在 `src/resource/yaml/` 下创建 `service.yaml`：

```yaml
service:
  title: "My Service"
  version: "1.0.0"
  host: "0.0.0.0"
  port: 8000
```

#### 控制器定义

```python
@controller(path="/api", name="my_controller")
def my_controller():
    return {"message": "Hello"}
```

### 嵌入插件 (embed.py)

将所有依赖项、装饰器和配置嵌入到全局命名空间中，便于直接使用。

### LangGraph 插件 (langgraph.py)

集成 LangGraph 用于构建复杂的 LLM 应用工作流。

```python
@langgraph_node(name="my_node")
def my_node(state):
    # 处理状态
    return state
```

## 核心模块说明

### framework/__init__.py
框架初始化模块，负责：
- 初始化环境
- 检查并创建必要目录
- 配置日志系统

### framework/run.py
框架运行主入口，流程：
1. 加载 DLC 插件
2. 加载用户源文件
3. 构建服务
4. 运行主循环

### framework/build.py
服务构建模块，负责：
- 实例化所有服务
- 执行构建器方法
- 启动主循环

### framework/library.py
核心库管理，维护：
- `dependencies`: 依赖库
- `decorator`: 装饰器
- `builder`: 构建器
- `loop_method`: 主循环方法
- `resource`: 用户资源
- `resource_yaml`: YAML 配置
- `resource_json`: JSON 配置
- `resource_dependencies`: 服务实例

### framework/load_src.py
源文件加载器，使用 AST 解析用户代码，安全加载带有装饰器的类和函数。

### framework/load_dlc.py
DLC 插件加载器，扫描并加载 `framework/dlc/` 目录下的插件。

## 开发示例

### 完整 MyBatis Plus 示例

```python
from framework.public_modules import Service, auto_inject, Method, Mapper

@Mapper(table_name="users")
class User:
    id = AutoField()
    username = CharField(unique=True)
    password = CharField()
    email = CharField(null=True)
    created_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])

@Service
class UserService:
    
    @auto_inject()
    def __init__(self, service_title: str):
        import framework.library as library
        print("UserService 初始化")
        self.User = library.dependencies["Mapper"]["User"]
    
    def add_user(self, username, password, email=None):
        """添加用户 - 类似 MyBatis Plus 的 save"""
        user = save(self.User, username=username, password=password, email=email)
        return user
    
    def list_all_users(self):
        """查询所有用户"""
        return list(self.User.select())
    
    def count_users(self):
        """统计用户数量 - 类似 MyBatis Plus 的 count"""
        return count(self.User)

@Method()
def test_mybatis_plus(service_title: str):
    """测试 MyBatis Plus 功能"""
    print(f"服务标题: {service_title}")
    
    import framework.library as library
    user_service = library.resource_dependencies["UserService"]
    
    # 添加用户
    user1 = user_service.add_user("admin", "123456", "admin@example.com")
    
    # 查询所有用户
    all_users = user_service.list_all_users()
    
    # 统计用户数量
    user_count = user_service.count_users()
```

### 启动文件 (main.py)

```python
from framework import run
import framework.library as library

print("=== 启动 Python Spring Framework ===")
run.run()

print("\n=== 框架启动完成，开始测试 ===")

# 调用测试方法
test_func = library.dependencies["Method"]["test_mybatis_plus"]
test_func()
```

## 注意事项

1. 所有用户代码应放在 `src/` 目录下
2. 资源文件应放在 `src/resource/` 对应的子目录中
3. 使用 `@Service` 装饰器的类会被自动实例化
4. `@auto_inject` 和 `@Method` 需要配合类型注解使用
5. MyBatis Plus 插件会自动将 peewee 的字段类嵌入到全局命名空间
6. 禁用 DLC 插件可以在 `framework.yaml` 中配置 `framework.disable_dlc`

## 依赖库

- `pyyaml`: YAML 配置文件解析
- `python-dotenv`: 环境变量加载
- `peewee`: ORM 数据库操作
- `fastapi`: Web 服务（可选）
- `uvicorn`: ASGI 服务器（可选）
- `langgraph`: 工作流编排（可选）
