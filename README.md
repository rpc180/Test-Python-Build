# 🚀 Azure AI Foundry Agent – Python Test Harness

This project is a lightweight, production-style Python application designed to **connect to and interact with Azure AI Foundry agents** using the `azure.ai.agents` SDK.

It provides a clean baseline for:

- Validating connectivity to Foundry-deployed agents
- Sending and receiving messages
- Building reusable agent interaction patterns
- Serving as a foundation for more advanced AI-enabled applications

---

## 📌 Project Goals

This repository focuses on two primary scripts:

### 🔹 `basic_test.py`

A minimal validation script that:

- Authenticates using Azure credentials
- Connects to a Foundry project endpoint
- Retrieves an existing agent
- Sends a simple message
- Prints the agent’s response

👉 **Purpose:**
Quickly confirm that your environment, authentication, and agent connectivity are working correctly.

---

### 🔹 `image_test.py` (optional/extended)

An extended test script that:

- Accepts user input (text and/or image)
- Sends structured messages to the agent
- Demonstrates more advanced interaction patterns

👉 **Purpose:**
Serve as a foundation for building user-driven or multimodal agent workflows.

---

## 🛠️ Prerequisites

Before getting started, ensure you have:

- ✅ Python 3.10+
- ✅ VS Code (recommended)
- ✅ Azure CLI installed
- ✅ Access to an Azure AI Foundry project
- ✅ A deployed agent (created via UI or API)

---

## 📥 Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

---

### 2️⃣ Open in VS Code

```bash
code .
```

---

### 3️⃣ Create a Virtual Environment

```bash
python -m venv .venv
```

---

### 4️⃣ Activate the Virtual Environment

**Windows (PowerShell):**

```powershell
.venv\Scripts\Activate
```

**Mac/Linux:**

```bash
source .venv/bin/activate
```

---

### 5️⃣ Select the Python Interpreter in VS Code ⚠️

Even after activating the virtual environment, VS Code may still be using a different Python interpreter.

To ensure the correct one is selected:

Press Ctrl + Shift + P
Search for: Python: Select Interpreter
Choose the interpreter that points to:
.venv\Scripts\python.exe (Windows)

or

.venv/bin/python (Mac/Linux)

✅ You should now see .venv in the bottom-right corner of VS Code.

---

### 5️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 6️⃣ Authenticate to Azure

```bash
az login
```

This allows `DefaultAzureCredential` to work automatically.

---

### 7️⃣ Configure Environment Variables

Copy the example file:

```bash
copy .env.example .env
```

(or on Mac/Linux)

```bash
cp .env.example .env
```

Then update `.env` with your values:

```env
AZURE_AI_PROJECT_ENDPOINT=https://<your-resource>.services.ai.azure.com/api/projects/<your-project>
AZURE_AGENT_ID=asst_xxxxxxxxxxxxxxxxx
```

⚠️ **Important:**

- `AZURE_AGENT_ID` must be the actual agent ID (not name)
- `.env` is not committed to git (by design)

---

## ▶️ Run the Basic Test

```bash
python src/basic_test.py
```

### ✅ Expected Output

- Successful authentication message
- Agent retrieval confirmation
- A response from your agent

---

## 🧪 Troubleshooting

### ❌ `ValueError: No value for given attribute`

**Cause:** Missing or incorrect environment variable
**Fix:** Verify `.env` contains:

```env
AZURE_AGENT_ID=...
```

---

### ❌ Authentication Errors

If `DefaultAzureCredential` fails:

```bash
az login
```

Or ensure your account has access to the Foundry project.

---

### ❌ `.env` Not Loading

Ensure:

- `.env` is in the **project root**
- Script uses:

```python
load_dotenv(Path(__file__).resolve().parents[1] / ".env")
```

---

## 🧱 Project Structure

```
.
├── src/
│   ├── basic_test.py
│   ├── image_test.py
│
├── .env.example
├── requirements.txt
├── README.md
```

---

## 🔐 Security Notes

- `.env` is excluded via `.gitignore`
- Never commit credentials or secrets
- Use Azure RBAC for access control

---

## 🚧 Future Enhancements

- Reusable agent client wrapper
- CLI interface for agent interaction
- Structured logging and error handling
- Integration with APIs / front-end apps
- Multi-agent orchestration patterns

---

## 💡 Why This Project Matters

This project demonstrates:

- Real-world Azure AI Foundry integration
- Secure credential handling
- Clean Python environment setup
- Practical agent interaction patterns

It is intentionally designed to be:

✅ Simple to run
✅ Easy to extend
✅ Useful as a learning and portfolio artifact

---

## 📬 Contributions / Ideas

Feel free to fork and expand:

- Add new agent workflows
- Integrate with cloud services (AWS/Azure hybrid)
- Build UI layers or APIs
