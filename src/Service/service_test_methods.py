"""
Service Test Methods - 服务测试方法
用于测试 API Key 和 LLM 服务功能

注意：Method 装饰器和 library 已通过 DLC embed 插件全局可用
"""

# Method 装饰器已全局可用，无需 import


@Method()
def test_api_key_service():
    """测试 API Key 服务功能"""
    # 使用全局 library 变量，无需 import
    api_key_service = library.resource_dependencies["ApiKeyService"]
    
    print("\n=== 测试 API Key 服务 ===")
    key1 = api_key_service.add_api_key(name="测试Key1", description="第一个测试密钥")
    print(f"创建 API Key: {key1.key[:12]}...")
    
    key2 = api_key_service.add_api_key(name="测试Key2", description="第二个测试密钥")
    print(f"创建 API Key: {key2.key[:12]}...")
    
    available_key = api_key_service.get_available_api_key()
    print(f"获取可用 API Key: {available_key[:12] if available_key else 'None'}...")
    
    is_valid = api_key_service.validate_api_key(key1.key)
    print(f"验证 API Key 有效性: {is_valid}")
    
    all_keys = api_key_service.list_all_api_keys()
    print(f"当前活跃 API Key 数量: {len(all_keys)}")
    
    api_key_service.remove_api_key(key1.key)
    print(f"删除 API Key: {key1.key[:12]}...")
    
    remaining_keys = api_key_service.list_all_api_keys()
    print(f"删除后活跃 API Key 数量: {len(remaining_keys)}")
    print("=== API Key 服务测试完成 ===\n")


@Method()
def test_llm_service():
    """测试 LLM 服务功能"""
    # 使用全局 library 变量，无需 import
    llm_service = library.resource_dependencies["LLMService"]
    api_key_service = library.resource_dependencies["ApiKeyService"]
    
    print("\n=== 测试 LLM 服务 ===")
    
    api_key_service.add_api_key(name="LLM Key 1", description="用于 LLM 调用")
    api_key_service.add_api_key(name="LLM Key 2", description="备用密钥")
    
    messages = [{"role": "user", "content": "你好，请介绍一下自己"}]
    
    try:
        response = llm_service.call_llm_with_retry(messages)
        print(f"LLM 响应: {response['choices'][0]['message']['content']}")
    except Exception as e:
        print(f"调用失败: {e}")
    
    print("=== LLM 服务测试完成 ===\n")
