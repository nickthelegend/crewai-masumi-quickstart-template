import os
import uvicorn
import uuid
from dotenv import load_dotenv
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, Field, field_validator
from masumi.config import Config
from masumi.payment import Payment, Amount
from crew_definition import ResumeCrew, call_mcp_server, mint_nft
from simple_crew import generate_resume_html, upload_to_pinata
from logging_config import setup_logging

# Configure logging
logger = setup_logging()

# Load environment variables
load_dotenv(override=True)

# Retrieve API Keys and URLs
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PAYMENT_SERVICE_URL = os.getenv("PAYMENT_SERVICE_URL")
PAYMENT_API_KEY = os.getenv("PAYMENT_API_KEY")
NETWORK = os.getenv("NETWORK")

logger.info("Starting application with configuration:")
logger.info(f"PAYMENT_SERVICE_URL: {PAYMENT_SERVICE_URL}")

# Initialize FastAPI
app = FastAPI(
    title="Resume Generation Service - Masumi API Standard",
    description="Professional resume generation service that creates HTML resumes, converts them to PDF, and mints them as NFTs. Integrated with Masumi payment system.",
    version="1.0.0"
)

# ─────────────────────────────────────────────────────────────────────────────
# Temporary in-memory job store (DO NOT USE IN PRODUCTION)
# ─────────────────────────────────────────────────────────────────────────────
jobs = {}
payment_instances = {}

# ─────────────────────────────────────────────────────────────────────────────
# Initialize Masumi Payment Config
# ─────────────────────────────────────────────────────────────────────────────
config = Config(
    payment_service_url=PAYMENT_SERVICE_URL,
    payment_api_key=PAYMENT_API_KEY
)

# ─────────────────────────────────────────────────────────────────────────────
# Pydantic Models
# ─────────────────────────────────────────────────────────────────────────────
class StartJobRequest(BaseModel):
    identifier_from_purchaser: str
    input_data: dict[str, str]
    
    class Config:
        json_schema_extra = {
            "example": {
                "identifier_from_purchaser": "resume_job_123",
                "input_data": {
                    "text": "Name: Alice Johnson\nEmail: alice@example.com\nPhone: (555) 123-4567\nLocation: San Francisco, CA\n\nProfessional Summary:\nSenior Software Engineer with 5+ years developing web applications using Python, JavaScript, and React.\n\nWork Experience:\n- Senior Software Engineer at TechCorp (2021-2024)\n  * Led development of microservices architecture\n  * Improved system performance by 40%\n  * Mentored junior developers\n\nEducation:\n- Bachelor of Science in Computer Science\n  University of Technology (2015-2019)\n\nSkills:\nPython, JavaScript, React, Node.js, Docker, AWS, PostgreSQL, Git"
                }
            }
        }

class ProvideInputRequest(BaseModel):
    job_id: str

# ─────────────────────────────────────────────────────────────────────────────
# Resume Generation Task Execution (Using Working Functions from crew_definition)
# ─────────────────────────────────────────────────────────────────────────────
async def execute_crew_task(input_data: dict) -> dict:
    """Execute resume generation workflow using functions from crew_definition"""
    try:
        resume_text = input_data.get("text", "")
        
        # Extract name for token name
        name = "Resume"
        for line in resume_text.split('\n'):
            if line.strip().startswith("Name:"):
                name = line.replace("Name:", "").strip().replace(" ", "_")
                break
        
        logger.info("Step 1: Generating HTML resume...")
        html_content = generate_resume_html(resume_text)
        
        logger.info("Step 2: Converting to PDF via MCP server...")
        pdf_result = call_mcp_server(html_content, "resume.pdf")
        
        # Extract PDF URL from result
        pdf_url = None
        if "https://" in pdf_result:
            pdf_url = pdf_result.split("https://")[1].split()[0]
            pdf_url = "https://" + pdf_url
        
        if pdf_url:
            logger.info("Step 3: Uploading metadata to IPFS...")
            short_token_name = f"{name[:8]}_NFT"
            ipfs_cid = upload_to_pinata(pdf_url, short_token_name)
            
            logger.info("Step 4: Minting NFT from IPFS metadata...")
            nft_result = mint_nft(ipfs_cid, short_token_name)
            
            result = {
                "html_length": len(html_content),
                "pdf_result": pdf_result,
                "ipfs_cid": ipfs_cid,
                "nft_result": nft_result,
                "status": "completed"
            }
        else:
            result = {
                "html_length": len(html_content),
                "pdf_result": pdf_result,
                "status": "pdf_failed"
            }
        
        logger.info(f"Resume workflow completed: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Error in resume workflow: {str(e)}")
        return {"error": str(e), "status": "failed"}

# ─────────────────────────────────────────────────────────────────────────────
# 1) Start Job (MIP-003: /start_job)
# ─────────────────────────────────────────────────────────────────────────────
@app.post("/start_job")
async def start_job(data: StartJobRequest):
    """ Initiates a job and creates a payment request """
    print(f"Received data: {data}")
    print(f"Received data.input_data: {data.input_data}")
    try:
        job_id = str(uuid.uuid4())
        agent_identifier = os.getenv("AGENT_IDENTIFIER")
        
        # Log the input text (truncate if too long)
        input_text = data.input_data["text"]
        truncated_input = input_text[:100] + "..." if len(input_text) > 100 else input_text
        logger.info(f"Received job request with input: '{truncated_input}'")
        logger.info(f"Starting job {job_id} with agent {agent_identifier}")

        # Define payment amounts
        payment_amount = os.getenv("PAYMENT_AMOUNT", "10000000")  # Default 10 ADA
        payment_unit = os.getenv("PAYMENT_UNIT", "lovelace") # Default lovelace

        amounts = [Amount(amount=payment_amount, unit=payment_unit)]
        logger.info(f"Using payment amount: {payment_amount} {payment_unit}")
        
        # Create a payment request using Masumi
        payment = Payment(
            agent_identifier=agent_identifier,
            #amounts=amounts,
            config=config,
            identifier_from_purchaser=data.identifier_from_purchaser,
            input_data=data.input_data,
            network=NETWORK
        )
        
        logger.info("Creating payment request...")
        payment_request = await payment.create_payment_request()
        payment_id = payment_request["data"]["blockchainIdentifier"]
        payment.payment_ids.add(payment_id)
        logger.info(f"Created payment request with ID: {payment_id}")

        # Store job info (Awaiting payment)
        jobs[job_id] = {
            "status": "awaiting_payment",
            "payment_status": "pending",
            "payment_id": payment_id,
            "input_data": data.input_data,
            "result": None,
            "identifier_from_purchaser": data.identifier_from_purchaser
        }

        async def payment_callback(payment_id: str):
            await handle_payment_status(job_id, payment_id)

        # Start monitoring the payment status
        payment_instances[job_id] = payment
        logger.info(f"Starting payment status monitoring for job {job_id}")
        await payment.start_status_monitoring(payment_callback)

        # Return the response in the required format
        return {
            "status": "success",
            "job_id": job_id,
            "blockchainIdentifier": payment_request["data"]["blockchainIdentifier"],
            "submitResultTime": payment_request["data"]["submitResultTime"],
            "unlockTime": payment_request["data"]["unlockTime"],
            "externalDisputeUnlockTime": payment_request["data"]["externalDisputeUnlockTime"],
            "agentIdentifier": agent_identifier,
            "sellerVkey": os.getenv("SELLER_VKEY"),
            "identifierFromPurchaser": data.identifier_from_purchaser,
            "amounts": amounts,
            "input_hash": payment.input_hash,
            "payByTime": payment_request["data"]["payByTime"],
        }
    except KeyError as e:
        logger.error(f"Missing required field in request: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=400,
            detail="Bad Request: If input_data or identifier_from_purchaser is missing, invalid, or does not adhere to the schema."
        )
    except Exception as e:
        logger.error(f"Error in start_job: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=400,
            detail="Input_data or identifier_from_purchaser is missing, invalid, or does not adhere to the schema."
        )

# ─────────────────────────────────────────────────────────────────────────────
# 2) Process Payment and Execute AI Task
# ─────────────────────────────────────────────────────────────────────────────
async def handle_payment_status(job_id: str, payment_id: str) -> None:
    """ Executes CrewAI task after payment confirmation """
    try:
        logger.info(f"Payment {payment_id} completed for job {job_id}, executing task...")
        
        # Update job status to running
        jobs[job_id]["status"] = "running"
        logger.info(f"Input data: {jobs[job_id]["input_data"]}")

        # Execute the AI task
        result = await execute_crew_task(jobs[job_id]["input_data"])
        logger.info(f"Resume generation completed for job {job_id}")
        
        # Mark payment as completed on Masumi
        await payment_instances[job_id].complete_payment(payment_id, result)
        logger.info(f"Payment completed for job {job_id}")

        # Update job status
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["payment_status"] = "completed"
        jobs[job_id]["result"] = result

        # Stop monitoring payment status
        if job_id in payment_instances:
            payment_instances[job_id].stop_status_monitoring()
            del payment_instances[job_id]
    except Exception as e:
        logger.error(f"Error processing payment {payment_id} for job {job_id}: {str(e)}", exc_info=True)
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)
        
        # Still stop monitoring to prevent repeated failures
        if job_id in payment_instances:
            payment_instances[job_id].stop_status_monitoring()
            del payment_instances[job_id]

# ─────────────────────────────────────────────────────────────────────────────
# 3) Check Job and Payment Status (MIP-003: /status)
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/status")
async def get_status(job_id: str):
    """ Retrieves the current status of a specific job """
    logger.info(f"Checking status for job {job_id}")
    if job_id not in jobs:
        logger.warning(f"Job {job_id} not found")
        raise HTTPException(status_code=404, detail="Job not found")

    job = jobs[job_id]

    # Check latest payment status if payment instance exists
    if job_id in payment_instances:
        try:
            status = await payment_instances[job_id].check_payment_status()
            job["payment_status"] = status.get("data", {}).get("status")
            logger.info(f"Updated payment status for job {job_id}: {job['payment_status']}")
        except ValueError as e:
            logger.warning(f"Error checking payment status: {str(e)}")
            job["payment_status"] = "unknown"
        except Exception as e:
            logger.error(f"Error checking payment status: {str(e)}", exc_info=True)
            job["payment_status"] = "error"


    result_data = job.get("result")
    result = result_data if isinstance(result_data, dict) else None

    return {
        "job_id": job_id,
        "status": job["status"],
        "payment_status": job["payment_status"],
        "result": result
    }

# ─────────────────────────────────────────────────────────────────────────────
# 4) Check Server Availability (MIP-003: /availability)
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/availability")
async def check_availability():
    """ Checks if the server is operational """

    return {"status": "available", "type": "masumi-agent", "message": "Resume Generation Service is ready to create professional resumes, convert to PDF, and mint NFTs."}
    # Commented out for simplicity sake but its recommended to include the agentIdentifier
    #return {"status": "available","agentIdentifier": os.getenv("AGENT_IDENTIFIER"), "message": "The server is running smoothly."}

# ─────────────────────────────────────────────────────────────────────────────
# 5) Retrieve Input Schema (MIP-003: /input_schema)
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/input_schema")
async def input_schema():
    """
    Returns the expected input schema for the /start_job endpoint.
    Fulfills MIP-003 /input_schema endpoint for Resume Generation Service.
    """
    return {
        "input_data": [
            {
                "id": "text",
                "type": "textarea",
                "name": "Resume Information",
                "data": {
                    "description": "Provide your resume information including name, contact details, work experience, education, and skills. The system will generate a professional HTML resume, convert it to PDF, and mint it as an NFT.",
                    "placeholder": "Name: John Smith\nEmail: john.smith@email.com\nPhone: (555) 123-4567\nLocation: New York, NY\n\nProfessional Summary:\nExperienced software engineer with 5+ years...\n\nWork Experience:\n- Senior Software Engineer at TechCorp (2021-2024)\n  * Led development of microservices\n  * Improved performance by 40%\n\nEducation:\n- Bachelor of Science in Computer Science\n  University of Technology (2015-2019)\n\nSkills:\nPython, JavaScript, React, Node.js, Docker, AWS"
                },
                "validations": [
                    {
                        "validation": "min",
                        "value": "50"
                    },
                    {
                        "validation": "max",
                        "value": "5000"
                    },
                    {
                        "validation": "format",
                        "value": "nonempty"
                    }
                ]
            }
        ]
    }

# ─────────────────────────────────────────────────────────────────────────────
# 6) Health Check
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/health")
async def health():
    """
    Returns the health of the server.
    """
    return {
        "status": "healthy"
    }

# ─────────────────────────────────────────────────────────────────────────────
# Main Logic if Called as a Script
# ─────────────────────────────────────────────────────────────────────────────
def main():
    print("Running CrewAI as standalone script is not supported when using payments.")
    print("Start the API using `python main.py api` instead.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "api":
        print("Starting FastAPI server with Masumi integration...")
        uvicorn.run(app, host="0.0.0.0", port=8000)
    else:
        main()
