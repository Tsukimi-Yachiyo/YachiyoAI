"""
API Key 停用控制器
处理 POST /api/apikey/deactivate 请求
"""

import logging

logger = logging.getLogger(__name__)


@post_controller("/api/apikey/deactivate", "deactivate_api_key")
def deactivate_api_key(request: RemoveApiKeyRequest):
    """停用 API Key - POST /api/apikey/deactivate"""
    # 使用全局 library 变量，无需 import
    ApiKeyService = library.resource_dependencies["ApiKeyService"]
    
    try:
        success = ApiKeyService.deactivate_api_key(request.key)
        if success:
            return {"success": True, "message": "API Key 停用成功"}
        else:
            return {"success": False, "message": "API Key 不存在"}
    except Exception as e:
        logger.error(f"停用 API Key 异常: {e}")
        return {"success": False, "message": f"服务器错误: {str(e)}"}
