# Lab 3 — Read Documents and Images with Azure AI Vision Services

In this lab you teach the support team's systems to *see*. You read a scanned supplier invoice with optical character recognition (OCR) in two tools: Content Understanding in the Foundry portal, and Document Intelligence Studio. Then you extract named fields such as the invoice number and total with a prebuilt invoice model, test what poor image quality does to the results, and ask a vision-capable language model to describe an image. You finish by comparing the four vision tasks (OCR, image description, classification and object detection) and where each one is done on Azure today. This maps to the syllabus topic **Azure Vision — image analysis, OCR, Custom Vision (classification and object detection)**.

Run on https://ai.azure.com and https://documentintelligence.ai.azure.com — sign in with your Azure free account (https://azure.microsoft.com/free).

> **Before you start:** you need the Foundry resource `foundry-ai-w8-<suffix>`, the project `contoso-support` and the `gpt-5-mini` deployment from Lab 1, and the four sample files from this lab folder on your computer. Allow about 75 minutes.

---

## Step 1 — Compare a text PDF with a scanned PDF

1. On your computer, open `invoice-text.pdf` from this lab folder. Try to select the heading **NIAI SYNTHETIC INVOICE** with your mouse. The text highlights: the PDF contains real text characters.
2. Open `invoice-scan.pdf` and try the same. Nothing highlights: this PDF contains only a picture of the page.
3. Open `invoice-scan.png`. It is the same picture as an image file.

The two PDFs look identical, but a program sees them very differently. Software can read the text PDF directly, which is what the Week 6 FastAPI PDF reader did. The scanned PDF is only pixels, so a program needs **OCR** to turn the shapes of letters back into text.

---

## Step 2 — Run OCR with Content Understanding in Foundry

1. Go to **https://ai.azure.com** and open the `contoso-support` project. Check that the **New Foundry** toggle is **on**.
2. Click **Build** > **Services** and open **Content Understanding**.
3. Set **Modality** to `Document` and choose the **Read** analyzer.
4. Upload `invoice-scan.pdf` and click **Run analysis**.
5. When it finishes, look at the results:
   - The page preview, with a box drawn around each line of text it found
   - The extracted text: check that it contains `INV-W8-001`, `14 October 2026` and `TOTAL USD: 170.00`
6. Click one line of text in the results and see which box highlights on the page.
7. Open the JSON result and scroll through it. You look at the JSON fields in detail in Step 6.

OCR returns more than text: each line and word comes with its position on the page. Content Understanding is Microsoft's newest tool for this, and it also handles images, audio and video.

---

## Step 3 — Compare with the Layout analyzer

1. In Content Understanding, change the analyzer to **Layout** and run it on `invoice-scan.pdf` again.
2. Look for the **table**: rows for **Notebook** and **Headset**, with columns **Item**, **Quantity**, **Unit USD** and **Total USD**.
3. Check that the table's rows and columns match the page.

| Analyzer | What it returns | Use it when |
|---|---|---|
| **Read** | Text lines and words with positions and confidence | You only need the text |
| **Layout** | Everything Read returns, plus tables, paragraphs, headings and selection marks | The document's structure matters, for example a table of line items |

---

## Step 4 — Open Document Intelligence Studio and connect your resource

1. Open a new tab and go to **https://documentintelligence.ai.azure.com**. Sign in with the same account.
2. Click the **settings (gear) icon** at the top right, then the **Resource** tab.
3. Select your **Directory**, your free-account **Subscription**, the resource group `rg-ai-w8-labs` and the resource `foundry-ai-w8-<suffix>`. Click **Use resource**.
4. Return to the studio home page and look at the three groups of tiles:

| Group | Examples | What it is for |
|---|---|---|
| **Document analysis** | Read, Layout | OCR and document structure |
| **Prebuilt models** | Invoices, Receipts, Identity documents, Bank statements, Pay stubs | Named fields from common document types, with no training |
| **Custom models** | Custom extraction model, Custom classification model | Train a model on your own document types |

Document Intelligence Studio is a separate website for the **Document Intelligence** service, which your Foundry resource includes. Microsoft is moving its features into the Foundry portal, but custom document models are still trained here.

---

## Step 5 — Extract invoice fields with the prebuilt invoice model

1. On the studio home page, click **Invoices** under **Prebuilt models**.
2. Click **Browse for files** and select `invoice-scan.pdf`. Click **Run analysis**.
3. Open the **Fields** tab in the results pane. Find each field and check its value against the page:

| Field | Expected value |
|---|---|
| `InvoiceId` | `INV-W8-001` |
| `InvoiceDate` | `14 October 2026` |
| `VendorName` | `Classroom Example Supplies` |
| `CustomerName` | `Synthetic Learner` |
| `InvoiceTotal` | `170.00` |
| `Items` | Two line items: Notebook and Headset |

4. Note the **confidence** next to each field. Click a field to see where on the page it came from.
5. Open the **Result** tab to see the JSON, and the **Code** tab to see how an app would call the same model.

OCR (Step 2) gives you all the text; your code then has to work out which number is the total. A **prebuilt model** has already learned what invoices look like, so it returns the total as a field named `InvoiceTotal`. Lab 4's app uses the Read model; an accounts system would use this invoice model.

---

## Step 6 — Test the effect of image quality

1. In Document Intelligence Studio, go back to the home page and open **Read**.
2. Upload `invoice-scan-low-quality.png` (a blurred copy of the same invoice) and click **Run analysis**.
3. Check the same three values: `INV-W8-001`, `14 October 2026` and `170.00`. Note any wrong characters.
4. Open the **Result** tab (JSON). Find the `content` field (all the text), and the `pages` > `words` list. Pick the word `INV-W8-001` and note its `confidence` (0 to 1) and `polygon` (the coordinates of its box on the page).
5. Run **Read** on `invoice-scan.pdf` as well and compare the same word's confidence with the blurred copy.
6. Write down how an application should respond when confidence is low, for example by asking the user to upload a clearer photo or sending the document to a person.

OCR quality depends on the input. Blur, low resolution, shadows and skew all lower confidence and can change characters, for example `8` read as `B`. Good applications check confidence instead of trusting every result.

---

## Step 7 — Describe an image with a vision-capable model

1. In the Foundry portal, click **Build** > **Models**, select `gpt-5-mini` and open its **playground**.
2. Click the **attach (paperclip or image) icon** next to the chat box and upload `invoice-scan.png`.
3. Send:

```
Describe this image in two sentences. Then list the invoice number and total. If you cannot read a value, say so instead of guessing.
```

4. Compare the answer with the Document Intelligence result from Step 5.
5. Take a photo of a sign, label or poster near you with your phone, upload it, and ask `What text is in this photo, and what is the photo of?`

A vision-capable language model can describe a scene and answer questions about it, which older material calls **image analysis** or **captioning**. Unlike Document Intelligence, it returns free text with no confidence scores or page coordinates, and its answers can vary between runs. Use it for understanding images, not as a validated OCR or detection system.

---

## Step 8 — Compare the four vision tasks

Read the table, then answer the three questions below it.

| Task | Question it answers | Output | Azure service today |
|---|---|---|---|
| **OCR** | What text is in this image? | Text with positions and confidence | **Document Intelligence**, **Content Understanding** |
| **Image description** | What is in this image? | A sentence or tags | A **vision-capable model** in Foundry, or Content Understanding |
| **Image classification** | Which category does this image belong to? | One label per image (for example `damaged` or `undamaged`) | A custom model trained in **Azure Machine Learning** |
| **Object detection** | Where is each object in this image? | A label and a bounding box for each object | A custom model trained in **Azure Machine Learning** |

1. A student uploads a photo of a damaged laptop. Which task tells you *whether* it is damaged? (Classification.)
2. Which task tells you *where* each laptop is in a warehouse photo? (Object detection.)
3. Why is a model that writes "I see two laptops" not an object detector? (It returns no boxes, no consistent labels and no measured accuracy.)

**What changed:** older courses used **Azure AI Vision Image Analysis** for tags and captions and **Custom Vision** (customvision.ai) to train classifiers and detectors. Both are scheduled to retire on **25 September 2028**, and Microsoft recommends the services in the table above for new work. Custom classification and detection now use **AutoML for images** in Azure Machine Learning. It needs labelled images and GPU compute, which you look at in Lab 7, Step 13.

---

## Clean up

Nothing to delete. **Keep** the Foundry resource and the `gpt-5-mini` deployment: Labs 4–6 use them. The free monthly allowance covers the pages you analysed in this lab.

## What you learned

- The difference between a PDF with embedded text and a scanned PDF, and why the second needs OCR.
- How to run OCR in Content Understanding and Document Intelligence Studio, and how to read the words, positions and confidence scores in the JSON.
- That Layout adds structure, such as tables, to the text that Read returns.
- How a prebuilt invoice model returns named fields instead of raw text.
- That image quality affects OCR, and applications should act on low confidence.
- How OCR, image description, classification and object detection differ, and which Azure service does each one now that Image Analysis and Custom Vision are being retired.

---

## Files in this lab folder

| File | What it is |
|------|------------|
| `invoice-text.pdf` | A synthetic invoice with embedded text. |
| `invoice-scan.pdf` | The same invoice as a scanned image inside a PDF. Used in Steps 2, 3 and 5. |
| `invoice-scan.png` | The scan as an image file. Used in Step 7. |
| `invoice-scan-low-quality.png` | A blurred copy of the scan. Used in Step 6. |

## Microsoft Learn

- [Choose the right document-processing tool](https://learn.microsoft.com/en-us/azure/ai-services/content-understanding/choosing-right-ai-tool)
- [What is Content Understanding?](https://learn.microsoft.com/en-us/azure/ai-services/content-understanding/overview)
- [Document Intelligence Read model](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/prebuilt/read)
- [Document Intelligence invoice model](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/prebuilt/invoice)
- [Document Intelligence Studio](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/studio-overview)
- [Image Analysis migration options](https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/migration-options)
- [Custom Vision migration options](https://learn.microsoft.com/en-us/azure/ai-services/custom-vision-service/migration-options)
- [AutoML for computer vision in Azure Machine Learning](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-auto-train-image-models)
