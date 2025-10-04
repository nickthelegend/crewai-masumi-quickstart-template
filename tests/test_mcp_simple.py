#!/usr/bin/env python3
"""
Simple test for MCP server connection without CrewAI dependencies
"""

import os
import requests
import json

# Set API key
os.environ["SMITHERY_API_KEY"] = "e85cb0c5-9f65-4a00-9be8-87c5b641cc6c"

def test_mcp_server():
    """Test the MCP server directly"""
    
    # Sample HTML content
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>John Smith - Resume</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .header { text-align: center; margin-bottom: 30px; }
            .section { margin-bottom: 20px; }
            .section h2 { color: #333; border-bottom: 2px solid #333; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>John Smith</h1>
            <p>john.smith@email.com | (555) 123-4567 | New York, NY</p>
        </div>
        
        <div class="section">
            <h2>Professional Summary</h2>
            <p>Experienced software engineer with 5+ years developing web applications using Python, JavaScript, and React.</p>
        </div>
        
        <div class="section">
            <h2>Work Experience</h2>
            <h3>Senior Software Engineer at TechCorp (2021-2024)</h3>
            <ul>
                <li>Led development of microservices architecture</li>
                <li>Improved system performance by 40%</li>
                <li>Mentored junior developers</li>
            </ul>
        </div>
        
        <div class="section">
            <h2>Skills</h2>
            <p>Python, JavaScript, React, Node.js, Docker, AWS, PostgreSQL, Git</p>
        </div>
    </body>
    </html>
    """
    
    print("Testing MCP server connection...")
    
    try:
        # Try different authentication methods
        auth_methods = [
            {"Authorization": f"Bearer {os.environ['SMITHERY_API_KEY']}"},
            {"X-API-Key": os.environ['SMITHERY_API_KEY']},
            {"smithery-api-key": os.environ['SMITHERY_API_KEY']}
        ]
        
        for i, auth_header in enumerate(auth_methods):
            print(f"Trying authentication method {i+1}: {list(auth_header.keys())[0]}")
            
            headers = {"Content-Type": "application/json"}
            headers.update(auth_header)
            
            response = requests.post(
                "https://server.smithery.ai/@nickthelegend/test-mcp/mcp",
                headers=headers,
                json={
                    "method": "html_to_pdf",
                    "params": {
                        "html": html_content,
                        "filename": "test_resume.pdf"
                    }
                },
                timeout=30
            )
            
            if response.status_code != 401:
                break
            else:
                print(f"Auth method {i+1} failed with 401")
        
        print(f"Final Response Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Success! PDF URL: {result.get('url', 'No URL returned')}")
            print(f"Full Response: {json.dumps(result, indent=2)}")
        else:
            print(f"Error: {response.status_code}")
            print(f"Response Text: {response.text}")
            
    except Exception as e:
        print(f"Exception occurred: {str(e)}")

if __name__ == "__main__":
    test_mcp_server()