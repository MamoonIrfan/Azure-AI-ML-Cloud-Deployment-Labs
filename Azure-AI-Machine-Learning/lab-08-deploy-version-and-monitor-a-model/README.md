# Lab 8 — Deploy, Version and Monitor a Model

In this final lab you take the flower classifier you trained in Lab 7 and run it the way production teams do. You deploy it to a managed online endpoint and test it, then register a second version and deploy it beside the first (a **blue/green** deployment). You send it a share of the traffic and roll back. Then you look at the endpoint's metrics and logs, walk through model monitoring for drift, and schedule a pipeline to retrain. You finish with an overview of CI/CD and optimization, and the full course clean-up. This maps to the syllabus topic **MLOps and deployment — CI/CD, versioning, endpoints, monitoring, retraining, optimization (overview)**.

Run on https://ml.azure.com and https://portal.azure.com — sign in with your Azure free account (https://azure.microsoft.com/free).

> **Before you start:** you need the workspace `mlw-ai-w8`, the completed AutoML job and Designer pipeline, and the registered model `iris-classifier` version 1 from Lab 7. You also need `sample-request.json` and `sample-expected.json` from this lab folder. Allow about 2 hours. Endpoints are billed every hour they exist, so do the clean-up at the end even if you finish early.

---

## Step 1 — Check your quota before deploying

1. In the Azure portal, open `mlw-ai-w8` and click **Usage + quotas** in the left menu (under **Support + troubleshooting** or **Settings**).
2. Find **Standard FSv2 Family vCPUs** and note how many are available, and the **Total Regional vCPUs** limit.
3. Compare with what this lab needs:

| Deployment | VM size | Instances | vCPUs reserved |
|---|---|---|---|
| `blue` (Step 4) | `Standard_F2s_v2` (2 cores, 4 GB) | 1 | 4 |
| `green` (Step 8) | `Standard_F2s_v2` | 1 | 4 |
| **Total** | | | **8** |

A managed online endpoint reserves about 20% extra capacity for upgrades, so one 2-core instance reserves 4 vCPUs. If your free account has fewer than 8 available, do Steps 1–7 and 9–14 yourself and follow Step 8 on your instructor's screen.

---

## Step 2 — Inspect the model you will deploy

1. Go to **https://ml.azure.com** and select the workspace `mlw-ai-w8`.
2. Click **Models** > `iris-classifier`. On the **Details** tab, note the **Version** (1), **Type** (MLflow) and the **Job** link back to the AutoML job.
3. Open the **Artifacts** tab. Open the `MLmodel` file and find its `signature`: the four input columns and one output.
4. Note the `conda.yaml` and `requirements.txt` files: the Python packages the model needs.

Because the model is in **MLflow** format, it carries its own description of its inputs and its environment. Azure Machine Learning can therefore deploy it without a scoring script; this is called **no-code deployment**.

---

## Step 3 — Start the deployment wizard

1. On the `iris-classifier` page, click **Deploy** > **Real-time endpoint**.
2. In the pane that opens, click **More options** to open the full wizard.
3. On the **Endpoint** page enter:
   - Endpoint name: `iris-<suffix>` (must be unique in East US)
   - Compute type: `Managed`
   - Authentication type: `Key-based authentication`
4. Click **Next**. On the **Model** page, check that `iris-classifier` version `1` is selected. Click **Next**.

An **endpoint** is a stable URL that apps call. A **deployment** is a model version running on compute behind that URL. One endpoint can hold several deployments, which is how you swap versions without changing the URL your apps use.

---

## Step 4 — Configure and create the `blue` deployment

1. On the **Deployment** page enter:
   - Deployment name: `blue`
   - Application Insights diagnostics: **Enabled**
   - Data collection (inferencing data collection): **Enabled**
2. Click **Next**. On **Code + environment**, leave **Customize environment and scoring script** off (MLflow models need neither).
3. Click **Next**. On **Compute**, set **Virtual machine** to `Standard_F2s_v2` and **Instance count** to `1`.
4. Click **Next**. On **Live traffic**, check that `blue` gets **100%**.
5. Click **Next**, review the summary, and click **Create**.
6. Click **Endpoints** in the left menu and open `iris-<suffix>`. The deployment takes 10–15 minutes; wait until **Provisioning state** is **Succeeded**.

**Application Insights diagnostics** sends request metrics and failures to the Application Insights resource that Lab 7 created with the workspace. **Data collection** saves every request and prediction as a data asset, which model monitoring needs in Step 11.

---

## Step 5 — Tour the endpoint page

Open each tab on the `iris-<suffix>` page:

| Tab | What it shows |
|---|---|
| **Details** | The REST endpoint URL, status, deployments with their traffic share, and the **Update traffic** and **Add deployment** buttons |
| **Test** | A form for sending a JSON request to a chosen deployment |
| **Consume** | The REST URL, the authentication keys and sample code for calling the endpoint from an app |
| **Monitoring** | Request, latency and error charts |
| **Logs** | The container logs of each deployment |

---

## Step 6 — Test the endpoint

1. Open the **Test** tab and select the deployment `blue`.
2. Open `sample-request.json` from this lab folder, copy its contents, and paste them into the **Input** box.
3. Click **Test**. The result is a list of three predictions.
4. Compare the result with `sample-expected.json`: `[0, 1, 2]`, meaning setosa, versicolor and virginica.
5. Change the first flower's `petal_length` from `1.5` to `5.5` and test again. Note how the prediction changes.

The request lists the column names and one row of values per flower, matching the model's signature. The model saw none of these flowers in training: they come from a held-out set.

---

## Step 7 — Look at how an app would call the endpoint

1. Open the **Consume** tab.
2. Note the **REST endpoint** URL, the **Primary key** and **Secondary key**, and the sample code (for example Python or C#).
3. Compare it with the Container Apps URL from Lab 4:

| | Container Apps (Lab 4) | Managed online endpoint (this lab) |
|---|---|---|
| **Runs** | Your whole application, any container | One machine learning model |
| **You provide** | A container image | A registered model (and, for non-MLflow models, a scoring script and environment) |
| **Scaling** | Scale to zero, HTTP rules | Instance count, or autoscale rules; no scale to zero |
| **Versioning** | Revisions | Deployments behind one endpoint |
| **Typical use** | The app the student uses | The prediction service the app calls |

In a full solution, the app in Container Apps would call this endpoint with a key or managed identity. Keep the key secret: store it in Key Vault as you did in Lab 2.

---

## Step 8 — Register version 2 and deploy it as `green`

1. Click **Jobs**, open the `iris-automl` experiment and its AutoML job, then the **Models + child jobs** tab. Note the **second-best** model.
2. Click **Models** > **+ Register** > **From a job output**. Select the AutoML job, then the second-best child job, then its `mlflow-model` output, and set **Model type** to `MLflow`.
3. On **Model settings**, enter the Name `iris-classifier` (the same name) and the Description `Second-best AutoML candidate, Lab 8`. Click **Register**.
4. Open **Models** > `iris-classifier`. Note that it now has **Version 2**; use the version list to switch between them.
5. Open the endpoint `iris-<suffix>` > **Details** > **+ Add deployment**.
6. Select the model `iris-classifier` version `2`, name the deployment `green`, enable Application Insights diagnostics, choose `Standard_F2s_v2` with `1` instance, and keep live traffic at **0%** for green.
7. Click **Create** and wait until `green` is **Succeeded**.
8. On the **Test** tab, select `green` and send `sample-request.json`. Compare its result with `blue`.

In a real project, version 2 comes from retraining on newer data, but the mechanics are the same. Registering under the same name creates a new **version**, and both stay linked to the jobs that produced them. The new deployment gets **0% traffic**, so you can test it directly before any user reaches it.

---

## Step 9 — Shift traffic, then roll back

1. On the **Details** tab, click **Update traffic**.
2. Set `blue` to `90` and `green` to `10`, then click **Update**. Ten percent of requests now go to version 2. This is a **canary release**.
3. Click **Update traffic** again and look at **Enable mirrored traffic**. Read the option: it copies a share of live traffic to a deployment without returning its answers to users. Do not enable it.
4. Imagine the monitoring shows that `green` makes more errors. Roll back: click **Update traffic**, set `blue` to `100` and `green` to `0`, and click **Update**.
5. Delete `green`: on its deployment card, click the **delete (trash)** icon and confirm.

| Release technique | What happens | Risk if the new version is bad |
|---|---|---|
| **Replace** | All traffic moves to the new version at once | Every user is affected |
| **Canary** (90/10) | A small share of real users get the new version | Only that share is affected, and rollback is one click |
| **Mirror (shadow)** | The new version receives a copy of traffic, but users only see the old version's answers | No users are affected |

The Test tab sends requests to the deployment you pick, so it ignores the traffic split. The split applies to apps calling the endpoint URL.

---

## Step 10 — Read the metrics and logs

1. On the endpoint page, open the **Monitoring** tab. Look at **Requests per minute** and **Request latency** for the test calls you made. (Charts can take 5–10 minutes to show new data.)
2. On the **Details** tab, click **View metrics** to open the same data in Azure Monitor in the portal. Change the metric to **Request Latency** and the time range to the last hour.
3. In Azure Monitor, click **New alert rule** and look at the form: you could email yourself when latency or errors pass a threshold. Close it without creating.
4. Back in studio, open the **Logs** tab, select the deployment `blue`, and read the container log, including the lines for each scoring request.

**Operational monitoring** answers *is the service healthy?*: requests, latency, errors, CPU and memory. It does not tell you whether the predictions are still correct. That is the job of model monitoring.

---

## Step 11 — Walk through model monitoring

1. In studio, click **Monitoring** in the left menu, then **+ Add**.
2. On **Basic settings**, select the model `iris-classifier`, then the deployment `blue` (it appears because you enabled data collection). Look at the other fields: **Select training data**, **Monitor name**, **Virtual machine size** and **Recurrence**.
3. Click **Next** through the pages and look at **Select monitoring signals**. Note the signals:

| Signal | What it detects | Example |
|---|---|---|
| **Data drift** | The inputs have changed compared with the training data | Students now send flowers from a different region with larger petals |
| **Prediction drift** | The distribution of predictions has changed | The model suddenly predicts `virginica` twice as often |
| **Data quality** | Missing values, wrong types or out-of-range inputs | `petal_length` arrives empty or negative |

4. Click **Cancel**. Monitors run on serverless Spark compute, which costs extra, so you do not create one in this lab.
5. Click **Data** in the left menu. Find the data assets that data collection created, named `iris-<suffix>-blue-model_inputs` and `-model_outputs`, and open one to see your test requests.

A model that was accurate when trained can slowly become wrong as the world changes. Monitoring compares production data with training data on a schedule and sends an alert when they diverge. The response is to investigate, and if needed retrain and release a new version through Steps 8–9, with a person approving it first.

---

## Step 12 — Schedule the training pipeline to retrain

1. Click **Jobs**, open the `automobile-pipeline` experiment from Lab 7, and open the completed pipeline job.
2. Click **Schedule** > **Create new schedule**.
3. On **Basic settings** enter:
   - Name: `weekly-retrain`
   - Trigger: `Recurrence`, every `1` `Week`, on `Monday` at `02:00`
   - Start: next Monday
4. Click **Review + Create**, then **Create**.
5. Click **Jobs** > **All schedules** and open `weekly-retrain`. Note the **Overview**, **Job definition** and **Jobs history** tabs.
6. Select `weekly-retrain`, click **Disable**, then **Delete**, so it does not run after the course.

A schedule reruns the same pipeline on new data at fixed times. Combined with monitoring, this is the **retraining** loop: monitor, detect drift, retrain on recent data, evaluate, register a new version, release it with a canary and roll back if needed.

---

## Step 13 — CI/CD for machine learning (overview)

Read how the pieces you used in Labs 4, 7 and 8 fit into one automated MLOps process:

| Stage | What happens | Where you saw it |
|---|---|---|
| **Source control** | Training code, pipeline definitions and environments live in Git | GitHub repository (Lab 4) |
| **Continuous integration** | Each commit runs tests and validates the code | GitHub Actions workflow (Lab 4) |
| **Training pipeline** | The pipeline trains and evaluates a model on versioned data | Designer pipeline, data asset (Lab 7) |
| **Registration** | A model that passes evaluation is registered as a new version | Model registry (Labs 7–8) |
| **Approval** | A person reviews the metrics and approves the release | Step 9 decision |
| **Continuous deployment** | A workflow deploys the new version with a small traffic share | Blue/green deployment (Step 8) |
| **Monitoring** | Metrics, logs and drift signals are watched | Steps 10–11 |
| **Retraining** | A schedule or a drift alert starts the training pipeline again | Step 12 |

Microsoft's **MLOps v2 solution accelerator** provides ready-made GitHub Actions and Azure DevOps templates for these stages. In those templates, every step you clicked through in this lab runs as code on each commit.

---

## Step 14 — Optimization (overview)

When a deployed model is too slow, too expensive or not accurate enough, these are the main levers:

| Goal | Lever | Trade-off |
|---|---|---|
| Lower cost | Smaller VM size, fewer instances, delete idle deployments, batch endpoints for non-urgent work | Less headroom for traffic peaks |
| Lower latency | Larger VM size, more instances, a smaller or simpler model | Higher cost, or possibly lower accuracy |
| Handle load | Autoscale rules on instance count | Pay for extra instances during peaks |
| Higher accuracy | More and better training data, a larger AutoML search, better features | Longer training, more compute |
| Smaller model | Choose a simpler algorithm, or quantize or prune a neural network | Possibly lower accuracy |

Measure first. Use the latency and cost data from Step 10 and the accuracy from Lab 7 to decide which lever to pull.

---

## Clean up (full course clean-up)

1. In studio, open **Endpoints**, select `iris-<suffix>` and click **Delete**. This removes its deployments and stops the hourly charge.
2. Open **Compute** and confirm there are no running compute instances and that `cpu-cluster` shows 0 nodes.
3. In the Azure portal, open **Resource groups** > `rg-ai-w8-labs` and click **Delete resource group**. Type the name to confirm and click **Delete**. This removes everything from Labs 1–8: the Foundry resource and project, key vault, Container Apps environment, storage account, search service and Machine Learning workspace.
4. Open **Key vaults** > **Manage deleted vaults** and purge `kv-ai-w8-<suffix>` if you want to free its name now (otherwise it is purged automatically after 7 days).
5. Open **Cost Management** > **Cost analysis** over the next day to confirm that charges have stopped.
6. Optional: delete the `contoso-docreader` repository on GitHub if you have not already.

## What you learned

- How to deploy an MLflow model to a managed online endpoint without a scoring script, and how endpoints differ from deployments.
- How to test an endpoint in studio and find what an app needs to call it.
- How model versions work in the registry, and how a blue/green deployment releases a new version safely with canary traffic, mirroring and rollback.
- The difference between operational monitoring (requests, latency, errors) and model monitoring (data drift, prediction drift, data quality).
- How a scheduled pipeline supports retraining, and how CI/CD automates the whole MLOps lifecycle.
- The main levers for optimizing cost, latency and accuracy.

---

## Files in this lab folder

| File | What it is |
|------|------------|
| `sample-request.json` | Three held-out flowers in the request format for the MLflow endpoint. Used in Steps 6 and 8. |
| `sample-expected.json` | The correct species for those three flowers. |

## Microsoft Learn

- [Deploy MLflow models to online endpoints](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-deploy-mlflow-models-online-endpoints)
- [Deploy a model to an online endpoint](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-deploy-online-endpoints)
- [Safe rollout for online endpoints](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-safely-rollout-online-endpoints)
- [Managed online endpoint VM sizes](https://learn.microsoft.com/en-us/azure/machine-learning/reference-managed-online-endpoints-vm-sku-list)
- [Monitor online endpoints](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-monitor-online-endpoints)
- [Model monitoring concepts](https://learn.microsoft.com/en-us/azure/machine-learning/concept-model-monitoring)
- [Schedule a pipeline job](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-schedule-pipeline-job)
- [Set up MLOps with GitHub](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-setup-mlops-github-azure-ml)
- [Learning path: Operationalize machine learning models (DP-100)](https://learn.microsoft.com/en-us/training/paths/deploy-consume-models-azure-machine-learning/)
