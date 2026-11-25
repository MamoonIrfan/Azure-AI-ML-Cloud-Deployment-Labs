# Lab 6 — Build a Search Index and a Grounded Agent

In this lab you make the support team's policy documents searchable and give students three ways to get answers from them. First you mine the documents with Azure AI Search: an indexer reads them from Blob Storage, AI skills extract key phrases and entities, and you query the index in Search explorer. Then you build a **custom question answering** knowledge base from an approved FAQ list, the successor to QnA Maker. Finally you create an **agent** in Foundry Agent Service that answers questions in plain language using only the policy documents, and shows its sources. This maps to the syllabus topic **Knowledge mining and conversational AI (bots)**.

Run on https://portal.azure.com and https://ai.azure.com — sign in with your Azure free account (https://azure.microsoft.com/free).

> **Before you start:** you need the Foundry resource, the project `contoso-support` and the `gpt-5-mini` deployment from Lab 1, and the `policies` folder and `faq.tsv` from this lab folder. An Azure subscription can have only **one** free Azure AI Search service; if you already have one, use it instead of creating a new one in Step 2. Allow about 2 hours.

---

## Step 1 — Upload the policy documents to Blob Storage

1. In the Azure portal, search `storage accounts`, open **Storage accounts** and click **+ Create**.
2. On the **Basics** tab enter:
   - Resource group: `rg-ai-w8-labs`
   - Storage account name: `staiw8<suffix>` (lowercase letters and numbers only)
   - Region: `East US`
   - Primary service: `Azure Blob Storage or Azure Data Lake Storage Gen 2`
   - Performance: `Standard`
   - Redundancy: `Locally-redundant storage (LRS)`
3. Click **Review + create**, then **Create**. Click **Go to resource**.
4. In the left menu click **Data storage** > **Containers** > **+ Container**. Name it `policies` and click **Create**.
5. Open `policies`, click **Upload**, select the five `.txt` files from this lab's `policies` folder, and click **Upload**.
6. Click `refund-policy.txt` and **Edit** to read it. Close it without saving.

These five short documents stand in for a company's knowledge: policies, manuals, contracts and reports. In real projects there are thousands of them in PDFs, Word files and scanned images, and nobody can find anything. **Knowledge mining** is the process of extracting structure from that content and making it searchable.

---

## Step 2 — Create an Azure AI Search service

1. Search `ai search`, open **AI Search** and click **+ Create**.
2. On the **Basics** tab enter:
   - Resource group: `rg-ai-w8-labs`
   - Service name: `srch-ai-w8-<suffix>`
   - Location: `East US`
   - Pricing tier: click **Change Pricing Tier**, select **Free** and click **Select**
3. Click **Review + create**, then **Create**. Click **Go to resource**.

The Free tier is enough for this lab: 50 MB of storage and up to 3 indexes, 3 indexers and 3 skillsets. It cannot scale and does not support managed identities, so it is for learning, not production.

---

## Step 3 — Tour the search service

1. On the **Overview** page, note the **Url** of the service and the command bar: **Import data**, **Search explorer** and others.
2. Open the **Usage** tab (or **Monitoring** > **Usage**) and note your limits and current use: indexes, indexers, data sources, skillsets and storage.
3. In the left menu, expand **Search management** and note its items:

| Item | What it is |
|---|---|
| **Indexes** | The searchable store: a set of fields, like a database table built for search |
| **Indexers** | Crawlers that read a data source on a schedule and fill an index |
| **Data sources** | Connections to where the content lives, such as a Blob container |
| **Skillsets** | AI enrichment steps run during indexing, such as OCR, key phrases and entities |

4. In the left menu click **Settings** > **Keys**. Note the **admin keys** (full control) and **query keys** (search only).

---

## Step 4 — Import and enrich the documents

1. On the **Overview** page, click **Import data**.
2. Select **Azure Blob Storage** as the data source, then the **Keyword search** scenario.
3. On **Connect to your data**, select your subscription, the storage account `staiw8<suffix>` and the container `policies`. Leave **Authenticate using managed identity** unticked. Click **Next**.
4. On **Apply AI enrichments**:
   - Tick **Extract key phrases** (the label may be **Extract phrases**)
   - Tick **Extract entities**, click its **gear** icon, select **Persons**, **Locations**, **Organizations** and **Date/time**, and click **Save**
   - Leave **Use a free Foundry Tools resource (limited enrichments)** selected
   - Click **Next**
5. On **Preview mappings** (or **Configure the index**), look at the fields the wizard will create, such as `content`, `metadata_storage_name` and `keyphrases`. Select `metadata_storage_name`, click **Configure field**, and check that it is **Retrievable**, **Filterable** and **Sortable**. Click **Next**.
6. On **Advanced settings**, set **Schedule** to `Once`. Click **Next**.
7. On **Review and create**, set **Objects name prefix** to `policies` and click **Create**.

The wizard creates four objects at once: a **data source** (the container), a **skillset** (the enrichments), an **index** (the fields) and an **indexer** (the crawler that connects them). The free Foundry Tools resource allows 20 enriched documents per indexer per day, which is plenty for five files.

---

## Step 5 — Check the indexer and skillset

1. In the left menu click **Search management** > **Indexers** and open `policies-indexer`.
2. Wait until the status shows **Success**, then note **Docs succeeded**: `5`. Click the run in the **Execution history** to see any warnings.
3. Click **Search management** > **Skillsets** and open `policies-skillset`. Read the JSON definition and find the `KeyPhraseExtractionSkill` and `EntityRecognitionSkill` and their `inputs` and `outputs`.
4. Click **Search management** > **Indexes** and open `policies-index`. On the **Fields** tab, note each field's type and attributes (**Retrievable**, **Filterable**, **Searchable** and so on). Write down the exact names of the key phrase and entity fields.

An indexer pipeline does what you did by hand in Labs 3 and 5, but for every document automatically: crack the file, extract the text (with OCR if needed), run the AI skills, and store the results as searchable fields. If a field is not **Filterable** you cannot filter on it later without rebuilding the index, so the field settings matter.

---

## Step 6 — Query the index in Search explorer

1. On the index page, open the **Search explorer** tab.
2. In **Query view**, type `refund` and click **Search**. Note that the results include `refund-policy.txt` with a `@search.score`, and the enriched fields.
3. Switch to **JSON view** and run each query below. Use the field names you wrote down in Step 5 if they differ.

```
{ "search": "*", "count": true, "select": "metadata_storage_name" }
```

```
{ "search": "invoice duplicate", "select": "metadata_storage_name, keyphrases", "count": true }
```

```
{ "search": "*", "filter": "metadata_storage_name eq 'support-hours.txt'", "select": "metadata_storage_name, content" }
```

4. Search for `money back`. Note that it finds little or nothing, because no document contains those words.

Keyword search matches the words in the query against the words in the documents and ranks the results with a relevance score. It is fast and predictable, but it does not understand meaning: "money back" does not match "refund". The agent in Steps 9–11 closes this gap.

---

## Step 7 — Create a custom question answering project

1. Go to **https://ai.azure.com**, open `contoso-support`, and switch the **New Foundry** toggle **off** (classic view).
2. In the left menu click **Management center** > **Connected resources** > **+ New connection**. Choose **Azure AI Search**, select `srch-ai-w8-<suffix>` and click **Add connection**. Return to the project.
3. Click **Fine-tuning** > **AI Service fine-tuning** > **+ Fine-tune**. Select **Custom question answering** and click **Next**.
4. Enter:
   - Connected Azure AI Search resource: `srch-ai-w8-<suffix>`
   - Name: `contoso-faq`
   - Language: `English`
5. Click **Create**.
6. Open **Edit knowledge base** > **Question Answer Pairs**, choose **Import questions and answers**, select `faq.tsv` from this lab folder and import it. Three question-and-answer pairs appear.
7. Open the pair **What is the refund deadline?** and add the alternate question `How long do I have to get my money back?`. Click **Save changes**.

**Custom question answering** returns only answers that someone has written and approved. It suits a fixed FAQ, where every answer must be exact. You add alternate phrasings so that different questions reach the same approved answer.

---

## Step 8 — Test and deploy the knowledge base

1. Click **Test knowledge base** (or **Test**). Ask each question and note the answer and its **confidence score**:
   - `How long do I have to get my money back?`
   - `When are you open?`
   - `Do you sell gift cards?`
2. Note the result for the last question, which has no matching answer: the service returns a default "no answer found" response instead of inventing one.
3. Click **Deploy knowledge base** > **Deploy**, and confirm.
4. Switch the **New Foundry** toggle back **on**.

The deployed knowledge base has an endpoint that a chatbot, a website widget or a Teams app can call. Answer quality depends on the FAQ you maintain, not on a model's general knowledge.

---

## Step 9 — Create an agent

1. In the new Foundry portal, click **Build** > **Agents** > **Create agent**.
2. Enter the name `contoso-policy-agent`. The agent playground opens with `gpt-5-mini` selected as its model.
3. In **Instructions**, enter:

```
You are the Contoso Training student-support assistant. Answer only from the attached policy documents. Name the document you used for each answer. If the documents do not contain the answer, say that you do not know and suggest contacting the help desk. Never ask for passwords.
```

4. Under **Tools**, check the list. If a **Web search** tool is already attached, remove it, so that the agent cannot answer from the internet.
5. Click **Save**.

An **agent** combines a model, instructions and tools. The model handles language, the instructions set its job and limits, and the tools give it abilities, such as searching documents or running code.

---

## Step 10 — Ground the agent in the policy documents

1. In the agent playground, under **Tools**, click **Add** > **File search**.
2. Click **Upload files** and select the five files from this lab's `policies` folder. Click **Attach** (or **Upload and save**) and wait until indexing finishes.
3. Click **Save**.

File search splits the documents into chunks, turns each chunk into a vector (a list of numbers that represents its meaning), and stores them in a **vector store**. When a student asks a question, the agent retrieves the most relevant chunks and answers from them. This pattern is called **retrieval-augmented generation (RAG)**.

---

## Step 11 — Test the agent

In the chat pane on the right, ask each question and check the answer against the policy files:

1. `How long do I have to get my money back?` (expected: 14 calendar days if the course has not started; source `refund-policy.txt`)
2. `Can I still get a refund after my course has started?` (expected: a manual review)
3. `I forgot my password. Can I send it to you to fix my account?` (expected: no, use **Forgot password**; source `account-policy.txt`)
4. `Are you open on Saturday?` (expected: no, Monday to Friday)
5. `What is the capital of France?` (expected: it does not know, because the documents do not say)

For each answer, look for the **citation** that links to the source document. Compare question 1 with your keyword search for `money back` in Step 6.

The agent understood "money back" as "refund" because it searches by meaning, and it said where the answer came from. This supports the **transparency** principle from Lab 2. Its answers are still generated text, so check them against the sources before you trust them.

---

## Step 12 — Compare the three patterns and the bot options

| Pattern | How it answers | Strength | Weakness | Use it for |
|---|---|---|---|---|
| **Search index** (Steps 4–6) | Returns matching documents, ranked | Fast, predictable, shows every match | Matches words, not meaning; user must read the document | Search boxes, document discovery, filtering |
| **Custom question answering** (Steps 7–8) | Returns an approved answer | Exact, controlled answers | Only answers what you wrote | FAQs, policy answers that must not vary |
| **Agent with RAG** (Steps 9–11) | Generates an answer from retrieved passages, with citations | Understands meaning; answers from many documents | Answers can vary and must be checked | Questions across large document collections |

Older courses built chatbots with the **Bot Framework SDK** and **Azure Bot Service**. The SDK was archived in December 2025. To put an assistant in front of users today:

| Option | What it is | Use it when |
|---|---|---|
| **Foundry Agent Service** | Managed agents with models, tools and knowledge (this lab) | Developers build an AI assistant on Azure |
| **Copilot Studio** | A low-code tool for building agents and publishing them to Teams, websites and Microsoft 365 Copilot | Business teams build assistants without much code |
| **Microsoft 365 Agents SDK** | A code library that connects an agent to channels such as Teams and web chat | Developers need full control of channels and conversation state |

---

## Clean up

Nothing to delete now. **Keep** the search service, storage account, knowledge base and agent until the end of the course; the resource group is deleted in Lab 8. The search service and the free enrichments cost nothing; the storage account and the agent's vector store cost a few cents.

## What you learned

- Knowledge mining with Azure AI Search: data sources, skillsets, indexes and indexers, created with the Import data wizard.
- How AI enrichment extracts key phrases and entities from documents during indexing.
- How to query an index in Search explorer, and why keyword search does not understand meaning.
- How custom question answering (the successor to QnA Maker) returns approved answers from an FAQ.
- How to build a Foundry agent with instructions and file search, and how retrieval-augmented generation grounds its answers and cites sources.
- When to use a search index, custom question answering, an agent, Copilot Studio or the Microsoft 365 Agents SDK.

---

## Files in this lab folder

| File | What it is |
|------|------------|
| `policies/` | Five short synthetic policy documents: refunds, invoices, accounts, document uploads and support hours. |
| `faq.tsv` | Three approved question-and-answer pairs in the import format for custom question answering. |

## Microsoft Learn

- [What is Azure AI Search?](https://learn.microsoft.com/en-us/azure/search/search-what-is-azure-search)
- [Create a search service in the portal](https://learn.microsoft.com/en-us/azure/search/search-create-service-portal)
- [Import data wizard](https://learn.microsoft.com/en-us/azure/search/search-import-data-portal)
- [Quickstart: create a skillset in the portal](https://learn.microsoft.com/en-us/azure/search/search-get-started-skillset)
- [Search explorer](https://learn.microsoft.com/en-us/azure/search/search-explorer)
- [Custom question answering quickstart](https://learn.microsoft.com/en-us/azure/ai-services/language-service/question-answering/quickstart/sdk)
- [What is Foundry Agent Service?](https://learn.microsoft.com/en-us/azure/foundry/agents/overview)
- [What is Copilot Studio?](https://learn.microsoft.com/en-us/microsoft-copilot-studio/fundamentals-what-is-copilot-studio)
- [Microsoft 365 Agents SDK overview](https://learn.microsoft.com/en-us/microsoft-365/agents-sdk/agents-sdk-overview)
