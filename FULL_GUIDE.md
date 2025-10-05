# Resume Generation Service with NFT Minting - Complete Guide

This guide walks you through setting up and running a professional Resume Generation Service that creates HTML resumes, converts them to PDF, and mints them as NFTs on the Cardano blockchain using the Masumi payment network.

## 🎯 What This Service Does

1. **Accepts Resume Information**: Users provide their resume details via API
2. **Generates Professional HTML Resume**: Creates a styled HTML resume from the input
3. **Converts to PDF**: Uses Smithery AI MCP server to convert HTML to PDF
4. **Uploads to IPFS**: Stores metadata on Pinata IPFS for decentralized storage
5. **Mints NFT**: Creates a Cardano NFT representing the resume using Smithery AI
6. **Handles Payments**: Integrates with Masumi network for decentralized payments

## 📋 Prerequisites

- Python >= 3.10 and < 3.13
- uv (Python package manager)
- Smithery AI API key
- Pinata IPFS account
- Masumi Payment Service setup

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/masumi-network/crewai-masumi-quickstart-template.git
cd crewai-masumi-quickstart-template
```

### 2. Install Dependencies

```bash
uv venv --python 3.13
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

### 3. Configure Environment

Copy `.env.example` to `.env` and configure:

```ini
# Payment Service
PAYMENT_SERVICE_URL=http://localhost:3001/api/v1
PAYMENT_API_KEY=your_payment_key

# Agent Configuration
AGENT_IDENTIFIER=your_agent_identifier_from_registration
PAYMENT_AMOUNT=10000000
PAYMENT_UNIT=lovelace
SELLER_VKEY=your_selling_wallet_vkey

# Smithery AI Configuration
SMITHERY_API_KEY=your_smithery_api_key
SMITHERY_PROFILE=your_smithery_profile

# Pinata IPFS Configuration
PINATA_JWT=your_pinata_jwt_token

# OpenAI API (optional, for enhanced resume generation)
OPENAI_API_KEY=your_openai_api_key
```

## 🔧 Service Configuration

### Smithery AI Setup

1. Sign up at [Smithery AI](https://smithery.ai)
2. Get your API key and profile name
3. Add them to your `.env` file

### Pinata IPFS Setup

1. Create account at [Pinata](https://pinata.cloud)
2. Generate JWT token in API Keys section
3. Add to `.env` file

### Masumi Payment Service

Follow the [Masumi Installation Guide](https://docs.masumi.network/documentation/get-started/installation) to set up the payment service.

## 🏃‍♂️ Running the Service

### Start the API Server

```bash
python main.py api
```

The service will be available at:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs

### Test Without Payments (Development)

For testing the core functionality without payments:

```python
# Create test_standalone.py
from simple_crew import SimpleResumeCrew
import asyncio

async def test_resume_generation():
    crew = SimpleResumeCrew()
    
    input_data = {
        "text": """
        Name: John Smith
        Email: john.smith@email.com
        Phone: (555) 123-4567
        Location: New York, NY
        
        Professional Summary:
        Experienced software engineer with 5+ years developing scalable web applications.
        
        Work Experience:
        - Senior Software Engineer at TechCorp (2021-2024)
          * Led development of microservices architecture
          * Improved application performance by 40%
          * Mentored junior developers
        
        Education:
        - Bachelor of Science in Computer Science
          University of Technology (2015-2019)
        
        Skills:
        Python, JavaScript, React, Node.js, Docker, AWS, PostgreSQL
        """
    }
    
    result = await crew.run(input_data)
    print("Resume generation completed!")
    print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(test_resume_generation())
```

Run the test:
```bash
python test_standalone.py
```

## 📡 API Endpoints

### 1. Get Input Schema
```bash
GET /input_schema
```
Returns the expected input format for resume generation.

### 2. Check Availability
```bash
GET /availability
```
Checks if the service is operational.

### 3. Start Job (with Payment)
```bash
POST /start_job
Content-Type: application/json

{
    "identifier_from_purchaser": "resume-job-123",
    "input_data": {
        "text": "Name: John Smith\nEmail: john@email.com\n..."
    }
}
```

### 4. Check Job Status
```bash
GET /status?job_id=your_job_id
```

### 5. Health Check
```bash
GET /health
```

## 💳 Payment Integration

### Register Your Agent

1. **Get Payment Source Info**:
```bash
curl -X GET 'http://localhost:3001/api/v1/payment-source/' \
  -H 'accept: application/json' \
  -H 'token: your_api_key'
```

2. **Register Agent**:
```bash
curl -X POST 'http://localhost:3001/api/v1/registry' \
  -H 'Content-Type: application/json' \
  -H 'token: your_api_key' \
  -d '{
    "name": "Resume Generator NFT",
    "description": "Professional resume generation with PDF conversion and NFT minting",
    "url": "http://localhost:8000",
    "amounts": [{"amount": 10000000, "unit": "lovelace"}],
    "walletVkey": "your_wallet_vkey"
  }'
```

3. **Get Agent Identifier**:
```bash
curl -X GET 'http://localhost:3001/api/v1/registry/' \
  -H 'accept: application/json' \
  -H 'token: your_api_key'
```

### Test Payment Flow

1. **Start a Job**:
```bash
curl -X POST "http://localhost:8000/start_job" \
  -H "Content-Type: application/json" \
  -d '{
    "identifier_from_purchaser": "test-resume-001",
    "input_data": {
      "text": "Name: Alice Johnson\nEmail: alice@example.com\nExperience: Software Engineer at XYZ Corp..."
    }
  }'
```

2. **Make Payment** (from buyer's perspective):
```bash
curl -X POST 'http://localhost:3001/api/v1/purchase' \
  -H 'Content-Type: application/json' \
  -H 'token: buyer_api_key' \
  -d '{
    "agent_identifier": "your_agent_identifier"
  }'
```

3. **Check Status**:
```bash
curl -X GET "http://localhost:8000/status?job_id=your_job_id"
```

## 🔍 Understanding the Workflow

### 1. Resume HTML Generation
The service extracts name from input and generates professional HTML:
```python
def generate_resume_html(resume_text: str) -> str:
    # Extracts name and creates styled HTML resume
    # Returns complete HTML document
```

### 2. PDF Conversion via MCP
Uses Smithery AI MCP server to convert HTML to PDF:
```python
async def call_mcp_server(html_content: str) -> str:
    # Connects to Smithery MCP server
    # Converts HTML to PDF
    # Returns base64 encoded PDF
```

### 3. IPFS Metadata Upload
Uploads NFT metadata to Pinata IPFS:
```python
async def upload_to_pinata(name: str, pdf_base64: str) -> str:
    # Creates NFT metadata
    # Uploads to Pinata IPFS
    # Returns IPFS CID
```

### 4. NFT Minting
Mints Cardano NFT using Smithery AI:
```python
async def mint_nft(metadata_cid: str, name: str) -> dict:
    # Mints NFT on Cardano
    # Uses IPFS CID for metadata
    # Returns transaction details
```

## 🛠 Troubleshooting

### Common Issues

1. **MCP Server Connection Failed**
   - Verify Smithery API key and profile
   - Check network connectivity
   - Ensure proper authentication format

2. **IPFS Upload Failed**
   - Verify Pinata JWT token
   - Check file size limits
   - Ensure proper JSON formatting

3. **NFT Minting Failed**
   - Verify metadata CID format
   - Check Smithery AI balance
   - Ensure proper asset name format

4. **Payment Issues**
   - Verify Masumi service is running
   - Check wallet has sufficient funds
   - Ensure proper agent registration

### Debug Mode

Enable detailed logging by adding to your `.env`:
```ini
LOG_LEVEL=DEBUG
```

### Testing Individual Components

Test each component separately:

```python
# Test HTML generation
from simple_crew import generate_resume_html
html = generate_resume_html("Name: Test User\nEmail: test@example.com")
print(html)

# Test MCP server (requires async)
from crew_definition import call_mcp_server
import asyncio
pdf = asyncio.run(call_mcp_server(html))
print(f"PDF generated: {len(pdf)} characters")
```

## 📈 Production Deployment

### Database Integration
Replace in-memory job storage with PostgreSQL:

```python
# Add to requirements.txt
asyncpg==0.29.0
sqlalchemy[asyncio]==2.0.23

# Update job storage in main.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
```

### Message Queue
Add Redis/Celery for background processing:

```python
# Add to requirements.txt
celery==5.3.4
redis==5.0.1
```

### Monitoring
Add health checks and metrics:

```python
@app.get("/metrics")
async def get_metrics():
    return {
        "jobs_completed": len([j for j in jobs.values() if j["status"] == "completed"]),
        "jobs_pending": len([j for j in jobs.values() if j["status"] == "pending"]),
        "uptime": time.time() - start_time
    }
```

## 🔐 Security Considerations

1. **API Key Management**: Store sensitive keys in environment variables
2. **Input Validation**: Validate all user inputs before processing
3. **Rate Limiting**: Implement rate limiting for API endpoints
4. **HTTPS**: Use HTTPS in production
5. **Authentication**: Add proper authentication for admin endpoints

## 📚 Additional Resources

- [Masumi Documentation](https://docs.masumi.network)
- [Smithery AI Documentation](https://smithery.ai/docs)
- [Pinata IPFS Documentation](https://docs.pinata.cloud)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [MCP Protocol](https://modelcontextprotocol.io)

## 🤝 Support

For issues and questions:
- Check the troubleshooting section above
- Review logs for error details
- Test individual components separately
- Verify all environment variables are set correctly

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.