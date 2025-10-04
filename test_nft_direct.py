#!/usr/bin/env python3
"""
Direct test of NFT minting with shorter URL
"""

import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from urllib.parse import urlencode
import json

async def test_nft_minting():
    """Test NFT minting directly"""
    
    # Use a shorter test URL
    test_url = "https://example.com/resume.pdf"
    token_name = "ResumeNFT"
    
    print(f"Testing NFT minting with URL: {test_url}")
    print(f"Token name: {token_name}")
    
    try:
        base_url = "https://server.smithery.ai/@nickthelegend/test-mcp/mcp"
        params = {"api_key": "3afacbc0-9c57-4aa0-a77d-5c1f94e7bf21"}
        mcp_url = f"{base_url}?{urlencode(params)}"
        
        async with streamablehttp_client(mcp_url) as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                result = await session.call_tool(
                    "mint_nft",
                    {
                        "url": test_url,
                        "token_name": token_name
                    }
                )
                
                if result.content and len(result.content) > 0:
                    content = result.content[0].text
                    print(f"NFT minting result: {content}")
                    
                    try:
                        data = json.loads(content)
                        tx_id = data.get('tx_id', 'No transaction ID')
                        policy_id = data.get('policy_id', 'No policy ID')
                        print(f"Success! TX ID: {tx_id}, Policy ID: {policy_id}")
                        return True
                    except json.JSONDecodeError:
                        print(f"Raw result: {content}")
                        return "Error" not in content
                else:
                    print("No content returned from NFT minting")
                    return False
                    
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_nft_minting())
    print(f"\nNFT Test {'PASSED' if success else 'FAILED'}")