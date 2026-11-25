# Lab 5 — Analyze Text, Speech and Translation, and Build a CLU Model

In this lab you give the support team's systems the ability to understand language. You analyze student feedback for sentiment, key phrases, entities and personal data with Azure Language, then turn speech into text and text into speech with the Speech service, and translate an announcement with Translator. Finally you build and train your own **conversational language understanding (CLU)** model. It reads a student's message and works out what they want and which order they mean. CLU replaces LUIS, which was retired in March 2026. This maps to the syllabus topic **Azure NLP — text analysis, speech, translation; LUIS and QnA**.

Run on https://ai.azure.com — sign in with your Azure free account (https://azure.microsoft.com/free).

> **Before you start:** you need the Foundry resource `foundry-ai-w8-<suffix>` in **East US** and the project `contoso-support` from Lab 1, and `intent-test-cases.csv` from this lab folder. You need a microphone for Step 6 (a laptop or phone headset works). Allow about 2 hours.

---

## Step 1 — Switch to the classic view and tour the playgrounds

1. Go to **https://ai.azure.com** and open the `contoso-support` project.
2. At the top of the page, switch the **New Foundry** toggle **off**. The portal changes to **Foundry (classic)** with a menu on the left.
3. In the left menu click **Playgrounds**. Note the playground tiles, including **Chat**, **Agents**, **Language**, **Translator** and **Speech**.
4. Find **Fine-tuning** in the left menu as well. You use it in Step 9 to build the CLU model.

This lab uses the classic view because Microsoft documents the full Language playground and CLU there as of October 2026. Step 8 (Translator) uses the new view. The services are the same; only the portal view differs. Language Studio, the older separate website for these tools, retires on 20 March 2027.

---

## Step 2 — Analyze sentiment

1. On **Playgrounds**, click **Try the Language playground**.
2. Select the **Analyze sentiment** tile (you may find it under a group such as **Classify text**).
3. Replace the sample text with this student feedback:

```
The replacement laptop arrived late. The support team fixed the setup quickly. Please send the invoice to learner@example.com.
```

4. Click **Run**. Look at the results:
   - The overall **sentiment** of the document and its scores for **positive**, **neutral** and **negative**
   - The sentiment of **each sentence**: the first is negative, the second positive, the third neutral
5. If the configuration pane offers **Opinion mining**, turn it on and run again. Note how it links a target (`laptop`) to an opinion (`late`).

Sentiment analysis works per sentence, then combines the sentences into an overall label, which here is likely **mixed**. A support team can sort thousands of messages this way and read the negative ones first.

---

## Step 3 — Extract key phrases and entities

1. In the Language playground, select **Extract key phrases**. Keep the same text and click **Run**. Note phrases such as `replacement laptop`, `support team` and `invoice`.
2. Select **Extract named entities** and click **Run**. Note each entity's **category** (for example **Product** or **Email**) and its **confidence score**.
3. Select **Extract PII** (personally identifiable information) and click **Run**. Note that `learner@example.com` is detected as an **Email** and shown redacted, as `*******************`, in the output text.

| Feature | Question it answers | Example output |
|---|---|---|
| **Sentiment analysis** | How does the writer feel? | `mixed`; sentence 2 `positive` |
| **Key phrase extraction** | What is the text about? | `replacement laptop`, `invoice` |
| **Named entity recognition** | Which people, places, products, dates? | `laptop` (Product) |
| **PII detection** | Which personal data must be protected? | `learner@example.com` (Email), redacted |
| **Language detection** | Which language is it written in? | `English` (you tried this in Lab 1) |

PII detection lets you redact personal data before storing messages or sending them to another service. This supports the **privacy and security** principle from Lab 2.

---

## Step 4 — Summarize a longer text

1. In the Language playground, select **Summarize information** (or **Extractive summarization**).
2. Paste this text and click **Run**:

```
A learner may request a refund within 14 calendar days of purchase if the course has not started. After the course begins, refunds require a manual review by the support team. Invoices are emailed within two business days after payment is confirmed. A duplicate invoice can be requested from the help desk using the order number. Support is available Monday through Friday, 09:00 to 17:00 Pakistan Standard Time.
```

3. Note which sentences it selects and their rank scores.

**Extractive** summarization picks the most important sentences from the original text. **Abstractive** summarization writes new sentences, like a language model does. Extractive is safer when every word must come from an approved document.

---

## Step 5 — Look at the playground's code and settings

1. In any Language playground result, open the **View code** (or **Code**) tab. Note the endpoint, the API version and the JSON request body.
2. Look at the **JSON** tab of the result. Every feature returns the same pattern: a list of `documents`, each with results and confidence scores.

Everything you did in the playground is one REST call to your Foundry resource. An application would send the same JSON. You tested the service before writing a single line of code.

---

## Step 6 — Turn speech into text

1. Go back to **Playgrounds** and click **Try the Speech playground**.
2. Select **Real-time transcription** (speech to text).
3. Under **Configure**, leave the language on **auto-detect** or choose **English (United States)**.
4. Click the **microphone** button, allow microphone access in the browser, and read this sentence aloud at normal speed:

```
Hello, I bought the Python course last week and I would like a refund for order four eight two one.
```

5. Stop recording. Read the transcript and compare it with what you said. Check whether `four eight two one` became `4821`.
6. Open the **JSON** tab. Find the `offset` and `duration` of each phrase and the recognized `text`.
7. Record a second sentence, this time speaking quickly or with background noise, and compare the result.

Speech to text converts audio into text with timestamps, so you can, for example, jump to the moment in a call where a customer said "refund". Converting spoken numbers into digits is called **inverse text normalization**, and the service does it for you.

---

## Step 7 — Turn text into speech

1. In the Speech playground, select **Voice gallery** (text to speech).
2. Choose a neural voice, for example **Ava** (`en-US-AvaMultilingualNeural`), and click **Try it out** (or **Open in playground**).
3. Enter this text and click **Play**:

```
Your refund for order 4821 has been approved. You will receive the money within five business days.
```

4. Try two other voices, and any **speaking style** the voice offers (for example **cheerful** or **customer service**).
5. Filter the gallery by language and find the voices for **Urdu (Pakistan)**.

Neural text to speech produces natural-sounding audio for phone systems, accessibility features and voice assistants. Free accounts get half a million characters of neural voice per month.

---

## Step 8 — Translate an announcement

1. Switch the **New Foundry** toggle **on**. Click **Build** > **Models**, open the **AI services** tab and select **Azure Translator - Text translation**.
2. Leave the source language on **Auto-detect**, and set the target languages to **French**, **Spanish** and **Urdu**.
3. Enter this announcement and click **Translate**:

```
The Data Science course starts on Monday at 10:00. Please bring your laptop and charger. Classes are held in Room 4.
```

4. Note the **detected source language**, and compare the three translations. Check that numbers and times such as `10:00` and `Room 4` are kept.
5. Open the **Code** tab and note that one request returned all three languages.
6. Switch the **New Foundry** toggle **off** again for the CLU steps.

**Translator** translates text with consistent results at a fixed price per character. The **Speech** service can also translate speech directly. Use Translator for written text and Speech translation for live audio.

---

## Step 9 — Create a CLU project and define intents and an entity

1. In the left menu click **Fine-tuning**, then the **AI Service fine-tuning** tab, then **+ Fine-tune**.
2. Select **Conversational language understanding** and click **Next**.
3. Enter:
   - Connected service: your Foundry resource
   - Name: `contoso-helpdesk`
   - Language: `English`
4. Click **Create**. The project opens on **Define schema**.
5. On the **Intents** tab, click **+ Add intent** three times and create `TrackOrder`, `ReportDamage` and `RequestInvoice`. Note the built-in `None` intent.
6. Open the **Entities** tab, click **+ Add entity** and create `OrderNumber`.
7. Select `OrderNumber`. Under its components, add a **Regular expression** component with the key `four-digits` and the pattern `\b\d{4}\b`. Save it.

An **intent** is what the user wants to do. An **entity** is a piece of information the app needs to do it, here the order number. The regular expression component finds any four-digit number. CLU can also *learn* entities from labelled examples, which you try in the next step.

---

## Step 10 — Add training utterances

1. In the left menu of the project, click **Manage data** (or **Data labeling**). Keep **Training set** selected.
2. Select the intent `TrackOrder`, type each utterance below, and press **Enter** after each one. Repeat for the other intents.

| Intent | Utterances |
|---|---|
| `TrackOrder` | `Where is my order 4821?` / `Track delivery 5530 please` / `What is the status of order 1207?` / `Has package 3391 shipped yet?` / `Can you check order 6610 for me?` |
| `ReportDamage` | `My laptop arrived with a cracked screen` / `The headset I received is broken` / `The box was crushed and the keyboard is damaged` / `My charger stopped working on arrival` / `The monitor came with deep scratches` |
| `RequestInvoice` | `Please send the invoice for order 2290` / `I need a copy of my bill for 7741` / `Can I get a receipt for order 1015?` / `Email me the invoice for purchase 3302` / `Where can I download the invoice for 9908?` |
| `None` | `What is the weather today?` / `Tell me a joke` / `Who won the cricket match?` |

3. In two or three utterances, select the order number with your mouse and choose `OrderNumber` to label it.
4. Click **Save changes**.

**Utterances** are example messages. The model learns from their variety, not from exact words, so it can recognize "Could you locate delivery 7193?" even though that sentence is not in the training data. The `None` intent teaches the model to say "this is not something I handle".

---

## Step 11 — Train and evaluate the model

1. Click **Train model** > **+ Train model**.
2. Enter Model name `helpdesk-v1`, select **Standard training** (free, English only), and choose **Automatically split the testing set from training data**.
3. Click **Train**. Training takes a few minutes.
4. When it finishes, click **Evaluate your model** (or **Model performance**) and select `helpdesk-v1`.
5. Note the overall **precision**, **recall** and **F1 score**, and the scores per intent. Open the **confusion matrix**.

| Metric | Question it answers |
|---|---|
| **Precision** | When the model predicts `TrackOrder`, how often is it right? |
| **Recall** | Of all the real `TrackOrder` messages, how many did it find? |
| **F1 score** | One number that balances precision and recall |

With only 18 utterances, the automatic test set holds just a few examples, so the scores are rough. A production model needs many more varied utterances, from real users if possible.

---

## Step 12 — Deploy and test the model

1. Click **Deploy model** > **+ Deploy a trained model**.
2. Select **Create a new deployment**, enter the name `production`, assign the model `helpdesk-v1`, and click **Create**.
3. Go to **Playgrounds** > **Language playground** and select **Conversational language understanding**. Choose the project `contoso-helpdesk` and the deployment `production`.
4. Open `intent-test-cases.csv`. Enter each utterance in the playground, click **Run**, and fill in the `actual_intent`, `actual_entity` and `score_or_review` columns.
5. Note any message the model gets wrong, and suggest an utterance you would add to fix it.

The test file contains sentences the model has never seen, including `What is the capital of France?`, which should go to `None`. A support app would use the intent to route the message, and the `OrderNumber` entity to look up the order.

---

## Step 13 — Compare the old and new services

| Older service | Status | Replacement | Where you use it |
|---|---|---|---|
| **LUIS** (Language Understanding) | Retired 31 March 2026 | **Conversational language understanding (CLU)** | Steps 9–12 |
| **QnA Maker** | Retired 31 October 2025 | **Custom question answering** in Azure Language | Lab 6 |
| **Text Analytics** | Became part of Azure Language | **Azure Language** sentiment, key phrases, entities, PII | Steps 2–4 |
| **Language Studio** website | Retires 20 March 2027 | The **Foundry portal** | This lab |

The concepts you learned (intents, entities, utterances, training, evaluation, deployment) are the same in LUIS and CLU. What changed is the service and the portal.

Switch the **New Foundry** toggle back **on** before you leave.

---

## Clean up

Nothing to delete. **Keep** the Foundry resource and the CLU project. The playground calls in this lab fit within the monthly free allowances for Language, Speech and Translator, and Standard CLU training is free.

## What you learned

- How to analyze text with Azure Language: sentiment, key phrases, named entities, PII and summarization.
- How speech to text returns timestamps and converts spoken numbers into digits, and how neural text to speech offers voices and styles.
- How Translator translates one text into several languages in a single request.
- How to build a CLU model: define intents and entities, add utterances, train, evaluate with precision and recall, deploy and test.
- That CLU replaces LUIS and custom question answering replaces QnA Maker, with the same core concepts.

---

## Files in this lab folder

| File | What it is |
|------|------------|
| `intent-test-cases.csv` | Six unseen messages with the expected intent and order number. Fill in the actual results in Step 12. |

## Microsoft Learn

- [What is Azure Language?](https://learn.microsoft.com/en-us/azure/ai-services/language-service/overview)
- [Sentiment analysis and opinion mining](https://learn.microsoft.com/en-us/azure/ai-services/language-service/sentiment-opinion-mining/overview)
- [PII detection](https://learn.microsoft.com/en-us/azure/ai-services/language-service/personally-identifiable-information/overview)
- [Speech to text quickstart](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/get-started-speech-to-text)
- [Text to speech quickstart](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/get-started-text-to-speech)
- [What is Azure Translator?](https://learn.microsoft.com/en-us/azure/ai-services/translator/overview)
- [CLU quickstart](https://learn.microsoft.com/en-us/azure/ai-services/language-service/conversational-language-understanding/quickstart)
- [Migrate from LUIS or QnA Maker to Azure Language](https://learn.microsoft.com/en-us/azure/ai-services/language-service/reference/migrate)
- [Migrate from Language Studio to Foundry](https://learn.microsoft.com/en-us/azure/ai-services/language-service/migration-studio-to-foundry)
