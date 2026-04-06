# YachiyoAI

YachiyoAI 是一个基于 LLM（大语言模型）的智能服务平台，提供了 API 接口、模型集成和工具调用等功能。

## 项目结构

```
YachiyoAI/
├── src/
│   ├── chain/          # 链式处理模块
│   ├── llm/            # 语言模型模块
│   ├── persistent/     # 持久化存储模块
│   ├── tool/           # 工具集成模块
│   ├── __init__.py
│   ├── api.py          # API 接口定义
│   ├── config.py       # 配置管理
│   └── main.py         # 主入口
├── tests/              # 测试目录
├── .env                # 环境变量配置
├── poetry.lock         # 依赖锁定文件
├── poetry.toml         # Poetry 配置
└── pyproject.toml      # 项目依赖配置
```

## 技术栈

- **Python 3.13**
- **FastAPI** - API 框架
- **LangChain** - LLM 应用框架
- **LangGraph** - 状态管理和工作流
- **PostgreSQL** - 数据库
- **Peewee** - ORM 库
- **Uvicorn** - ASGI 服务器

## 安装说明

### 1. 克隆项目

```bash
git clone <repository-url>
cd YachiyoAI
```

### 2. 安装依赖

使用 Poetry 安装项目依赖：

```bash
poetry install
```

### 3. 配置环境变量

复制 `.env` 文件并填写相应的配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，设置以下环境变量：

```
DASHSCOPE_API_KEY=your_dashscope_api_key
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
DB_PORT=your_database_port
MODEL_NAME=your_model_name
BASE_URL=your_base_url
```

## 运行项目

### 开发模式

```bash
poetry run python main.py
```

服务将在 `http://0.0.0.0:5200` 上运行。

### 生产模式

可以使用 Uvicorn 直接运行：

```bash
poetry run uvicorn src.api:create_app --host 0.0.0.0 --port 5200
```

## API 接口

### 根路径

- **URL**: `/`
- **方法**: GET
- **描述**: 返回欢迎信息
- **响应**: `{"message": "Hello World"}`

### 聊天接口

- **URL**: `/chat`
- **方法**: GET
- **描述**: 聊天接口
- **响应**: `{"message": "Chat"}`

### 添加 API Key

- **URL**: `/add_api_key`
- **方法**: POST
- **描述**: 添加 API Key
- **响应**: `{"message": "Add API Key"}`

## 模块说明

### LLM 模块

负责与语言模型的交互，使用 `langchain-openai` 库调用 OpenAI 接口。

### 持久化模块

包含数据库历史记录和 Redis 信息存储功能。

### 工具模块

集成了各种工具，如天气查询等。

## 配置说明

项目使用 Pydantic V2 的 `BaseSettings` 进行配置管理，配置项包括：

- `DASHSCOPE_API_KEY`: 智谱 API 密钥
- `DB_NAME`: 数据库名称
- `DB_USER`: 数据库用户
- `DB_PASSWORD`: 数据库密码
- `DB_HOST`: 数据库主机
- `DB_PORT`: 数据库端口
- `MODEL_NAME`: 模型名称
- `BASE_URL`: API 基础 URL

## 开发指南

### 代码规范

- 使用 Poetry 管理依赖
- 遵循 PEP 8 代码风格
- 使用类型提示

### 测试

运行测试：

```bash
poetry run pytest
```

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

本项目采用 MIT 许可证。
