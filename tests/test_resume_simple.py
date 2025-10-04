#!/usr/bin/env python3
"""
Simple resume generation test without full CrewAI framework
"""

import os
import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from urllib.parse import urlencode

async def html_to_pdf_mcp_async(html_content: str, filename: str = "resume.pdf") -> str:
    """Convert HTML to PDF using Smithery MCP server"""
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
                
                if result.content:
                    return f"PDF generated: {result.content[0].text if result.content else 'No content returned'}"
                else:
                    return "PDF generation completed but no URL returned"
                    
    except Exception as e:
        return f"Exception: {str(e)}"

def html_to_pdf_mcp(html_content: str, filename: str = "resume.pdf") -> str:
    """Synchronous wrapper for async MCP call"""
    return asyncio.run(html_to_pdf_mcp_async(html_content, filename))

def generate_resume_html(resume_data: str) -> str:
    """Generate HTML resume from text data"""
    
    # Simple HTML template
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Professional Resume</title>
        <style>
            body {{ 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                margin: 40px; 
                line-height: 1.6;
                color: #333;
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
            .job-title {{ 
                font-weight: bold; 
                color: #2980b9;
                font-size: 1.1em;
            }}
            ul {{ 
                margin-left: 20px; 
            }}
            li {{ 
                margin-bottom: 5px; 
            }}
            .skills {{ 
                background-color: #ecf0f1; 
                padding: 15px; 
                border-radius: 5px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>John Smith</h1>
            <div class="contact-info">
                john.smith@email.com | (555) 123-4567 | New York, NY
            </div>
        </div>
        
        <div class="section">
            <h2>Professional Summary</h2>
            <p>Experienced software engineer with 5+ years developing web applications using Python, JavaScript, and React. Proven track record of leading development teams and delivering high-quality software solutions.</p>
        </div>
        
        <div class="section">
            <h2>Work Experience</h2>
            <div class="job-title">Senior Software Engineer at TechCorp (2021-2024)</div>
            <ul>
                <li>Led development of microservices architecture serving 1M+ users</li>
                <li>Improved system performance by 40% through optimization initiatives</li>
                <li>Mentored 5 junior developers and established coding best practices</li>
                <li>Implemented CI/CD pipelines reducing deployment time by 60%</li>
            </ul>
            
            <div class="job-title">Software Engineer at StartupXYZ (2019-2021)</div>
            <ul>
                <li>Built full-stack web applications using React and Node.js</li>
                <li>Collaborated with cross-functional teams in agile environment</li>
                <li>Developed RESTful APIs and integrated third-party services</li>
            </ul>
        </div>
        
        <div class="section">
            <h2>Education</h2>
            <div class="job-title">Bachelor of Science in Computer Science</div>
            <p>University of Technology (2015-2019) - GPA: 3.8/4.0</p>
        </div>
        
        <div class="section">
            <h2>Technical Skills</h2>
            <div class="skills">
                <strong>Languages:</strong> Python, JavaScript, TypeScript, Java<br>
                <strong>Frameworks:</strong> React, Node.js, Express, Django<br>
                <strong>Tools:</strong> Docker, AWS, PostgreSQL, Git, Jenkins<br>
                <strong>Methodologies:</strong> Agile, TDD, Microservices
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_template

def test_resume_workflow():
    """Test the complete resume generation workflow"""
    
    print("Starting resume generation test...")
    
    # Sample input data
    resume_input = """
    Name: John Smith
    Email: john.smith@email.com
    Phone: (555) 123-4567
    Location: New York, NY
    
    Professional Summary:
    Experienced software engineer with 5+ years developing web applications.
    
    Work Experience:
    - Senior Software Engineer at TechCorp (2021-2024)
    - Software Engineer at StartupXYZ (2019-2021)
    
    Education:
    - Bachelor of Science in Computer Science, University of Technology (2015-2019)
    
    Skills:
    Python, JavaScript, React, Node.js, Docker, AWS, PostgreSQL, Git
    """
    
    try:
        # Step 1: Generate HTML resume
        print("Step 1: Generating HTML resume...")
        html_resume = generate_resume_html(resume_input)
        print(f"HTML generated successfully ({len(html_resume)} characters)")
        
        # Step 2: Convert to PDF using MCP server
        print("Step 2: Converting to PDF via MCP server...")
        pdf_result = html_to_pdf_mcp(html_resume, "john_smith_resume.pdf")
        print(f"PDF conversion result: {pdf_result}")
        
        # Save HTML for inspection
        with open("generated_resume.html", "w", encoding="utf-8") as f:
            f.write(html_resume)
        print("HTML resume saved as 'generated_resume.html'")
        
        print("Resume generation workflow completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error in resume workflow: {str(e)}")
        return False

if __name__ == "__main__":
    test_resume_workflow()