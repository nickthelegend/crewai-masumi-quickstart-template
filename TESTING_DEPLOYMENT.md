# Testing Deployment - Resume NFT Generator

This guide provides step-by-step testing instructions for the deployed Resume NFT Generator service.

## 🌐 Deployed Service

**Base URL**: `https://crewai-masumi-quickstart-template.onrender.com`

**Interactive API Docs**: https://crewai-masumi-quickstart-template.onrender.com/docs

## 🧪 Testing Endpoints

### 1. Check Service Availability

**Test if the service is operational:**

```bash
curl -X GET "https://crewai-masumi-quickstart-template.onrender.com/availability"
```

**Expected Response:**
```json
{
  "status": "available",
  "type": "masumi-agent",
  "message": "Resume Generation Service is ready to create professional resumes, convert to PDF, and mint NFTs."
}
```

### 2. Get Input Schema

**Check what input format is required:**

```bash
curl -X GET "https://crewai-masumi-quickstart-template.onrender.com/input_schema"
```

**Expected Response:**
```json
{
  "input_data": [
    {
      "id": "text",
      "type": "textarea",
      "name": "Resume Information",
      "data": {
        "description": "Provide your resume information...",
        "placeholder": "Name: John Smith..."
      },
      "validations": [
        {"validation": "min", "value": "50"},
        {"validation": "max", "value": "5000"},
        {"validation": "format", "value": "nonempty"}
      ]
    }
  ]
}
```

### 3. Health Check

**Verify service health:**

```bash
curl -X GET "https://crewai-masumi-quickstart-template.onrender.com/health"
```

**Expected Response:**
```json
{
  "status": "healthy"
}
```

### 4. Start Resume Generation Job

**Submit a resume for processing:**

```bash
curl -X POST "https://crewai-masumi-quickstart-template.onrender.com/start_job" \
-H "Content-Type: application/json" \
-d '{
    "identifier_from_purchaser": "test_resume_001",
    "input_data": {
        "text": "Name: Sarah Chen\nEmail: sarah.chen@email.com\nPhone: (555) 987-6543\nLocation: Seattle, WA\n\nProfessional Summary:\nSenior Full Stack Developer with 6+ years of experience building scalable web applications and leading development teams. Expertise in React, Node.js, Python, and cloud technologies.\n\nWork Experience:\n- Senior Full Stack Developer at Microsoft (2020-2024)\n  * Led development of customer-facing web applications serving 10M+ users\n  * Architected microservices using Node.js and Azure\n  * Improved application performance by 45% through optimization\n  * Mentored 8 junior developers and conducted code reviews\n\n- Software Engineer at Amazon (2018-2020)\n  * Developed e-commerce features using React and Java\n  * Implemented automated testing reducing bugs by 30%\n  * Collaborated with cross-functional teams on product launches\n\nEducation:\n- Master of Science in Computer Science\n  University of Washington (2016-2018)\n- Bachelor of Science in Software Engineering\n  UC Berkeley (2012-2016)\n\nSkills:\nJavaScript, TypeScript, React, Node.js, Python, Java, AWS, Azure, Docker, Kubernetes, PostgreSQL, MongoDB, Git, Agile/Scrum"
    }
}'
```

**Expected Response:**
```json
{
  "status": "success",
  "job_id": "12345678-1234-1234-1234-123456789abc",
  "blockchainIdentifier": "blockchain_id_here",
  "submitResultTime": 1234567890,
  "unlockTime": 1234567890,
  "externalDisputeUnlockTime": 1234567890,
  "agentIdentifier": "your_agent_identifier",
  "sellerVkey": "your_seller_vkey",
  "identifierFromPurchaser": "test_resume_001",
  "amounts": [{"amount": "10000000", "unit": "lovelace"}],
  "input_hash": "hash_here",
  "payByTime": 1234567890
}
```

**Save the `job_id` from the response for the next step.**

### 5. Check Job Status

**Monitor job progress (replace `YOUR_JOB_ID` with actual job ID):**

```bash
curl -X GET "https://crewai-masumi-quickstart-template.onrender.com/status?job_id=YOUR_JOB_ID"
```

**Possible Responses:**

**Awaiting Payment:**
```json
{
  "job_id": "YOUR_JOB_ID",
  "status": "awaiting_payment",
  "payment_status": "pending",
  "result": null
}
```

**Processing:**
```json
{
  "job_id": "YOUR_JOB_ID",
  "status": "running",
  "payment_status": "completed",
  "result": null
}
```

**Completed:**
```json
{
  "job_id": "YOUR_JOB_ID",
  "status": "completed",
  "payment_status": "completed",
  "result": {
    "html_length": 2500,
    "pdf_result": "PDF generated successfully: https://...",
    "ipfs_cid": "QmXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "nft_result": {
      "transaction_id": "tx_hash_here",
      "asset_name": "Sarah_Ch_NFT",
      "policy_id": "policy_id_here"
    },
    "status": "completed"
  }
}
```

## 🔄 Complete Testing Workflow

### Step-by-Step Test Process

1. **Check Service Status**
   ```bash
   curl -X GET "https://crewai-masumi-quickstart-template.onrender.com/availability"
   ```

2. **Start a Job**
   ```bash
   curl -X POST "https://crewai-masumi-quickstart-template.onrender.com/start_job" \
   -H "Content-Type: application/json" \
   -d '{
       "identifier_from_purchaser": "my_test_resume",
       "input_data": {
           "text": "Name: John Doe\nEmail: john.doe@email.com\nPhone: (555) 123-4567\n\nProfessional Summary:\nExperienced software developer with 5+ years in web development.\n\nWork Experience:\n- Software Developer at TechCorp (2019-2024)\n  * Built responsive web applications\n  * Worked with React and Node.js\n\nEducation:\n- BS Computer Science, State University (2015-2019)\n\nSkills:\nJavaScript, React, Node.js, Python, SQL"
       }
   }'
   ```

3. **Monitor Job Status** (repeat until completed)
   ```bash
   curl -X GET "https://crewai-masumi-quickstart-template.onrender.com/status?job_id=YOUR_JOB_ID"
   ```

## 🧪 Test Cases

### Test Case 1: Minimal Resume
```json
{
  "identifier_from_purchaser": "minimal_test",
  "input_data": {
    "text": "Name: Test User\nEmail: test@example.com\nExperience: Software Developer\nSkills: Python, JavaScript"
  }
}
```

### Test Case 2: Comprehensive Resume
```json
{
  "identifier_from_purchaser": "comprehensive_test",
  "input_data": {
    "text": "Name: Jane Smith\nEmail: jane.smith@email.com\nPhone: (555) 456-7890\nLocation: New York, NY\n\nProfessional Summary:\nSenior Product Manager with 8+ years of experience leading cross-functional teams and launching successful products.\n\nWork Experience:\n- Senior Product Manager at Google (2020-2024)\n  * Led product strategy for consumer applications\n  * Managed team of 12 engineers and designers\n  * Launched 3 major features with 50M+ users\n\n- Product Manager at Facebook (2018-2020)\n  * Developed mobile app features\n  * Conducted user research and A/B testing\n\nEducation:\n- MBA, Stanford Graduate School of Business (2016-2018)\n- BS Engineering, MIT (2012-2016)\n\nSkills:\nProduct Strategy, User Research, Data Analysis, Agile, SQL, Python, Figma"
  }
}
```

### Test Case 3: Invalid Input (Too Short)
```json
{
  "identifier_from_purchaser": "invalid_test",
  "input_data": {
    "text": "Short text"
  }
}
```

## 📊 Expected Results

### Successful Job Flow:
1. `awaiting_payment` → Payment required
2. `running` → Processing resume (HTML → PDF → IPFS → NFT)
3. `completed` → Resume NFT created successfully

### Result Components:
- **HTML Resume**: Professional styled HTML document
- **PDF Conversion**: High-quality PDF via Smithery AI MCP server
- **IPFS Storage**: Metadata uploaded to Pinata IPFS
- **NFT Minting**: Cardano NFT created via Smithery AI MCP server

## 🚨 Troubleshooting

### Common Issues:

**Service Unavailable (503)**
- Service may be starting up (Render cold start)
- Wait 30-60 seconds and retry

**Job Status "failed"**
- Check input text meets minimum requirements (50+ characters)
- Ensure proper name format in resume text
- Verify all required services (Smithery AI, Pinata) are accessible

**Payment Issues**
- Job will remain in "awaiting_payment" status
- Payment must be made through Masumi network
- Contact Masumi support for payment-related issues

## 🔗 Additional Resources

- **API Documentation**: https://crewai-masumi-quickstart-template.onrender.com/docs
- **Masumi Network**: https://explorer.masumi.network/agents/721
- **Agent ID**: `7e8bdaf2b2b919a3a4b94002cafb50086c0c845fe535d07a77ab7f776b875de2ac4dfd3d0df7c38be2a97be0f33c0f71e34f67b67e8e7e75c3f203c6`