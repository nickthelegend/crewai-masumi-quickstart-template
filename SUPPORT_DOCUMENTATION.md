# Support Documentation - Resume NFT Generator

## 🆘 Getting Help

### Quick Support Channels
- **Technical Issues**: Check troubleshooting section below
- **Payment Problems**: Contact Masumi Network support
- **Service Status**: Check `/availability` endpoint
- **API Documentation**: Visit `/docs` endpoint

## 📋 Frequently Asked Questions

### General Service Questions

**Q: What does the Resume NFT Generator do?**
A: Creates professional HTML resumes, converts them to PDF, and mints them as NFTs on Cardano blockchain with IPFS metadata storage.

**Q: How long does the process take?**
A: Typically 2-5 minutes after payment confirmation, depending on network conditions.

**Q: What information do I need to provide?**
A: Resume details including name, contact info, work experience, education, and skills in text format.

**Q: Can I update my resume after minting?**
A: No, NFTs are immutable. You would need to create a new resume NFT.

### Payment Questions

**Q: What payment methods are accepted?**
A: ADA (Cardano) payments through the Masumi decentralized network.

**Q: How much does it cost?**
A: 10 ADA (10,000,000 lovelace) per resume generation and NFT minting.

**Q: Are payments refundable?**
A: No, payments are final once processing begins due to blockchain immutability.

**Q: What if payment fails?**
A: Check your wallet balance and try again. Contact Masumi support for persistent issues.

### Technical Questions

**Q: Which blockchain network is used?**
A: Cardano (Preprod for testing, Mainnet for production).

**Q: Where is my resume stored?**
A: Metadata is stored on IPFS (Pinata), NFT is on Cardano blockchain.

**Q: Can I access my resume later?**
A: Yes, through your Cardano wallet or IPFS using the provided CID.

## 🔧 Troubleshooting Guide

### Common Issues and Solutions

#### 1. Job Status Shows "Failed"
**Symptoms**: Status endpoint returns "failed" status
**Solutions**:
- Check if payment was completed successfully
- Verify resume text meets minimum requirements (50+ characters)
- Ensure text contains valid name and contact information
- Try submitting again with properly formatted content

#### 2. Payment Not Processing
**Symptoms**: Job stuck in "awaiting_payment" status
**Solutions**:
- Verify sufficient ADA balance in wallet
- Check Cardano network status
- Confirm payment was sent to correct address
- Wait up to 10 minutes for blockchain confirmation

#### 3. NFT Minting Failed
**Symptoms**: PDF generated but NFT creation failed
**Solutions**:
- Check Smithery AI service status
- Verify IPFS metadata was uploaded successfully
- Ensure Cardano network is operational
- Contact support if issue persists

#### 4. Service Unavailable
**Symptoms**: Cannot connect to service endpoints
**Solutions**:
- Check service status at `/availability` endpoint
- Verify correct API URL
- Check internet connection
- Try again in a few minutes

### Error Codes

| Code | Description | Solution |
|------|-------------|----------|
| 400 | Bad Request | Check input format and required fields |
| 404 | Job Not Found | Verify job ID is correct |
| 500 | Internal Error | Service issue, try again later |
| 503 | Service Unavailable | Temporary outage, check back soon |

## 🛠 API Usage Guide

### Basic Workflow

1. **Check Service Status**
```bash
GET /availability
```

2. **Get Input Requirements**
```bash
GET /input_schema
```

3. **Start Resume Generation**
```bash
POST /start_job
{
  "identifier_from_purchaser": "my-resume-001",
  "input_data": {
    "text": "Name: John Smith\nEmail: john@example.com\n..."
  }
}
```

4. **Make Payment** (via Masumi network)

5. **Check Status**
```bash
GET /status?job_id=your_job_id
```

### Input Format Guidelines

**Required Information**:
- Full name
- Contact information (email, phone)
- Professional experience
- Education background
- Skills and qualifications

**Format Example**:
```
Name: Jane Doe
Email: jane.doe@email.com
Phone: (555) 123-4567
Location: San Francisco, CA

Professional Summary:
Experienced software engineer with 5+ years...

Work Experience:
- Senior Developer at TechCorp (2021-2024)
  * Led team of 5 developers
  * Improved system performance by 40%

Education:
- BS Computer Science, Stanford University (2017)

Skills:
Python, JavaScript, React, AWS, Docker
```

## 🔍 Monitoring and Status

### Health Checks

**Service Health**: `GET /health`
- Returns service operational status
- Check before submitting jobs

**Availability**: `GET /availability`
- Confirms service is accepting new jobs
- Shows current service capabilities

### Job Tracking

**Status Monitoring**: `GET /status?job_id=<id>`
- Track job progress in real-time
- Monitor payment and processing status
- Get results when completed

**Status Values**:
- `awaiting_payment`: Waiting for payment confirmation
- `running`: Processing resume and generating NFT
- `completed`: Successfully finished with results
- `failed`: Error occurred during processing

## 📞 Contact and Support

### Self-Service Resources

1. **API Documentation**: Visit `/docs` for interactive API explorer
2. **Service Status**: Check `/availability` for current operational status
3. **This Guide**: Comprehensive troubleshooting and usage information

### External Support

1. **Masumi Network**: For payment and blockchain issues
   - Documentation: https://docs.masumi.network
   - Support channels through Masumi platform

2. **Smithery AI**: For MCP server related issues
   - Documentation: https://smithery.ai/docs
   - Technical support through Smithery platform

3. **Cardano Network**: For blockchain status
   - Status: https://cardanostatus.page
   - Explorer: https://cardanoscan.io

### Reporting Issues

When reporting issues, please include:
- Job ID (if applicable)
- Error message or status received
- Input data format used
- Timestamp of the issue
- Steps taken before the problem occurred

### Response Times

- **Critical Issues**: Service completely down - Immediate attention
- **High Priority**: Payment or NFT minting failures - Within 4 hours
- **Medium Priority**: Performance issues - Within 24 hours
- **Low Priority**: Documentation or enhancement requests - Within 72 hours

## 📊 Service Limits

### Rate Limits
- Maximum 10 requests per minute per user
- Maximum 100 requests per hour per user

### Content Limits
- Minimum resume text: 50 characters
- Maximum resume text: 5,000 characters
- Supported languages: English (primary)

### Technical Limits
- PDF size: Up to 5MB
- IPFS metadata: Up to 1MB
- Processing timeout: 10 minutes

---

**Need additional help?** Check the FULL_GUIDE.md for comprehensive setup and usage instructions.