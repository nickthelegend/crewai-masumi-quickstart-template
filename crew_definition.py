import os
import asyncio
from crewai import Agent, Crew, Task
from crewai.llm import LLM
from logging_config import get_logger
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from urllib.parse import urlencode

os.environ["OPENROUTER_API_KEY"] = "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"
os.environ["SMITHERY_API_KEY"] = "e85cb0c5-9f65-4a00-9be8-87c5b641cc6c"

deepseek_llm = LLM(
    model="deepseek/deepseek-chat-v3.1:free",
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
    temperature=0.7,
)

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
                    # Extract URL from the JSON response
                    import json
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
                    import json
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

def mint_nft(url: str, token_name: str = None) -> str:
    """Synchronous wrapper for async NFT minting"""
    return asyncio.run(mint_nft_async(url, token_name))

class ResumeCrew:
    def __init__(self, verbose=True, logger=None):
        self.verbose = verbose
        self.logger = logger or get_logger(__name__)
        self.crew = self.create_crew()
        self.logger.info("ResumeCrew initialized")

    def create_crew(self):
        self.logger.info("Creating resume generation crew with agents")
        
        resume_generator = Agent(
            role='Resume Generator',
            goal='Create professional HTML resume pages from user information',
            backstory='Expert at crafting beautiful, professional resumes in HTML format with modern styling',
            verbose=self.verbose,
            llm=deepseek_llm
        )

        pdf_converter = Agent(
            role='PDF Converter',
            goal='Convert HTML resumes to PDF format using Smithery MCP server',
            backstory='Expert in document conversion using the Smithery MCP server. Converts HTML content to PDF files and returns download URLs from Google Cloud Storage.',
            verbose=self.verbose,
            llm=deepseek_llm
        )

        nft_minter = Agent(
            role='NFT Minter',
            goal='Mint NFTs from PDF URLs using Smithery MCP server',
            backstory='Blockchain specialist who creates NFTs from digital documents. Uses the mint_nft function to create Cardano NFTs with PDF metadata.',
            verbose=self.verbose,
            llm=deepseek_llm
        )

        self.logger.info("Created resume generator, PDF converter, and NFT minter agents")

        crew = Crew(
            agents=[resume_generator, pdf_converter, nft_minter],
            tasks=[
                Task(
                    description='Generate a professional HTML resume using the provided information: {text}. Create a complete HTML page with modern CSS styling, proper structure, and professional formatting.',
                    expected_output='Complete HTML resume page with embedded CSS styling',
                    agent=resume_generator
                ),
                Task(
                    description='Convert the HTML resume from the previous task to PDF format using the Smithery MCP server. Call the call_mcp_server function with the HTML content and return the PDF download URL.',
                    expected_output='PDF download URL from Google Cloud Storage',
                    agent=pdf_converter
                ),
                Task(
                    description='Mint an NFT from the PDF URL generated in the previous task. Use the mint_nft function with the PDF URL and create a unique token name based on the resume.',
                    expected_output='NFT transaction ID and policy ID from Cardano blockchain',
                    agent=nft_minter
                )
            ]
        )
        self.logger.info("Resume crew setup completed")
        return crew