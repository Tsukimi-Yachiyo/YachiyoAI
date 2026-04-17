"""
API Key 添加控制器
处理 POST /api/apikey/add 请求
"""

import logging

logger = logging.getLogger(__name__)


@post_controller("/api/apikey/add", "add_api_key")
def add_api_key(request: AddApiKeyRequest):
    """添加 API Key - POST /api/apikey/add"""
    # 使用全局 library 变量，无需 import
    ApiKeyService = library.resource_dependencies["ApiKeyService"]
    
    try:
        api_key_obj = ApiKeyService.add_api_key(
            name=request.name,
            description=request.description,
            key=request.key
        )
        return {
            "success": True,
            "message": "API Key 添加成功",
            "data": {
                "key": api_key_obj.key,
                "name": api_key_obj.name,
                "description": api_key_obj.description
            }
        }
    except ValueError as e:
        logger.error(f"添加 API Key 失败: {e}")
        return {"success": False, "message": str(e)}
    except Exception as e:
        logger.error(f"添加 API Key 异常: {e}")
        return {"success": False, "message": f"服务器错误: {str(e)}"}
