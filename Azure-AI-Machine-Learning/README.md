# Week 8 — Azure AI and Machine Learning Labs

These eight hands-on labs teach how to build AI and machine learning solutions on Microsoft Azure. Each lab works through the Azure interfaces themselves, so you learn where things are and what each screen does: the Azure portal, the Microsoft Foundry portal, and Azure Machine Learning studio. No command line is required.

All labs run on a **free Azure account**:
**https://azure.microsoft.com/free** (USD 200 credit for 30 days + always-free services)

The labs share the resource group **`rg-ai-w8-labs`** in the region **East US**. East US is used because every service in these labs, including conversational language understanding, is available there. Lab 1 creates the resource group; the full clean-up happens at the end of Lab 8.

---

## The scenario

You work for **Contoso Training**, a company that runs short professional courses. Its student-support team spends its day on four kinds of work: reading scanned invoices, answering messages from students in several languages, looking up answers in policy documents, and making predictions from data. Across the eight labs you move this work to Azure, one capability at a time. You choose the right services, secure them, read documents, understand language, search knowledge, and train, deploy and monitor your own models.

---

## Part 1 — Azure AI services

| # | Lab | Syllabus topic | Where it runs |
|---|-----|----------------|---------------|
| 1 | [Tour Microsoft Foundry and Choose the Right AI Service](lab-01-tour-foundry-and-choose-ai-services/) | Azure AI ecosystem and Cognitive Services; selecting services | Azure portal + Foundry portal |
| 2 | [Secure an AI Resource and Run a Container](lab-02-secure-ai-resources-and-run-a-container/) | Security, resource management, deployment, containers; Responsible AI | Azure portal + Foundry portal |
| 3 | [Read Documents and Images with Azure AI Vision Services](lab-03-vision-ocr-and-image-analysis/) | Azure Vision: image analysis, OCR, custom vision | Foundry portal + Document Intelligence Studio |
| 4 | [Project: Move the Document App to Azure](lab-04-move-the-document-app-to-azure/) | Hands-on vision solution; project: move a workload to Azure | Azure portal |

## Part 2 — Language, knowledge and conversation

| # | Lab | Syllabus topic | Where it runs |
|---|-----|----------------|---------------|
| 5 | [Analyze Text, Speech and Translation, and Build a CLU Model](lab-05-language-speech-translation-and-clu/) | Azure NLP: text analysis, speech, translation; LUIS and QnA successors | Foundry portal |
| 6 | [Build a Search Index and a Grounded Agent](lab-06-knowledge-mining-and-agents/) | Knowledge mining and conversational AI (bots) | Azure portal + Foundry portal |

## Part 3 — Machine learning

| # | Lab | Syllabus topic | Where it runs |
|---|-----|----------------|---------------|
| 7 | [Train Models and Build a Pipeline in Azure Machine Learning Studio](lab-07-train-models-in-azure-ml-studio/) | Azure Machine Learning: pipelines, GPU training | Azure portal + Azure ML studio |
| 8 | [Deploy, Version and Monitor a Model](lab-08-deploy-version-and-monitor-a-model/) | MLOps and deployment: CI/CD, versioning, endpoints, monitoring, retraining | Azure ML studio — ends with full clean-up |

---

## Four-class schedule

| Class | Labs | Focus |
|-------|------|-------|
| **Class 1** | Labs 1–2 | The Azure AI landscape, choosing services, keys and identities, containers, Responsible AI |
| **Class 2** | Labs 3–4 | Reading documents and images, then deploying a real app to Azure |
| **Class 3** | Labs 5–6 | Language, speech, translation, intent recognition, search and agents |
| **Class 4** | Labs 7–8 | Training, pipelines, deployment, versioning and monitoring |

Each class is planned as three hours. Labs 7 and 8 together need more than that because jobs and deployments take time to run. Do Lab 7 Steps 1–7 (workspace, cluster, data and submitting the AutoML job) before Class 4 or at the end of Class 3, so the job has finished when Class 4 starts.

---

## The three portals you will use

| Portal | Address | What you do there |
|--------|---------|-------------------|
| **Azure portal** | https://portal.azure.com | Create and manage resources: resource groups, access control, keys, costs, container hosting |
| **Microsoft Foundry portal** | https://ai.azure.com | Try and use prebuilt AI services and models: language, speech, translation, documents, agents, guardrails |
| **Azure Machine Learning studio** | https://ml.azure.com | Train your own models: data, compute, AutoML, Designer pipelines, jobs, models, endpoints |

The Azure portal manages resources. Foundry and Azure Machine Learning studio are where you *work with* those resources. Lab 1 tours the Azure portal and Foundry; Lab 7 tours studio.

---

## Services that changed, and what these labs use instead

Several services in older course material have been retired or are being retired. These labs use the current replacements.

| Older service | Status | Used in these labs instead |
|---|---|---|
| Cognitive Services | Renamed | **Foundry Tools** (Azure Language, Speech, Translator, Document Intelligence, Content Safety) in a **Foundry resource** |
| LUIS | Retired 31 March 2026 | **Conversational language understanding (CLU)** in Azure Language (Lab 5) |
| QnA Maker | Retired 31 October 2025 | **Custom question answering** (Lab 5) and **Azure AI Search + an agent** (Lab 6) |
| Azure AI Vision Image Analysis | Retiring 25 September 2028 | **Content Understanding**, **Document Intelligence** and vision-capable models (Lab 3) |
| Custom Vision | Retiring 25 September 2028 | Explained in Lab 3; custom image models move to Azure Machine Learning |
| Azure ML data labeling | Retired 30 September 2026 | Not used |
| Bot Framework SDK | Archived December 2025 | **Foundry Agent Service** (Lab 6); Copilot Studio and Microsoft 365 Agents SDK are explained |

---

## How each lab folder is laid out

Every lab is a self-contained folder:

```
lab-07-train-models-in-azure-ml-studio/
|-- README.md                                    <- the lab instructions
|-- lab-07-train-models-in-azure-ml-studio.pdf   <- the same instructions as a PDF handout
`-- iris.csv                                     <- files the lab asks you to upload
```

- **`README.md`**: the lab instructions. Follow these on screen.
- **`<lab-name>.pdf`**: the same instructions as a PDF, for printing or a second screen.
- **Data files**: sample documents, datasets and test cases the lab asks you to upload or read. All of them are synthetic or public, so you can safely upload them to Azure.

Regenerate every PDF after editing any lab:

```bash
uv run --with reportlab python qa/render_lab_pdfs.py
```

---

## Before you start

1. Create an Azure free account at https://azure.microsoft.com/free if you do not have one. Use a personal Microsoft account, not a work account, so you have full control of the subscription.
2. Use a desktop browser (Edge or Chrome) with a large screen or two screens: one for the lab, one for Azure.
3. Download this whole folder to your computer. Several labs ask you to upload files from it.
4. Never upload real personal data, invoices or company documents. Use the supplied sample files.
5. Run every **Clean up** section. Azure bills for some resources while they exist, even when nobody uses them.

> **About free accounts and AI models:** some free-trial subscriptions receive no quota for deploying large language models such as `gpt-5-mini`. Labs 1, 2, 3 and 6 use one. If the deployment step reports zero quota, upgrade the subscription to pay-as-you-go (your remaining free credit still applies) or follow along with your instructor's screen for that step. Every other step works on a free account.
