"""
API Key 验证控制器
处理 GET /api/apikey/validate 请求
"""

import logging

logger = logging.getLogger(__name__)


@get_controller("/api/apikey/validate", "validate_api_key")
def validate_api_key(key: str):
    """验证 API Key - GET /api/apikey/validate"""
    # 使用全局 library 变量，无需 import
    ApiKeyService = library.resource_dependencies["ApiKeyService"]
    
    try:
        is_valid = ApiKeyService.validate_api_key(key)
        return {
            "success": True,
            "data": {
                "key": key[:8] + "...",
                "is_valid": is_valid
            }
        }
    except Exception as e:
        logger.error(f"验证 API Key 异常: {e}")
        return {"success": False, "message": f"服务器错误: {str(e)}"}
