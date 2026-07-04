# 03. Complete Beginner's Guide to TenantMind AI

Welcome to TenantMind AI! If you are a property manager, a landlord, a tenant, or simply someone who wants to understand how this platform works without getting lost in programming jargon, this guide is for you. We will explain all the fancy tech terms—like RAG, MCP, and Vector Databases—using everyday analogies.

---

## 1. The Big Picture: What is TenantMind AI?
Managing properties involves a lot of repetitive, manual tasks: answering tenant questions about lease terms, assigning plumbers to fix leaky sinks, tracking rent payments, and sending reminders. 

TenantMind AI acts as a **smart virtual assistant** for property management. It doesn't replace humans; instead, it handles the routine work so landlords and tenants can get things done faster. It can read and understand lease agreements, classify maintenance requests, and coordinate with vendors automatically.

---

## 2. Core Concepts Explained with Simple Analogies

To understand how the system works under the hood, let's break down the main technologies using real-world comparisons.

### A. RAG (Retrieval-Augmented Generation)
* **The Tech Term**: Retrieval-Augmented Generation.
* **The Analogy**: An **Open-Book Exam**.
* **How it works**: 
  Traditional AI models (like standard ChatGPT) are like students taking a closed-book exam. They answer questions based on what they memorized during training. Sometimes, they forget details or make things up (this is called "hallucinating").
  **RAG** makes the AI take an *open-book* exam. When a tenant asks, *"Can I have a pet dog in apartment 4B?"*, the system first **retrieves** the specific lease agreement for apartment 4B from the library. It then hands that lease to the AI (the **augmentation**) and asks it to write an answer based *only* on that document. The AI **generates** a response like: *"Yes, according to Section 12 of your lease, pets under 25 lbs are allowed."*
  This ensures the AI's answers are accurate, verified, and grounded in your actual documents.

### B. Vector Databases (Qdrant)
* **The Tech Term**: Vector Database.
* **The Analogy**: A **Conceptual Library Index**.
* **How it works**:
  If you search a regular library catalog for "dogs," you only find books containing the word "dogs." If a book talks about "canine companions" or "four-legged puppies" without saying the word "dogs," a traditional search will miss it.
  A **Vector Database** (we use one called **Qdrant**) translates the *meaning* of sentences into mathematical coordinates (vectors). It maps similar concepts close to each other. In a vector database, "dogs," "puppies," "canines," and "pets" are placed in the same conceptual neighborhood. When a tenant asks about "pets," Qdrant can instantly find lease sections discussing "animals," "cats," or "dogs" because it understands the *context* and *intent*, not just the keywords.

### C. MCP (Model Context Protocol)
* **The Tech Term**: Model Context Protocol.
* **The Analogy**: A **Smart Tool Belt with a Security Guard**.
* **How it works**:
  An AI by itself is just a brain; it cannot interact with the real world. It cannot delete files, send emails, or query database tables. 
  **MCP** is like giving the AI a smart tool belt. It allows the AI to plug into external systems (like sending a maintenance work order to a plumber or checking a payment status). 
  But because letting an AI run tools can be risky, TenantMind AI includes an **approval system**. If the AI tries to use a high-risk tool (like deleting a user or scheduling a refund), the MCP system halts the action and asks a human landlord for approval. Low-risk tools (like reading a public FAQ) are auto-approved.

### D. Keycloak & OIDC (Authentication)
* **The Tech Term**: OpenID Connect / Identity Provider.
* **The Analogy**: **Airport Security and Boarding Passes**.
* **How it works**:
  When you enter an airport, you show your passport to security, and they hand you a boarding pass (a token). You don't show your passport at every single gate; you just show your boarding pass.
  **Keycloak** is the airport security guard for TenantMind AI. When you log in, Keycloak verifies who you are and hands your browser a secure "boarding pass" (a JWT token). When you navigate the app or request data, your browser shows this token to the backend server. The server instantly knows whether you are a Tenant (who can only view their own apartment) or a Landlord (who can view the whole building).

### E. MongoDB (NoSQL Database)
* **The Tech Term**: Document Database.
* **The Analogy**: A **Flexible Filing Cabinet**.
* **How it works**:
  Traditional databases are like rigid spreadsheets where every row must have the exact same columns. If a column is missing, it breaks.
  **MongoDB** is like a cabinet filled with folders (called documents). Each folder can contain different pieces of paper. For example, one tenant's profile folder might contain their car license plate, while another tenant's folder doesn't have a car but contains emergency contact details. This flexibility allows TenantMind AI to store diverse properties, leases, and maintenance logs without forcing them into a rigid, fragile structure.

### F. Celery & Redis (Task Queues)
* **The Tech Term**: Message Broker and Task Queue.
* **The Analogy**: A **Busy Restaurant Kitchen**.
* **How it works**:
  Imagine you order food at a restaurant. The waiter (the Web API) doesn't run into the kitchen and cook the food himself while you wait at the counter. Instead, he writes your order on a ticket and sticks it on a wheel (the Broker, **Redis**). The kitchen staff (the Workers, **Celery**) grab the tickets one by one and cook the meals in the background while the waiter goes back to take more orders.
  In TenantMind AI, when a landlord clicks "Generate 100 Rent Invoices," the web server doesn't freeze up while calculating. It posts the tasks to **Redis**, and **Celery** workers calculate the bills and send emails in the background. The user interface remains fast and responsive.

### G. MinIO (Object Storage)
* **The Tech Term**: S3-Compatible Object Storage.
* **The Analogy**: A **Digital Safe-Deposit Box**.
* **How it works**:
  Databases are great for text and numbers, but they are terrible at holding heavy files like high-resolution lease PDFs, photos of damaged sinks, or video walkthroughs.
  **MinIO** is our digital safe-deposit box. We save the heavy files there and put a small text note (a link) in MongoDB pointing to the file. When a user needs to see the document, the app generates a temporary, secure key for them to peek inside the safe-deposit box.

### H. Prometheus & Grafana
* **The Tech Term**: Observability and Monitoring.
* **The Analogy**: The **Dashboard Gauges of a Car**.
* **How it works**:
  **Prometheus** is like the sensors in a car monitoring engine temperature, oil levels, and speed. It constantly records metrics from the TenantMind servers.
  **Grafana** is the digital dashboard screen on your steering wheel. It takes the numbers from Prometheus and turns them into beautiful graphs, warning lights, and dials so system administrators can see if the servers are running hot or running out of memory before a breakdown happens.

---

## 3. Step-by-Step: How a Tenant's Question Gets Answered

Let's see how these systems coordinate when a tenant asks a question:

1. **Ask**: Tenant types in the chat: *"Can I sublet my room this summer?"*
2. **Authenticate**: The system checks the tenant's Keycloak "boarding pass" to verify their identity and determine which lease belongs to them.
3. **Retrieve**: The system embeds the query using `sentence-transformers` and searches the **Qdrant Vector Database** to find the lease terms for that tenant.
4. **Formulate**: Qdrant returns the exact section (e.g., *"Subletting is permitted only with written landlord consent"*).
5. **Generate**: The system passes the question and the lease section to the **LLM (AI Engine)**.
6. **Respond**: The AI writes a polite response: *"According to your lease, you can sublet your room, but you must get written consent from your landlord first. Would you like me to draft a request email for you?"*
7. **Log**: The entire interaction is logged in **MongoDB** for audit records and tracked in **TraceNest** for system health.

---

## 4. Safety First: The "Human-in-the-Loop" Principle
AI is incredibly smart, but it can make mistakes. TenantMind AI uses a strict security design:
* **No Direct Actions on Critical Systems**: The AI cannot transfer money, rewrite leases, or dispatch vendors without a human landlord clicking "Approve" on the dashboard.
* **Encrypted Storage**: All sensitive files and user passwords are encrypted.
* **Tenant Isolation**: The system acts like an apartment building with thick concrete walls—data from tenant A can never leak or be visible to tenant B.
