# Lab 4 — Project: Move the Document App to Azure

In this project lab you move a real workload to Azure: the FastAPI PDF reader you built in Week 6, now extended with an OCR endpoint. You put the code on GitHub, and Azure builds it into a container image, stores it in Azure Container Registry and runs it on Azure Container Apps. Then you connect the app to Document Intelligence through a managed identity, so it can read scanned invoices with no key anywhere in its settings. Finally you push a code change and watch it deploy automatically. This maps to the syllabus topic **Hands-on: build an Azure vision solution + Project: move workload to Azure**.

Run on https://portal.azure.com and https://github.com — sign in with your Azure free account (https://azure.microsoft.com/free) and a free GitHub account (https://github.com/signup).

> **Before you start:** you need the Container Apps environment `cae-ai-w8` (Lab 2) and the Foundry resource `foundry-ai-w8-<suffix>` (Lab 1). Download the `app` folder and the sample files from this lab folder. Allow about 2 hours.

---

## Step 1 — Read the app you are moving

1. Open `app/main.py` from this lab folder in a text editor. Find the four endpoints:

| Endpoint | What it does |
|---|---|
| `GET /health` | Returns `{"status": "ok", "version": ...}` so Azure and you can check that the app is running |
| `POST /upload-pdf` | Reads the first line of text from a PDF that contains embedded text (the Week 6 behaviour) |
| `POST /ocr` | Sends a scanned PDF to Document Intelligence Read and returns the recognized text |
| `POST /store-pdf` | Saves a PDF to Blob Storage (not used in this lab) |

2. In `/ocr`, find `DOCUMENT_INTELLIGENCE_ENDPOINT` and `DefaultAzureCredential()`. The app reads the service address from an environment variable and signs in with an Azure identity, not a key.
3. Open `app/Dockerfile`. Read it line by line: start from a Python 3.11 image, install `requirements.txt`, copy `main.py`, run as a non-root user, and start the app on port **8000**.

The Dockerfile is the recipe for the **container image**. Anyone who builds it gets exactly the same app with the same package versions, on a laptop or in Azure. This is what makes the workload portable.

---

## Step 2 — Put the code on GitHub

1. Go to **https://github.com** and sign in. Click **+** (top right) > **New repository**.
2. Enter Repository name `contoso-docreader`, choose **Private**, and click **Create repository**.
3. On the empty repository page, click **uploading an existing file**.
4. Drag the three files from this lab's `app` folder into the page: `Dockerfile`, `main.py` and `requirements.txt`. Upload the files themselves, not the folder.
5. Enter the commit message `Add document app` and click **Commit changes**.
6. Check that the three files appear at the top level of the repository.

Azure will build the image from this repository. Keeping the code in source control also gives you a history of every change, which is the starting point for CI/CD (continuous integration and continuous deployment).

---

## Step 3 — Create a container registry

1. In the Azure portal, search `container registries`, open **Container registries** and click **+ Create**.
2. On the **Basics** tab enter:
   - Resource group: `rg-ai-w8-labs`
   - Registry name: `acraiw8<suffix>` (letters and numbers only)
   - Location: `East US`
   - Pricing plan: `Basic`
3. Click **Review + create**, then **Create**. Click **Go to resource**.
4. In the left menu, click **Services** > **Repositories**. It is empty for now.

A **container registry** stores container images, like GitHub stores code. Container Apps pulls the image from here each time it starts a new replica. Azure Container Registry keeps your images private, in your subscription and region.

---

## Step 4 — Create the container app

1. Open **Container Apps** and click **+ Create** > **Container App**.
2. On the **Basics** tab enter:
   - Resource group: `rg-ai-w8-labs`
   - Container app name: `ca-docreader`
   - Deployment source: `Container image`
   - Region: `East US`
   - Container Apps environment: `cae-ai-w8`
3. On the **Container** tab, tick **Use quickstart image**.
4. On the **Ingress** tab, check that ingress is enabled and accepts traffic from anywhere.
5. Click **Review + create**, then **Create**. Click **Go to resource**.

The quickstart image is a placeholder. In the next step you replace it with your own app, built from GitHub.

---

## Step 5 — Connect GitHub for continuous deployment

1. In `ca-docreader`, click **Settings** > **Continuous deployment** in the left menu.
2. Click **Sign in with GitHub** and authorize **Azure App Service** to access your account.
3. Under **GitHub settings** select:
   - Organization: your GitHub user name
   - Repository: `contoso-docreader`
   - Branch: `main`
4. Under **Registry settings** select:
   - Repository source: `Azure Container Registry`
   - Registry: `acraiw8<suffix>`
   - Image: `docreader`
5. Under **Azure access**, set **Service principal** to **Create new**.
6. Click **Start continuous deployment**. If the form reports that the registry needs admin credentials, open the registry > **Settings** > **Access keys**, tick **Admin user**, then return and try again.

Azure adds a **GitHub Actions workflow** file to your repository under `.github/workflows/`. From now on, every commit to `main` builds a new image, pushes it to your registry and deploys it as a new revision of the container app.

---

## Step 6 — Watch the build in GitHub Actions

1. In GitHub, open `contoso-docreader` and click the **Actions** tab. A workflow run is in progress.
2. Click the run, then the **build** job. Expand the steps and find where Docker installs the packages from `requirements.txt`.
3. When the build job finishes, open the **deploy** job and watch it update the container app.
4. In the Azure portal, open the registry > **Repositories** > `docreader`. Note the image **tag**: it matches the GitHub commit ID.
5. Open `ca-docreader` > **Application** > **Revisions and replicas**. A new revision is running your image.

The first build takes 3–5 minutes. If the workflow fails, open the failed step's log and read the last red lines; the usual cause is files uploaded inside a folder instead of at the top level of the repository.

---

## Step 7 — Point ingress at the app's port

1. Open the container app's **Application Url**. The page does not load correctly yet.
2. In `ca-docreader`, click **Settings** > **Ingress**. Change **Target port** from `80` to `8000` and click **Save**.
3. Wait one minute, then open `<Application Url>/health` in the browser. You see `{"status":"ok","version":"v1"}`.

The quickstart image listened on port 80, but the Dockerfile starts the app on port 8000. **Ingress** receives HTTPS traffic from the internet on port 443 and forwards it to the container's **target port**. When they do not match, the app runs but no request reaches it.

---

## Step 8 — Test the app in the browser

1. Open `<Application Url>/docs`. FastAPI generates this interactive test page from the code.
2. Expand **POST /upload-pdf**, click **Try it out**, choose `invoice-text.pdf` and click **Execute**. The response shows `"first_line": "NIAI SYNTHETIC INVOICE"`.
3. Repeat with `invoice-scan.pdf`. The response is **422**: `No embedded text. Use /ocr for a scanned PDF.`
4. Repeat with `not-a-pdf.txt`. The response is **400**: `Upload a PDF file.`
5. Expand **POST /ocr** and try `invoice-scan.pdf`. The response is **503**: `Configure DOCUMENT_INTELLIGENCE_ENDPOINT first.`

The app moved to Azure without code changes and behaves exactly as it did on your laptop. The 503 from `/ocr` is correct: the app does not know yet where Document Intelligence is, and it has no permission to call it.

---

## Step 9 — Give the app an identity and permission to call Document Intelligence

1. In `ca-docreader`, click **Security** > **Identity**. On **System assigned**, set **Status** to **On**, click **Save** and confirm with **Yes**.
2. Open `foundry-ai-w8-<suffix>` > **Access control (IAM)** > **+ Add** > **Add role assignment**.
3. Search for and select `Cognitive Services User`, then click **Next**.
4. Set **Assign access to** to **Managed identity**, click **+ Select members**, choose **Container App** > `ca-docreader` and click **Select**.
5. Click **Review + assign** twice.
6. On the Foundry resource, open **Resource Management** > **Keys and Endpoint** and copy the **Endpoint** (it looks like `https://foundry-ai-w8-<suffix>.cognitiveservices.azure.com/`).

The app's code calls `DefaultAzureCredential()`. In Azure, this finds the managed identity and gets a short-lived token from Microsoft Entra ID. The role assignment lets that identity call the service. No key is stored in the app, the registry, GitHub or the container settings.

---

## Step 10 — Configure the endpoint in a new revision

1. In `ca-docreader`, click **Application** > **Revisions and replicas** > **+ Create new revision**.
2. Select the container and click **Edit**. On **Environment variables**, add two variables with **Source** `Manual entry`:
   - Name `DOCUMENT_INTELLIGENCE_ENDPOINT`, Value: the endpoint you copied
   - Name `APP_VERSION`, Value: `v2`
3. Click **Save**, then **Create**.
4. When the new revision is running, open `<Application Url>/health`. It now shows `"version":"v2"`.
5. Open `/docs` again and run **POST /ocr** with `invoice-scan.pdf`. The response has `"status": "succeeded"` and a `content` field containing `INV-W8-001` and `TOTAL USD: 170.00`.

This is the Lab 3 OCR result, now produced by your own app running in Azure. Configuration such as the endpoint lives in environment variables, outside the image, so the same image can run in a test and a production environment with different settings.

---

## Step 11 — Split traffic between two revisions

1. Open **Revisions and replicas**. Click **Choose revision mode**, select **Multiple: Several revisions active simultaneously** and click **Apply**.
2. Tick **Show inactive revisions** if needed. Make sure both the first app revision (no `APP_VERSION`, so it reports `v1`) and the `v2` revision are **Active**.
3. Set their **Traffic** to `50` and `50` and click **Save**.
4. Open `<Application Url>/health` and refresh several times. The version alternates between `v1` and `v2`.
5. Set the traffic back to `0` for v1 and `100` for v2, click **Save**, then switch the revision mode back to **Single**.

Splitting traffic lets you release a new version to a share of users first and move everyone back instantly if it misbehaves. This is the same idea as the blue/green model deployment in Lab 8.

---

## Step 12 — Push a change and watch it deploy

1. In GitHub, open `main.py` and click the **pencil (Edit)** icon.
2. Change the line `app = FastAPI(title="NIAI Document Workshop", version="1.0")` to use `title="Contoso Document Reader"`.
3. Click **Commit changes** > **Commit changes**.
4. Open the **Actions** tab and watch the new workflow run build and deploy.
5. When it finishes, open `<Application Url>/docs`. The page title is now **Contoso Document Reader**, and `/health` still reports `v2`.

You changed code and the cloud updated itself, with no manual steps. This is **continuous deployment**. The environment variables from Step 10 carried over because each new revision copies the previous configuration and replaces only the image.

---

## Step 13 — Read the app's logs

1. In `ca-docreader`, click **Monitoring** > **Log stream** and select **Console**.
2. In another tab, run **POST /ocr** again from `/docs`.
3. In the log stream, find the line containing `operation=ocr outcome=success` and its `request_id`.
4. Compare the `request_id` with the one in the `/docs` response.

The app writes one log line per request with an ID. When a user reports a problem, the request ID lets you find exactly what happened, without logging the document contents.

---

## Step 14 — Review what you moved

Compare where each part of the workload ran before and after this lab:

| Part | Before (Week 6) | After (this lab) |
|---|---|---|
| Code | A folder on your laptop | A GitHub repository with history |
| Build | `pip install` on your laptop | GitHub Actions builds a container image from the Dockerfile |
| Image storage | None | Azure Container Registry |
| Hosting | `uvicorn` on your laptop | Azure Container Apps, with HTTPS, scaling and revisions |
| OCR | Not available | Document Intelligence, reached through a managed identity |
| Configuration | Hard-coded or local variables | Environment variables in each revision |
| Release | Restart the program | Commit to `main`; a new revision deploys automatically |

---

## Clean up

1. Open `ca-docreader` > **Settings** > **Continuous deployment** and click **Disconnect**.
2. Open `ca-docreader` and click **Delete**. Keep the environment if asked.
3. Search **Microsoft Entra ID** > **App registrations** > **All applications**. Find the registration that continuous deployment created (its name includes `ca-docreader` or `github`), open it and click **Delete**. This removes the credential GitHub used to deploy to your subscription; deleting the resource group would not remove it.
4. Open the registry `acraiw8<suffix>` and click **Delete**. A Basic registry is billed every day it exists.
5. Optional: in GitHub, delete the `contoso-docreader` repository (**Settings** > **Delete this repository**).
6. **Keep** the Foundry resource: Labs 5 and 6 use it.

## What you learned

- How a Dockerfile turns an app into a portable container image.
- How to store images in Azure Container Registry and run them on Azure Container Apps.
- How continuous deployment from GitHub builds and deploys every commit automatically.
- Why ingress must point at the container's target port.
- How a managed identity and the **Cognitive Services User** role let an app call Document Intelligence with no key.
- How environment variables, revisions and traffic splitting let you configure and release new versions safely.
- How request IDs in the log stream help you trace a single request.

---

## Files in this lab folder

| File | What it is |
|------|------------|
| `app/main.py` | The FastAPI document app: `/health`, `/upload-pdf`, `/ocr` and `/store-pdf`. |
| `app/Dockerfile` | The recipe that builds the app into a container image. |
| `app/requirements.txt` | The exact Python package versions the image installs. |
| `invoice-text.pdf` | A PDF with embedded text. Used in Step 8. |
| `invoice-scan.pdf` | A scanned PDF. Used in Steps 8 and 10. |
| `not-a-pdf.txt` | A text file the app should reject. Used in Step 8. |

## Microsoft Learn

- [Introduction to Azure Container Registry](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-intro)
- [Create a container registry in the portal](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-get-started-portal)
- [Continuous deployment with GitHub Actions in Container Apps](https://learn.microsoft.com/en-us/azure/container-apps/github-actions)
- [Ingress in Azure Container Apps](https://learn.microsoft.com/en-us/azure/container-apps/ingress-overview)
- [Managed identities in Azure Container Apps](https://learn.microsoft.com/en-us/azure/container-apps/managed-identity)
- [Traffic splitting in Azure Container Apps](https://learn.microsoft.com/en-us/azure/container-apps/traffic-splitting)
- [Authenticate requests to Foundry Tools with Microsoft Entra ID](https://learn.microsoft.com/en-us/azure/ai-services/authentication)
