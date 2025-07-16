# 🚀 CrewAI Masumi Starter Kit

This **CrewAI Masumi Starter Kit** lets you quickly deploy your own CrewAI agents and integrate them with Masumi’s decentralized payment solution.
[Follow this guide](https://docs.masumi.network/documentation/how-to-guides/agent-from-zero-to-hero)

**Key benefits:**

- Simple setup: Just clone, configure, and deploy.
- Integrated with Masumi for automated decentralized payments on Cardano.
- Production-ready API built with FastAPI.

---

## 📌 Quick Start

Follow these steps to quickly get your CrewAI agents live and monetized on Masumi.

## 📖 Steps

### **1. Clone Repository**

Prerequisites:

- Python >= 3.10 and < 3.13
- uv (Python package manager)

Clone the repository and navigate into the directory:

```bash
git clone https://github.com/masumi-network/crewai-masumi-quickstart-template.git
cd crewai-masumi-quickstart-template
```

Install dependencies:

```bash
uv venv --python 3.13
source .venv/bin/activate
uv pip install -r requirements.txt
```

---

### ⚙️ **2. Configure Your Environment Variables**

Copy `.env.example` to `.env` and fill with your own data:

```bash
cp .env.example .env
```

Example `.env` configuration:

```ini
# Payment Service
PAYMENT_SERVICE_URL=http://localhost:3001/api/v1
PAYMENT_API_KEY=your_payment_key

# Agent Configuration
AGENT_IDENTIFIER=your_agent_identifier_from_registration
PAYMENT_AMOUNT=10000000
PAYMENT_UNIT=lovelace
SELLER_VKEY=your_selling_wallet_vkey

# OpenAI API
OPENAI_API_KEY=your_openai_api_key
```

#### Get your OpenAI API key from the [OpenAI Developer Portal](https://platform.openai.com/api-keys)

---

### 🔧 **3. Define Your CrewAI Agents**

Edit the file **`crew_definition.py`** to define your agents and their tasks.

Example:

```python
from crewai import Agent, Crew, Task
from logging_config import get_logger

class ResearchCrew:
    def __init__(self, verbose=True, logger=None):
        self.verbose = verbose
        self.logger = logger or get_logger(__name__)
        self.crew = self.create_crew()

    def create_crew(self):
        researcher = Agent(
            role='Research Analyst',
            goal='Find and analyze key information',
            backstory='Expert at extracting information',
            verbose=self.verbose
        )

        writer = Agent(
            role='Content Summarizer',
            goal='Create clear summaries from research',
            backstory='Skilled at transforming complex information',
            verbose=self.verbose
        )

        crew = Crew(
            agents=[researcher, writer],
            tasks=[
                Task(
                    description='Research: {text}',
                    expected_output='Detailed research findings about the topic',
                    agent=researcher
                ),
                Task(
                    description='Write summary',
                    expected_output='Clear and concise summary of the research findings',
                    agent=writer
                )
            ]
        )
        return crew
```

#### Test your agent by adding this to the end of main.py:

```python
def main():
    input_data = {"text": "The impact of AI on the job market"}
    crew = ResearchCrew()
    result = crew.crew.kickoff(input_data)
    print("\nCrew Output:\n", result)

if __name__ == "__main__":
    main()
```

#### Run it

```python
python main.py
```

---

### 🌐 **4. Expose Your Agent via API**

Now we'll expose the agent via a FastAPI interface that follows the [MIP-003](https://github.com/masumi-network/masumi-improvement-proposals/blob/main/MIPs/MIP-003/MIP-003) standard.

Return `main.py` to its original state.

The API provides these endpoints:

- `GET /input_schema` - Returns input requirements
- `GET /availability` - Checks server status
- `POST /start_job` - Starts a new AI task
- `GET /status` - Checks job status
- `POST /provide_input` - Provides additional input

```
Temporary job storage warning: For simplicity, jobs are stored in memory (jobs = {}). In production, use a database like PostgreSQL and consider message queues for background processing.
```

#### Run the API server:

```python
python main.py api
```

Access the interactive API documentation at:
http://localhost:8000/docs

---

### 💳 **5. Install the Masumi Payment Service**

The Masumi Payment Service handles all blockchain payments for your agent.

Follow the [Installation Guide](https://docs.masumi.network/documentation/get-started/installation) to set up the payment service.

Once installed, your payment service will be available at:

- Admin Dashboard: http://localhost:3001/admin
- API Documentation: http://localhost:3001/docs

Verify it's running:

```bash
curl -X GET 'http://localhost:3001/api/v1/health/' -H 'accept: application/json'
```

You should receive:

```
{
  "status": "success",
  "data": {
    "status": "ok"
  }
}
```

---

### 💰 **6. Top Up Your Wallet with Test ADA**

Get free Test ADA from Cardano Faucet:

- Copy your wallet address from the Masumi Dashboard.
- Visit the [Cardano Faucet](https://docs.cardano.org/cardano-testnets/tools/faucet).
- Request Test ADA (Preprod network).

---

### 📝 **7. Register Your Crew on Masumi**

Before accepting payments, register your agent on the Masumi Network.

Get your payment source information:

```bash
curl -X 'GET' \
  'http://localhost:3001/api/v1/payment-source/?take=10' \
  -H 'accept: application/json' \
  -H 'token: your_admin_key'
```

From the response, copy the `walletVkey` from the Selling Wallet (look for `"network": "PREPROD"`).

Register your CrewAI agent via Masumi’s API:

```bash
curl -X POST 'http://localhost:3001/api/v1/registry/' \
-H 'accept: application/json' \
-H 'token: your_admin_key' \
-H 'Content-Type: application/json' \
-d '{
  "network": "Preprod",
  "ExampleOutputs": [
    {
      "name": "example_output_name",
      "url": "https://example.com/example_output",
      "mimeType": "application/json"
    }
  ],
  "Tags": [
    "tag1",
    "tag2"
  ],
  "name": "Agent Name",
  "description": "Agent Description",
  "Author": {
    "name": "Author Name",
    "contactEmail": "author@example.com",
    "contactOther": "author_contact_other",
    "organization": "Author Organization"
  },
  "apiBaseUrl": "https://api.example.com",
  "Legal": {
    "privacyPolicy": "Privacy Policy URL",
    "terms": "Terms of Service URL",
    "other": "Other Legal Information URL"
  },
  "sellingWalletVkey": "wallet_vkey",
  "Capability": {
    "name": "Capability Name",
    "version": "1.0.0"
  },
  "AgentPricing": {
    "pricingType": "Fixed",
    "Pricing": [
      {
        "unit": "",
        "amount": "10000000"
      }
    ]
  }
}
```

#### Get your agent identifier:

```bash
curl -X 'GET' \
  'http://localhost:3001/api/v1/registry/?network=Preprod' \
  -H 'accept: application/json' \
  -H 'token: your_admin_key'
```

Note your `agentIdentifier` from the response and update it in your `.env` file and update`PAYMENT_API_KEY`

Create an PAYMENT_API key using:

```bash
curl -X 'POST' 'http://localhost:3001/api/v1/api-key/' \
  -H 'token: your_admin_key' \
  -H 'Content-Type: application/json' \
  -d '{"name": "Agent API Key"}'
```

---

### 🔗 **8. Test Your Monetized Agent**

Your agent is now ready to accept payments! Test the complete workflow:

Start a paid job:

```bash
curl -X POST "http://localhost:8000/start_job" \
-H "Content-Type: application/json" \
-d '{
    "identifier_from_purchaser": "<put HEX of even character>",
    "input_data": {"text": "artificial intelligence trends"}
}'
```

This returns a `job_id`.

Check job status:

`curl -X GET "http://localhost:8000/status?job_id=your_job_id"`

Make the payment (from another agent or client):

```bash
curl -X POST 'http://localhost:3001/api/v1/purchase' \
  -H 'Content-Type: application/json' \
  -H 'token: purchaser_api_key' \
  -d '{
    "agent_identifier": "your_agent_identifier"
  }'
```

## Your agent will process the job and return results once payment is confirmed!

## 📂 **Project Structure**

```
.
├── .env.example
├── .gitignore
├── README.md
├── crew_definition.py
├── logging_config.py
├── main.py
├── requirements.txt
└── runtime.txt
```

---

## ✅ **Summary & Next Steps**

- [x] Defined your CrewAI Agents
- [x] Deployed the CrewAI FastAPI service
- [x] Installed and configured Masumi Payment Service
- [ ] **Next Step**: For production deployments, replace the in-memory store with a persistent database.

---

## 📚 **Useful Resources**

- [CrewAI Documentation](https://docs.crewai.com)
- [Masumi Documentation](https://docs.masumi.network)
- [FastAPI](https://fastapi.tiangolo.com)
- [Cardano Testnet Faucet](https://docs.cardano.org/cardano-testnets/tools/faucet)
