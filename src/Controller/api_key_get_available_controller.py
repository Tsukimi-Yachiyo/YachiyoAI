"""
API Key 获取可用控制器
处理 GET /api/apikey/get-available 请求
"""

import logging

logger = logging.getLogger(__name__)


@get_controller("/api/apikey/get-available", "get_available_api_key")
def get_available_api_key():
    """获取可用 API Key - GET /api/apikey/get-available"""
    # 使用全局 library 变量，无需 import
    ApiKeyService = library.resource_dependencies["ApiKeyService"]
    
    try:
        api_key = ApiKeyService.get_available_api_key()
        if api_key:
            return {
                "success": True,
                "data": {
                    "key": api_key
                }
            }
        else:
            return {"success": False, "message": "没有可用的 API Key"}
    except Exception as e:
        logger.error(f"获取可用 API Key 异常: {e}")
        return {"success": False, "message": f"服务器错误: {str(e)}"}
