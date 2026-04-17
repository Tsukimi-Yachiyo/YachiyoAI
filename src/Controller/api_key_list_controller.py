"""
API Key 列表控制器
处理 GET /api/apikey/list 请求
"""

import logging

logger = logging.getLogger(__name__)


@get_controller("/api/apikey/list", "list_api_keys")
def list_api_keys(include_inactive: bool = False):
    """列出所有 API Key - GET /api/apikey/list"""
    # 使用全局 library 变量，无需 import
    ApiKeyService = library.resource_dependencies["ApiKeyService"]
    
    try:
        api_keys = ApiKeyService.list_all_api_keys(include_inactive=include_inactive)
        return {
            "success": True,
            "data": {
                "count": len(api_keys),
                "keys": [
                    {
                        "key": key_obj.key,
                        "name": key_obj.name,
                        "description": key_obj.description,
                        "is_active": key_obj.is_active
                    }
                    for key_obj in api_keys
                ]
            }
        }
    except Exception as e:
        logger.error(f"列出 API Key 异常: {e}")
        return {"success": False, "message": f"服务器错误: {str(e)}"}
