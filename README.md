<div align="center">
  <h1>Azure AI/ML & Cloud Deployment Labs</h1>
  <p><strong>A practical, step-by-step learning collection covering Azure fundamentals, Azure AI services, machine learning workflows, deployment, security, and monitoring.</strong></p>
  <p>
    <a href="https://learn.microsoft.com/azure/">
      <img src="https://img.shields.io/badge/Microsoft_Azure-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white" alt="Microsoft Azure" />
    </a>
    <a href="https://learn.microsoft.com/credentials/certifications/azure-fundamentals/">
      <img src="https://img.shields.io/badge/AZ--900-Fundamentals-2563EB?style=for-the-badge" alt="AZ-900" />
    </a>
    <a href="https://learn.microsoft.com/azure/machine-learning/">
      <img src="https://img.shields.io/badge/Azure_Machine_Learning-ML-7C3AED?style=for-the-badge" alt="Azure Machine Learning" />
    </a>
    <img src="https://img.shields.io/badge/Hands--on_Labs-24-16A34A?style=for-the-badge" alt="24 hands-on labs" />
  </p>
  <p>
    <a href="#learning-path">Learning Path</a> ·
    <a href="#azure-fundamentals">Azure Fundamentals</a> ·
    <a href="#azure-ai--machine-learning">Azure AI & ML</a> ·
    <a href="#getting-started">Getting Started</a> ·
    <a href="#cost-and-cleanup">Cost & Cleanup</a>
  </p>
</div>

---

## About this repository

This repository brings together **24 practical lab exercises** in two learning tracks:

- **16 Azure Fundamentals labs** — core cloud concepts, Azure architecture and services, identity, access control, governance, cost management, and monitoring.
- **8 Azure AI & Machine Learning labs** — Azure AI services, document intelligence, language and speech, knowledge mining, agents, model training, deployment, versioning, and monitoring.

The material is designed to help learners connect the pieces between **building an AI/ML solution and operating it on cloud infrastructure**. It includes guided instructions, PDF handouts, supporting datasets, sample documents, scripts, configuration examples, and other lab assets where provided.

> **Learning goal:** understand the practical Azure workflow around an AI/ML solution — selecting services, preparing cloud resources, applying security, working with data and AI capabilities, training models, deploying endpoints, and monitoring the resulting resources.

## Who is this for?

- Students learning Microsoft Azure and cloud computing.
- Beginners preparing for Azure Fundamentals (AZ-900) concepts.
- AI/ML learners who want to understand the cloud side of model development.
- Developers exploring Azure AI services, Azure Machine Learning, and deployment workflows.
- Anyone who prefers guided, task-based practice over theory alone.

You do not need to complete all 24 labs at once. Start with Azure Fundamentals if you are new to Azure, or use the AI & Machine Learning track if you already understand the basic Azure resource model.

## Learning path

<div align="center">
  <table>
    <tr>
      <td align="center" width="33%">
        <h3>01 · Understand Azure</h3>
        <p>Cloud concepts, portal, CLI, compute, networking, storage, identity, governance and cost.</p>
        <strong>16 labs</strong>
      </td>
      <td align="center" width="33%">
        <h3>02 · Explore Azure AI</h3>
        <p>Foundry, AI services, document processing, language, speech, search and agents.</p>
        <strong>6 applied AI labs</strong>
      </td>
      <td align="center" width="33%">
        <h3>03 · Train & Operate Models</h3>
        <p>Azure ML, pipelines, endpoints, model versions, monitoring and retraining.</p>
        <strong>2 ML lifecycle labs</strong>
      </td>
    </tr>
  </table>
</div>

---

## Azure Fundamentals

<sub><strong>16 labs</strong> · Azure Portal · Azure Cloud Shell · Azure CLI · PowerShell · Governance</sub>

This track follows the three broad AZ-900 knowledge areas represented in the supplied lab index: cloud concepts, Azure architecture and services, and Azure management and governance.

| # | Lab | Main practical focus | Instructions |
|---:|---|---|---|
| 01 | Tour the Azure Portal and Create Your First Resource Group | Portal navigation, subscriptions, resource groups and first resource | [Open lab](Azure-Fundamentals/lab-01-azure-portal-tour/) |
| 02 | Get Started with Azure Cloud Shell (CLI and PowerShell) | Cloud Shell, command-line tooling and basic Azure commands | [Open lab](Azure-Fundamentals/lab-02-cloud-shell-cli/) |
| 03 | Explore Regions, Region Pairs and Availability Zones | Azure geography, resilience and availability concepts | [Open lab](Azure-Fundamentals/lab-03-regions-availability-zones/) |
| 04 | Create a Windows Virtual Machine in the Portal | Provisioning and connecting to a Windows VM | [Open lab](Azure-Fundamentals/lab-04-windows-vm-portal/) |
| 05 | Create a Linux VM with the Azure CLI | Deploying and managing a Linux VM through CLI | [Open lab](Azure-Fundamentals/lab-05-linux-vm-cli/) |
| 06 | Create a Web App with Azure App Service | Hosting a web application with App Service | [Open lab](Azure-Fundamentals/lab-06-app-service-webapp/) |
| 07 | Deploy a Container with Azure Container Instances | Running a container workload in Azure | [Open lab](Azure-Fundamentals/lab-07-container-instances/) |
| 08 | Create a Virtual Network and Test Private Connectivity | Virtual networks and private communication | [Open lab](Azure-Fundamentals/lab-08-virtual-network/) |
| 09 | Create a Storage Account and Work with Blob Storage | Storage accounts and blob operations | [Open lab](Azure-Fundamentals/lab-09-storage-blobs/) |
| 10 | Create an Azure SQL Database | Provisioning and querying Azure SQL | [Open lab](Azure-Fundamentals/lab-10-azure-sql/) |
| 11 | Explore Microsoft Entra ID: Users and Groups | Identity, users and groups | [Open lab](Azure-Fundamentals/lab-11-entra-id/) |
| 12 | Manage Access with Azure RBAC | Role-based access control and permissions | [Open lab](Azure-Fundamentals/lab-12-rbac/) |
| 13 | Apply Resource Tags and Resource Locks | Resource organization and protection | [Open lab](Azure-Fundamentals/lab-13-tags-locks/) |
| 14 | Enforce Standards with Azure Policy | Policy definitions and governance controls | [Open lab](Azure-Fundamentals/lab-14-azure-policy/) |
| 15 | Estimate and Control Costs | Pricing Calculator, TCO and budgets | [Open lab](Azure-Fundamentals/lab-15-cost-management/) |
| 16 | Monitor Your Environment | Advisor, Service Health and Azure Monitor | [Open lab](Azure-Fundamentals/lab-16-monitoring/) |

**Track index:** [Azure Fundamentals lab index](Azure-Fundamentals/README.md) · [PDF index](Azure-Fundamentals/README.pdf)

---

## Azure AI & Machine Learning

<sub><strong>8 labs</strong> · Microsoft Foundry · Azure AI services · Azure Machine Learning · Model lifecycle</sub>

This track uses a practical scenario in which a training organization's support workflows involve scanned documents, multilingual communication, policy knowledge, and data-driven predictions. Across the labs, learners select appropriate services, secure resources, process documents, work with language and search, and train and deploy models.

| # | Lab | Main practical focus | Instructions |
|---:|---|---|---|
| 01 | Tour Microsoft Foundry and Choose the Right AI Service | Explore the Azure AI ecosystem and select services for use cases | [Open lab](Azure-AI-Machine-Learning/lab-01-tour-foundry-and-choose-ai-services/) |
| 02 | Secure an AI Resource and Run a Container | Resource security, keys/identity concepts and container execution | [Open lab](Azure-AI-Machine-Learning/lab-02-secure-ai-resources-and-run-a-container/) |
| 03 | Read Documents and Images with Azure AI Vision Services | Image analysis, OCR and document processing | [Open lab](Azure-AI-Machine-Learning/lab-03-vision-ocr-and-image-analysis/) |
| 04 | Project: Move the Document App to Azure | Package and move a document-processing application to Azure | [Open lab](Azure-AI-Machine-Learning/lab-04-move-the-document-app-to-azure/) |
| 05 | Analyze Text, Speech and Translation, and Build a CLU Model | Text analytics, speech, translation and conversational language understanding | [Open lab](Azure-AI-Machine-Learning/lab-05-language-speech-translation-and-clu/) |
| 06 | Build a Search Index and a Grounded Agent | Knowledge mining, Azure AI Search and agent-based question answering | [Open lab](Azure-AI-Machine-Learning/lab-06-knowledge-mining-and-agents/) |
| 07 | Train Models and Build a Pipeline in Azure Machine Learning Studio | Data, compute, AutoML jobs and Designer pipelines | [Open lab](Azure-AI-Machine-Learning/lab-07-train-models-in-azure-ml-studio/) |
| 08 | Deploy, Version and Monitor a Model | Managed online endpoints, model versions, monitoring and retraining | [Open lab](Azure-AI-Machine-Learning/lab-08-deploy-version-and-monitor-a-model/) |

**Track index:** [Azure AI & Machine Learning lab index](Azure-AI-Machine-Learning/README.md) · [PDF index](Azure-AI-Machine-Learning/README.pdf)

### The three Azure workspaces used in this track

| Workspace | What it is used for in these labs |
|---|---|
| [Azure portal](https://portal.azure.com/) | Creating and managing Azure resources, resource groups, access, keys, costs and hosting resources. |
| [Microsoft Foundry](https://ai.azure.com/) | Exploring and working with AI services and models, including language, speech, translation, document capabilities and agents. |
| [Azure Machine Learning studio](https://ml.azure.com/) | Working with data, compute, AutoML, Designer pipelines, jobs, models and managed endpoints. |

The supplied AI/ML lab index explains that the Azure portal manages resources, while Foundry and Azure Machine Learning studio are the workspaces used to work with AI capabilities and ML workflows.

---

## Repository structure

```text
Azure-AI-ML-Cloud-Deployment-Labs/
│
├── README.md
├── .gitignore
│
├── Azure-Fundamentals/
│   ├── README.md
│   ├── README.pdf
│   ├── lab-01-azure-portal-tour/
│   ├── lab-02-cloud-shell-cli/
│   ├── ...
│   └── lab-16-monitoring/
│
└── Azure-AI-Machine-Learning/
    ├── README.md
    ├── README.pdf
    ├── lab-01-tour-foundry-and-choose-ai-services/
    ├── lab-02-secure-ai-resources-and-run-a-container/
    ├── ...
    └── lab-08-deploy-version-and-monitor-a-model/
```

Each lab folder contains its own `README.md` with the guided instructions and, where supplied, a matching PDF handout plus supporting scripts, sample datasets, documents, JSON/YAML files, or application assets. Keep the complete lab folder together; some exercises depend on those accompanying files.

## Getting started

### 1. Prepare an Azure account

The supplied lab indexes point learners to the [Azure free account](https://azure.microsoft.com/free/). Review the current offer, subscription eligibility, quotas and service availability before creating resources. A free-account offer or credit does **not** mean every service or deployment is free.

### 2. Choose a learning track

- New to Azure? Start with `Azure-Fundamentals/README.md` and work through the 16 fundamentals labs in order.
- Already familiar with Azure basics? Start with `Azure-AI-Machine-Learning/README.md` and follow the eight AI/ML labs.

### 3. Download or clone the repository

```bash
git clone https://github.com/<YOUR-GITHUB-USERNAME>/Azure-AI-ML-Cloud-Deployment-Labs.git
cd Azure-AI-ML-Cloud-Deployment-Labs
```

Alternatively, select **Code → Download ZIP** on GitHub and extract the archive locally.

### 4. Follow each lab

1. Open the relevant track's `README.md`.
2. Read the prerequisites and resource naming/region notes before starting.
3. Follow the steps in order in the specified Azure portal or Cloud Shell environment.
4. Use the included sample files and helper scripts only where the lab instructs you to.
5. Verify the expected result before moving to the next exercise.
6. Complete the lab's **Clean up** section before leaving the resources running.

## Prerequisites

- A Microsoft account and an Azure subscription with permission to create the resources used by the selected lab.
- A modern desktop browser such as Microsoft Edge or Google Chrome.
- Stable internet access.
- For the Fundamentals track: Azure portal and, for CLI/PowerShell exercises, Azure Cloud Shell. Some exercises use a local RDP client to connect to a Windows VM.
- For the AI/ML track: access to the Azure portal, Microsoft Foundry and Azure Machine Learning studio as specified by each lab.
- Basic familiarity with navigating web applications is helpful. The labs are written as guided exercises, but some Azure terminology may be new to beginners.

**Region notes from the supplied manuals:** the Fundamentals labs use resource group `rg-az900-labs` in `Southeast Asia`; the AI/ML labs use `rg-ai-w8-labs` in `East US`. Follow the region specified in each lab rather than assuming all Azure services are available in every region.

## Cost, quotas, security and cleanup

<blockquote>
  <strong>Important: Azure resources can incur charges.</strong> Some compute, database, container, AI model and managed endpoint resources may generate costs while provisioned, even when idle. Free-account credits and quotas vary by subscription, service, region and time.
</blockquote>

- Review the pricing and quota information for each service before deployment.
- The supplied AI/ML manual notes that some model deployments may have zero quota on certain free-trial subscriptions. Follow the alternatives described in the relevant lab if that occurs.
- Do not use real customer documents, personal information, credentials, API keys or confidential company data in practice exercises. Use the supplied sample assets.
- Never commit passwords, access keys, connection strings, `.env` files or other secrets to GitHub.
- Complete every lab's cleanup instructions. The Fundamentals track specifies full course cleanup at the end of Lab 16; the AI/ML track specifies full cleanup at the end of Lab 8.
- Before deleting a resource group, verify that it contains only resources created for these exercises. Deletion is permanent.

## Learning outcomes

After completing the relevant exercises, learners should have practical familiarity with:

- Navigating Azure subscriptions, resource groups, regions and core resource services.
- Provisioning compute, networking, storage, database and application-hosting resources.
- Working with identity, RBAC, policy, tags, locks, budgets and monitoring.
- Exploring Azure AI services for vision, OCR, language, speech, translation and knowledge search.
- Moving a sample document-processing application to Azure.
- Preparing data and compute, running AutoML/Designer workflows, and working with model artifacts.
- Deploying models to managed online endpoints and exploring versioning, monitoring and retraining concepts.

These are learning outcomes represented by the supplied lab instructions; completing the guides does not itself certify production readiness or guarantee that a deployed service will meet a particular workload's requirements.

## Learning material and attribution

The lab folders preserve the supplied manuals and their supporting files. This repository organizes those materials into a single learning path and adds a top-level guide to help learners navigate them.

If you reuse or redistribute the underlying manuals, scripts, sample assets or screenshots, make sure you have the necessary permissions and retain any attribution or notices included with the original material. No affiliation with or endorsement by Microsoft is implied.

## Useful official resources

- [Microsoft Azure documentation](https://learn.microsoft.com/azure/)
- [Azure Fundamentals learning path](https://learn.microsoft.com/training/paths/azure-fundamentals-describe-cloud-concepts/)
- [Azure AI documentation](https://learn.microsoft.com/azure/ai-services/)
- [Microsoft Foundry documentation](https://learn.microsoft.com/azure/ai-foundry/)
- [Azure Machine Learning documentation](https://learn.microsoft.com/azure/machine-learning/)
- [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/)
- [Azure free account](https://azure.microsoft.com/free/)

## Feedback and contributions

Found an unclear step, broken link or outdated portal label? Open a GitHub Issue with:

1. The track and lab number.
2. The step where you encountered the problem.
3. The Azure region and service involved (do not include secrets or personal data).
4. The error text or a redacted screenshot, if useful.

Suggestions that make the instructions clearer and safer for learners are welcome.

---

<div align="center">
  <p><strong>Learn by doing. Build by practicing. Grow by exploring.</strong></p>
  <p><sub>Created as a practical learning resource during NIAI–NAVTTC AI & Machine Learning training at NETSOL Technologies Pakistan.</sub></p>
</div>
