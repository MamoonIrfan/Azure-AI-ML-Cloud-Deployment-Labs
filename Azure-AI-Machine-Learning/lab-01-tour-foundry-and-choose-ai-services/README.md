# Lab 1 — Tour Microsoft Foundry and Choose the Right AI Service

In this lab you map the Azure AI landscape and set up the workspace you use for the rest of the week. You create the resource group `rg-ai-w8-labs`, create a Microsoft Foundry resource and project, and take a guided tour of the Foundry portal. Then you try a prebuilt AI service and a large language model side by side, and finish by choosing the right service for eleven real support-team tasks. This maps to the syllabus topic **Azure AI ecosystem and Cognitive Services; selecting services (vision, language, decision, speech)**.

Run on https://portal.azure.com and https://ai.azure.com — sign in with your Azure free account (https://azure.microsoft.com/free).

> **Before you start:** choose a short **suffix** for names that must be unique across Azure: your initials plus two digits, for example `rm42`. Wherever a lab shows `<suffix>`, type yours. Allow about 75 minutes.

---

## Step 1 — Create the resource group `rg-ai-w8-labs`

1. Go to **https://portal.azure.com** and sign in.
2. In the search bar type `resource groups` and open **Resource groups**. Click **+ Create**.
3. On the **Basics** tab enter:
   - Subscription: your free-account subscription
   - Resource group: `rg-ai-w8-labs`
   - Region: `East US`
4. Click **Next: Tags** and add the tag Name `course`, Value `ai-w8`.
5. Click **Review + create**, then **Create**.

Every resource you create this week goes into this group, so one delete at the end of Lab 8 removes everything. The tag lets you filter the week's costs in Cost Management.

---

## Step 2 — Browse the AI services in the Azure Marketplace

1. In the portal, click **+ Create a resource** (on the Home page, or search `create a resource`).
2. In the left list of categories, click **AI + Machine Learning**.
3. Find these services in the list. You do not create any of them now; just read each card.

| Service | What it does | Lab |
|---|---|---|
| **Microsoft Foundry** | One resource that gives access to models, agents and all the Foundry Tools below | All labs |
| **Azure Language** | Sentiment, key phrases, entities, PII, language detection, conversational language understanding (CLU), question answering | 1, 5, 6 |
| **Speech** | Speech to text, text to speech, speech translation | 5 |
| **Translator** | Text and document translation between 100+ languages | 5 |
| **Document Intelligence** | Text, tables and named fields from documents (OCR) | 3, 4 |
| **Content Safety** | Detects harmful text and images, and prompt attacks | 2 |
| **Azure AI Search** | Indexes and searches your own documents | 6 |
| **Azure Machine Learning** | Trains, deploys and monitors your own models | 7, 8 |

4. Close the blade without creating anything.

Older material calls the prebuilt services **Cognitive Services** and later **Azure AI services**. Microsoft now calls them **Foundry Tools**. They are the same kind of service: an API that Microsoft has already trained, which you call with your data. A **Foundry resource** bundles them, so one endpoint and one set of keys work for all of them.

---

## Step 3 — Open the Foundry portal and create a project

1. Open a new browser tab and go to **https://ai.azure.com**. Sign in with the same account.
2. At the top of the page, make sure the **New Foundry** toggle is **on**.
3. Click **Create new project** (if you already have projects, click the project name at the top left, then **Create new project**).
4. Enter the project name `contoso-support`, then expand **Advanced options** and set:
   - Foundry resource: `foundry-ai-w8-<suffix>`
   - Subscription: your free-account subscription
   - Resource group: `rg-ai-w8-labs`
   - Region: `East US`
5. Click **Create**. Creation takes 2–4 minutes. The project home page opens when it finishes.

A **Foundry resource** is the Azure resource that you pay for and secure. A **project** is a workspace inside it where you keep your model deployments, agents and files. One resource can hold several projects, for example one per team.

---

## Step 4 — Tour the Foundry portal

1. Look at the navigation bar across the top of the portal and click each section in turn:

| Section | What you find there | Used in |
|---|---|---|
| **Home** | The project endpoint, the project API key and quick-start links | This step |
| **Discover** | The model catalog: hundreds of models from Microsoft, OpenAI, Meta, Mistral and others, with benchmarks | Step 6 |
| **Build** | Everything you build: **Agents**, **Models** (your deployments), **Services** (Foundry Tools), **Tools**, **Knowledge**, **Guardrails**, **Data**, **Evaluations**, **Fine-tune** | Labs 1–6 |
| **Operate** | Monitoring, tracing and compliance across all your projects | Lab 6 |
| **Manage** | Quota, resource details, project users and connected resources | Step 5 |
| **Docs** | Documentation links | — |

2. Click **Home**. Note the **Project endpoint** and the **API key**. Click the eye icon to reveal the key, then hide it again.
3. Click **Manage** > **Resource details**. Note the resource name, region and the **Add project** button.
4. At the top of the page, switch the **New Foundry** toggle **off**. The portal changes to **Foundry (classic)**, with a left-hand menu that includes **Playgrounds**, **Fine-tuning** and **Management center**. Switch it back **on**.

You will use both views this week. The new portal is where Microsoft adds new features. A few older features, such as the Language playground for sentiment analysis and conversational language understanding, are documented in the classic view, and Lab 5 uses it.

---

## Step 5 — Find the Foundry resource in the Azure portal

1. Go back to the Azure portal tab. Open **Resource groups** > `rg-ai-w8-labs`.
2. Click `foundry-ai-w8-<suffix>`. Note the **Type**: **Foundry** (sometimes shown as **Azure AI services**).
3. In the left menu, click **Resource Management** > **Keys and Endpoint**. Note **KEY 1**, **KEY 2**, the **Location** and the **Endpoint**.
4. Click **Pricing tier** in the left menu and note the tier: **S0 Standard**. You pay per call or per page; there is no monthly fee.

The same resource appears in both portals. The Azure portal is where you manage it: keys, access control, networking, cost. The Foundry portal is where you use it. Lab 2 secures these keys properly.

---

## Step 6 — Find and deploy a model from the catalog

1. In the Foundry portal, click **Discover**. The **Models** tab shows the model catalog.
2. Use the filters to narrow the list, for example **Inference tasks** = `Chat completion`, or **Collections** = `Azure OpenAI`.
3. Search for `gpt-5-mini` and open its **model card**. Note the description, the supported inputs (text and images), the context length and the benchmark scores.
4. Click **Deploy** > **Default settings**. Leave the deployment name as `gpt-5-mini` and click **Deploy**.
5. When the deployment finishes, the model's playground opens.

A model in the catalog is not usable until you **deploy** it. A deployment gives the model an endpoint in your project and a **quota** in tokens per minute. If this step says you have no quota, read the note in the course index (your free trial may need upgrading to pay-as-you-go), and follow your instructor's screen for Steps 6 and 8.

---

## Step 7 — Try a prebuilt service: language detection

1. In the Foundry portal, click **Build** > **Services**. Note the tiles: these are the Foundry Tools available in your resource.
2. Open **Azure Language - Language detection**.
3. Replace the sample text with:

```
Ma facture n'est pas encore arrivée. Pouvez-vous me l'envoyer ?
```

4. Click **Detect**. Note the detected language (**French**), its ISO code (`fr`) and the **confidence score**.
5. Try two more lines: `¿Cuándo empieza el curso?` and `When does the course start?`.
6. Open the **Code** tab (or **View code**). Note the endpoint and key the playground uses, and the JSON request it sends.

A prebuilt service does one task, returns structured JSON with a confidence score, and costs a fixed price per call. You do not deploy anything: it works as soon as the Foundry resource exists.

---

## Step 8 — Try the same task with a language model

1. Click **Build** > **Models**, select `gpt-5-mini`, and open its **playground** (chat).
2. In the chat box, enter:

```
What language is this, and what does the writer want? "Ma facture n'est pas encore arrivée. Pouvez-vous me l'envoyer ?"
```

3. Read the answer. Then ask the same question again and compare the two answers.
4. Find the **Instructions** (system message) box. Enter `Reply with only the ISO language code.` and ask again.

| | Prebuilt service (Step 7) | Language model (Step 8) |
|---|---|---|
| **Output** | Fixed JSON fields, same every time | Free text; wording varies between runs |
| **Scope** | One task | Many tasks, described in plain language |
| **Confidence score** | Yes | No |
| **Cost model** | Per call (per 1,000 text records) | Per token in and out |
| **Best when** | You need a reliable, testable result for a known task | The task is open-ended or needs reasoning across several steps |

Both answers are useful, but in different ways. When an application needs the same field in the same format every time, for example to route a ticket, a prebuilt service is easier to test and cheaper to run.

---

## Step 9 — Choose services for the support team's tasks

1. Open `service-selection.csv` from this lab folder in Excel or a text editor.
2. For each task, fill in what the output must be, which service you would choose, why, and one limitation or cost question.
3. When you finish, compare your answers with the table below.

| Task | Service | Why |
|---|---|---|
| Read the text on a scanned invoice | **Document Intelligence** (Read) or **Content Understanding** | OCR built for documents; returns text with page positions |
| Pull the invoice number and total as fields | **Document Intelligence** (prebuilt invoice model) | Returns named fields such as `InvoiceId` and `InvoiceTotal` |
| Positive or negative feedback | **Azure Language** (sentiment analysis) | Prebuilt, returns a label and scores |
| Recorded call to text | **Speech** (speech to text) | Built for audio, including speaker separation |
| Translate an announcement | **Translator** | Consistent translation at a fixed price per character |
| What does the student want? | **Azure Language** (conversational language understanding) | You define the intents; it returns intent and entities |
| Answer from approved FAQ answers | **Azure Language** (custom question answering) | Returns only answers you approved |
| Answer from policy documents, with sources | **Azure AI Search** + a model or agent | Retrieves the relevant passages and cites them (Lab 6) |
| Block abusive messages | **Content Safety** / Foundry **Guardrails** | Detects harmful content and prompt attacks |
| Predict enrolments | **Azure Machine Learning** | A custom model trained on your own data (Labs 7–8) |
| Box every laptop in a photo | A custom **object detection** model in **Azure Machine Learning** | Needs your own labelled images and a trained detector (Lab 3 explains) |

The syllabus groups services into **vision**, **language**, **speech** and **decision**. Use those groups to start, then ask: *What exact output do I need? Does a prebuilt service already produce it, or must I train my own model?* The old "decision" services (Personalizer, Anomaly Detector) have been retired. Today, decisions come from a custom model in Azure Machine Learning, from rules, or, for harmful-content decisions, from Content Safety.

---

## Clean up

Nothing to delete. **Keep** `rg-ai-w8-labs`, the Foundry resource and project, and the `gpt-5-mini` deployment: Labs 2–6 use them. The Foundry resource has no monthly fee, and you pay only for the calls you make.

## What you learned

- The Azure AI landscape: Foundry Tools (Language, Speech, Translator, Document Intelligence, Content Safety), Azure AI Search, Foundry models and agents, and Azure Machine Learning.
- A Foundry resource is the billable, securable Azure resource; a project is a workspace inside it.
- How to navigate the Foundry portal (Home, Discover, Build, Operate, Manage) and switch between the new and classic views.
- Models must be deployed before use, and deployments use token quota.
- Prebuilt services return fixed, testable outputs; language models are flexible but vary between runs.
- How to choose a service by asking what output you need and whether a prebuilt service already produces it.

---

## Files in this lab folder

| File | What it is |
|------|------------|
| `service-selection.csv` | The worksheet for Step 9. |

## Microsoft Learn

- [What is Microsoft Foundry?](https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry)
- [Create a Foundry project](https://learn.microsoft.com/en-us/azure/foundry/how-to/create-projects)
- [Find your way from Foundry (classic)](https://learn.microsoft.com/en-us/azure/foundry/how-to/navigate-from-classic)
- [Foundry Tools overview](https://learn.microsoft.com/en-us/azure/ai-services/what-are-ai-services)
- [Choose an Azure AI services technology](https://learn.microsoft.com/en-us/azure/architecture/data-guide/technology-choices/ai-services)
- [Azure Language overview](https://learn.microsoft.com/en-us/azure/ai-services/language-service/overview)
- [Learning path: Get started with AI applications and agents on Azure (AI-900)](https://learn.microsoft.com/en-us/training/paths/get-started-with-artificial-intelligence-on-azure/)
