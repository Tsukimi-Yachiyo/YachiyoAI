"""
API Key 删除控制器
处理 POST /api/apikey/remove 请求
"""

import logging

logger = logging.getLogger(__name__)


@post_controller("/api/apikey/remove", "remove_api_key")
def remove_api_key(request: RemoveApiKeyRequest):
    """删除 API Key - POST /api/apikey/remove"""
    # 使用全局 library 变量，无需 import
    ApiKeyService = library.resource_dependencies["ApiKeyService"]
    
    try:
        success = ApiKeyService.remove_api_key(request.key)
        if success:
            return {"success": True, "message": "API Key 删除成功"}
        else:
            return {"success": False, "message": "API Key 不存在"}
    except Exception as e:
        logger.error(f"删除 API Key 异常: {e}")
        return {"success": False, "message": f"服务器错误: {str(e)}"}
