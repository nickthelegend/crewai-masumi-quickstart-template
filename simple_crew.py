#!/usr/bin/env python3
"""
Simplified crew implementation without CrewAI dependencies
"""

import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from urllib.parse import urlencode
import json
import requests

async def call_mcp_server_async(html_content: str, filename: str = "resume.pdf") -> str:
    """Convert HTML content to PDF using Smithery AI MCP server"""
    try:
        base_url = "https://server.smithery.ai/@nickthelegend/test-mcp/mcp"
        params = {"api_key": "3afacbc0-9c57-4aa0-a77d-5c1f94e7bf21"}
        url = f"{base_url}?{urlencode(params)}"
        
        async with streamablehttp_client(url) as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                result = await session.call_tool(
                    "html_to_pdf",
                    {
                        "html": html_content,
                        "filename": filename
                    }
                )
                
                if result.content and len(result.content) > 0:
                    content = result.content[0].text
                    try:
                        data = json.loads(content)
                        pdf_url = data.get('url', 'No URL found')
                        return f"PDF generated successfully: {pdf_url}"
                    except json.JSONDecodeError:
                        return f"PDF generated: {content}"
                else:
                    return "PDF generation completed but no content returned"
                    
    except Exception as e:
        return f"Error calling MCP server: {str(e)}"

def call_mcp_server(html_content: str, filename: str = "resume.pdf") -> str:
    """Synchronous wrapper for async MCP call"""
    return asyncio.run(call_mcp_server_async(html_content, filename))

async def mint_nft_async(url: str, token_name: str = None) -> str:
    """Mint NFT using Smithery AI MCP server"""
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
                        "url": url,
                        "token_name": token_name
                    }
                )
                
                if result.content and len(result.content) > 0:
                    content = result.content[0].text
                    try:
                        data = json.loads(content)
                        tx_id = data.get('tx_id', 'No transaction ID')
                        policy_id = data.get('policy_id', 'No policy ID')
                        return f"NFT minted successfully: TX ID {tx_id}, Policy ID {policy_id}"
                    except json.JSONDecodeError:
                        return f"NFT minted: {content}"
                else:
                    return "NFT minting completed but no content returned"
                    
    except Exception as e:
        return f"Error minting NFT: {str(e)}"

def upload_to_pinata(pdf_url: str, token_name: str) -> str:
    """Upload metadata to Pinata IPFS and return IPFS URL"""
    try:
        # Pinata credentials
        jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiI2NmUzZTMwZi1kMTUxLTQ5YmItOTMxOC1hZDlkMDRhOWQ2OGQiLCJlbWFpbCI6InRlc3Rpbmd0ZXNsYTdAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInBpbl9wb2xpY3kiOnsicmVnaW9ucyI6W3siZGVzaXJlZFJlcGxpY2F0aW9uQ291bnQiOjEsImlkIjoiRlJBMSJ9LHsiZGVzaXJlZFJlcGxpY2F0aW9uQ291bnQiOjEsImlkIjoiTllDMSJ9XSwidmVyc2lvbiI6MX0sIm1mYV9lbmFibGVkIjpmYWxzZSwic3RhdHVzIjoiQUNUSVZFIn0sImF1dGhlbnRpY2F0aW9uVHlwZSI6InNjb3BlZEtleSIsInNjb3BlZEtleUtleSI6IjQxOTQ3ZDEzZWI0OTFhM2Y3ZTk1Iiwic2NvcGVkS2V5U2VjcmV0IjoiNDdmOTA5YjJhYWNkMjgyMDAyZTRhZTg4ZDM1MzRkZjQwOTU2OTkxNGIyMGM3N2RiNGE4Y2M5MDI4MWMyNzA1YSIsImV4cCI6MTc5MTEwNTEzOX0.ZyVq3-5-Ig7X52xE1Mbo61sAPWzz2Ae01AWp4A29s0g"
        
        # Create metadata JSON
        metadata = {
            "name": token_name,
            "description": f"Resume NFT for {token_name}",
            "image": pdf_url,
            "external_url": pdf_url,
            "attributes": [
                {"trait_type": "Document Type", "value": "Resume"},
                {"trait_type": "Format", "value": "PDF"}
            ]
        }
        
        # Upload to Pinata
        response = requests.post(
            "https://api.pinata.cloud/pinning/pinJSONToIPFS",
            headers={
                "Authorization": f"Bearer {jwt_token}",
                "Content-Type": "application/json"
            },
            json={
                "pinataContent": metadata,
                "pinataMetadata": {
                    "name": f"{token_name}_metadata.json"
                }
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            ipfs_hash = result.get('IpfsHash')
            # Use ipfs:// format now that validation is removed
            ipfs_url = f"ipfs://{ipfs_hash}"
            return ipfs_url
        else:
            return f"Error uploading to Pinata: {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"Error uploading to Pinata: {str(e)}"

def mint_nft(url: str, token_name: str = None) -> str:
    """Synchronous wrapper for async NFT minting with IPFS upload"""
    # First upload metadata to IPFS to get shorter URL
    ipfs_url = upload_to_pinata(url, token_name or "Resume")
    
    if "Error" in ipfs_url:
        return ipfs_url
    
    # Use IPFS URL for NFT minting (much shorter)
    return asyncio.run(mint_nft_async(ipfs_url, token_name))

def generate_resume_html(resume_text: str) -> str:
    """Generate professional HTML resume"""
    
    # Extract basic info (simplified parsing)
    lines = resume_text.strip().split('\n')
    name = "Professional Resume"
    email = ""
    phone = ""
    location = ""
    
    for line in lines:
        line = line.strip()
        if line.startswith("Name:"):
            name = line.replace("Name:", "").strip()
        elif line.startswith("Email:"):
            email = line.replace("Email:", "").strip()
        elif line.startswith("Phone:"):
            phone = line.replace("Phone:", "").strip()
        elif line.startswith("Location:"):
            location = line.replace("Location:", "").strip()
    
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{name} - Resume</title>
        <style>
            body {{ 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                margin: 40px; 
                line-height: 1.6;
                color: #333;
                max-width: 800px;
            }}
            .header {{ 
                text-align: center; 
                margin-bottom: 30px; 
                border-bottom: 3px solid #2c3e50;
                padding-bottom: 20px;
            }}
            .header h1 {{ 
                color: #2c3e50; 
                margin-bottom: 10px;
                font-size: 2.5em;
                margin-top: 0;
            }}
            .contact-info {{ 
                color: #7f8c8d; 
                font-size: 1.1em;
            }}
            .section {{ 
                margin-bottom: 25px; 
            }}
            .section h2 {{ 
                color: #2c3e50; 
                border-bottom: 2px solid #3498db; 
                padding-bottom: 5px;
                font-size: 1.4em;
            }}
            .content {{
                white-space: pre-line;
                margin-left: 20px;
            }}
            .skills {{ 
                background-color: #ecf0f1; 
                padding: 15px; 
                border-radius: 5px;
                margin-top: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>{name}</h1>
            <div class="contact-info">
                {email} | {phone} | {location}
            </div>
        </div>
        
        <div class="section">
            <h2>Resume Content</h2>
            <div class="content">{resume_text}</div>
        </div>
    </body>
    </html>
    """
    
    return html_template

class SimpleResumeCrew:
    """Simplified resume crew without CrewAI dependencies"""
    
    def __init__(self):
        print("SimpleResumeCrew initialized")
    
    def process_resume(self, resume_data: dict) -> str:
        """Process resume data, generate PDF, and mint NFT"""
        
        resume_text = resume_data.get("text", "")
        
        # Extract name for token name
        name = "Resume"
        for line in resume_text.split('\n'):
            if line.strip().startswith("Name:"):
                name = line.replace("Name:", "").strip().replace(" ", "_")
                break
        
        print("Step 1: Generating HTML resume...")
        html_content = generate_resume_html(resume_text)
        print(f"HTML generated ({len(html_content)} characters)")
        
        print("Step 2: Converting to PDF via MCP server...")
        pdf_result = call_mcp_server(html_content, "resume.pdf")
        print(f"PDF result: {pdf_result}")
        
        # Extract PDF URL from result
        pdf_url = None
        if "https://" in pdf_result:
            pdf_url = pdf_result.split("https://")[1].split()[0]
            pdf_url = "https://" + pdf_url
        
        if pdf_url:
            print("Step 3: Uploading metadata to IPFS...")
            short_token_name = f"{name[:8]}_NFT"
            print(f"Step 4: Minting NFT from IPFS metadata...")
            nft_result = mint_nft(pdf_url, short_token_name)
            print(f"NFT result: {nft_result}")
            
            return f"Resume processing completed. HTML: {len(html_content)} chars, PDF: {pdf_result}, NFT: {nft_result}"
        else:
            return f"Resume processing completed. HTML: {len(html_content)} chars, PDF: {pdf_result}, NFT: Skipped (no PDF URL)"

def test_simple_crew():
    """Test the simplified crew"""
    
    resume_data = {
        "text": """
        Name: Alex Chen
        Email: alex.chen@email.com
        Phone: (555) 234-5678
        Location: Seattle, WA
        
        Professional Summary:
        Senior DevOps Engineer with 6+ years of experience in cloud infrastructure and automation.
        
        Work Experience:
        - Senior DevOps Engineer at CloudTech (2021-2024)
          * Managed AWS infrastructure for 100+ microservices
          * Reduced deployment time by 75% with automated CI/CD
          * Led migration to Kubernetes saving $200K annually
        
        - DevOps Engineer at StartupCorp (2018-2021)
          * Built infrastructure automation using Terraform
          * Implemented monitoring and alerting systems
          * Maintained 99.9% uptime for production systems
        
        Education:
        - Bachelor of Science in Computer Engineering
          University of Washington (2014-2018)
        
        Skills:
        AWS, Docker, Kubernetes, Terraform, Jenkins, Python, Bash, Monitoring
        """
    }
    
    print("Testing SimpleResumeCrew with NFT minting...")
    
    try:
        crew = SimpleResumeCrew()
        result = crew.process_resume(resume_data)
        print(f"Final result: {result}")
        return True
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_simple_crew()
    print(f"\nTest {'PASSED' if success else 'FAILED'}")