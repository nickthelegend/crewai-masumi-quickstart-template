#!/usr/bin/env python3
"""
Debug MCP server authentication
"""

import requests
import json

def test_mcp_auth():
    """Test different authentication approaches"""
    
    api_key = "e85cb0c5-9f65-4a00-9be8-87c5b641cc6c"
    base_url = "https://server.smithery.ai/@nickthelegend/test-mcp"
    
    auth_methods = [
        {"headers": {"Authorization": f"Bearer {api_key}"}, "name": "Bearer token"},
        {"headers": {"X-API-Key": api_key}, "name": "X-API-Key header"},
        {"headers": {"smithery-api-key": api_key}, "name": "smithery-api-key header"},
        {"params": {"api_key": api_key}, "name": "Query parameter"},
        {"params": {"key": api_key}, "name": "Key query parameter"},
    ]
    
    test_payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list"
    }
    
    for i, auth_method in enumerate(auth_methods):
        print(f"\nTest {i+1}: {auth_method['name']}")
        try:
            headers = {"Content-Type": "application/json"}
            params = {}
            
            if "headers" in auth_method:
                headers.update(auth_method["headers"])
            if "params" in auth_method:
                params.update(auth_method["params"])
            
            response = requests.post(
                f"{base_url}/mcp",
                headers=headers,
                params=params,
                json=test_payload,
                timeout=10
            )
            
            print(f"Status: {response.status_code}")
            if response.status_code != 401:
                print(f"SUCCESS! Response: {response.text}")
                return auth_method
            else:
                print(f"401 Error: {response.text}")
                
        except Exception as e:
            print(f"Error: {e}")
    
    print("\nAll authentication methods failed.")
    return None

if __name__ == "__main__":
    working_auth = test_mcp_auth()
    if working_auth:
        print(f"\nWorking authentication method: {working_auth}")
    else:
        print("\nNo working authentication method found. Check API key or contact Smithery support.")