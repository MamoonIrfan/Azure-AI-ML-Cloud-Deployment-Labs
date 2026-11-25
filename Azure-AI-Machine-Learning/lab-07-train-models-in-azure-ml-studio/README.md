# Lab 7 — Train Models and Build a Pipeline in Azure Machine Learning Studio

In this lab you create an Azure Machine Learning workspace, take a guided tour of Azure Machine Learning studio, and train models in it two ways. First, Automated ML (AutoML) tries several algorithms on a flower dataset and ranks them. Then you build a training pipeline in Designer by dragging components onto a canvas and connecting them. You finish by finding where GPU compute is chosen and why a free account cannot use it. This maps to the syllabus topic **Azure Machine Learning — pipelines, GPU training**. Lab 8 deploys the model you train here.

Run on https://portal.azure.com and https://ml.azure.com — sign in with your Azure free account (https://azure.microsoft.com/free).

> **Before you start:** you need the resource group `rg-ai-w8-labs` in **East US** from Lab 1, and the file `iris.csv` from this lab folder on your computer. Allow about 2 hours. AutoML and Designer jobs take 10–20 minutes each to run, and you can read ahead while they do.

---

## Step 1 — Create the Azure Machine Learning workspace

1. Go to **https://portal.azure.com**. In the search bar type `machine learning` and open **Azure Machine Learning**.
2. Click **+ Create** > **New workspace**.
3. On the **Basics** tab enter:
   - Subscription: your free-account subscription
   - Resource group: `rg-ai-w8-labs`
   - Name: `mlw-ai-w8`
   - Region: `East US`
   - Storage account, Key vault, Application insights: leave the new names the portal suggests
   - Container registry: `None`
4. Click **Review + create**, wait for **Validation passed**, then click **Create**. Deployment takes 2–3 minutes.
5. When it finishes, click **Go to resource**.

A workspace is the top-level container for everything you do in Azure Machine Learning: data, compute, jobs, models and endpoints. It is an Azure resource like any other, so it lives in a resource group and is billed to your subscription. The workspace itself is free. You pay for the compute you run in it and a few cents for storage.

---

## Step 2 — Look at what the workspace created

1. Open `rg-ai-w8-labs` (search **Resource groups**, then click it).
2. Find the resources the workspace created alongside itself:

| Resource type | What the workspace uses it for |
|---|---|
| **Storage account** | Stores uploaded datasets, job outputs, logs and model files |
| **Key vault** | Stores secrets, such as connection strings, so they are not kept in code |
| **Application Insights** | Collects telemetry from deployed endpoints (Lab 8) |
| **Azure Machine Learning workspace** | The workspace itself |

3. Open `mlw-ai-w8` again. On its **Overview** page, note the **Studio web URL** and the **Launch studio** button.

Azure Machine Learning is built from ordinary Azure services. When you upload data in studio, it lands in this storage account. Deleting the resource group in Lab 8 removes all of these together.

---

## Step 3 — Launch studio and tour the navigation

1. Click **Launch studio**. Azure Machine Learning studio opens at https://ml.azure.com with `mlw-ai-w8` selected. The workspace name appears at the top right.
2. If the left menu is collapsed, click the **menu icon** (three lines) at the top left to expand it.
3. Find each area below in the left menu. You use most of them in this lab or the next.

| Menu area | What it is for | Used in |
|---|---|---|
| **Home** | Shortcuts, recent jobs and getting-started links | This step |
| **Notebooks** | Jupyter notebooks that run on a compute instance | Not needed (no code in this lab) |
| **Automated ML** | A form that trains and compares many models for you | Steps 6–8 |
| **Designer** | A drag-and-drop canvas for building pipelines | Steps 10–12 |
| **Data** | Versioned datasets (data assets) and connections to storage | Step 6 |
| **Jobs** | Every training run, its status, metrics, outputs and logs | Steps 7, 8, 12 |
| **Components** | Reusable pipeline steps | Step 10 |
| **Environments** | Docker images and Python packages that jobs run in | Step 8 |
| **Models** | The model registry: named, versioned models | Step 9, Lab 8 |
| **Endpoints** | Deployed models that apps can call | Lab 8 |
| **Compute** | Compute instances, compute clusters and quota | Step 4, Step 13 |
| **Monitoring** | Drift and data-quality monitors for deployed models | Lab 8 |

4. Click the **workspace name** at the top right. Note the panel that shows the subscription, resource group and region, and the link to the workspace in the Azure portal.

The Azure portal manages the workspace as a resource: who can access it, where it runs, and what it costs. Studio is where you do machine learning work inside it. You will move between the two throughout Weeks 7–8.

---

## Step 4 — Create a compute cluster

1. In the left menu click **Compute**. Note the tabs: **Compute instances**, **Compute clusters**, **Serverless Spark** (if shown), **Kubernetes clusters** and **Attached computes**.
2. Click the **Compute clusters** tab, then **+ New**.
3. On the **Virtual machine** page enter:
   - Location: `East US`
   - Virtual machine tier (or priority): `Dedicated`
   - Virtual machine type: `CPU`
   - Virtual machine size: click **Select from all options**, then choose `Standard_D2as_v4` (2 cores, 8 GB RAM). Use the search box to find it.
4. Click **Next**. On the **Advanced settings** page enter:
   - Compute name: `cpu-cluster`
   - Minimum number of nodes: `0`
   - Maximum number of nodes: `1`
   - Idle seconds before scale down: `300`
5. Click **Create**. The cluster appears with **0 nodes** after about a minute.

The three kinds of compute serve different jobs:

| Compute type | What it is | When to use it |
|---|---|---|
| **Compute instance** | One VM for you, with Jupyter and VS Code | Writing and testing code interactively |
| **Compute cluster** | A pool of VMs that scales up when a job is submitted and back to zero when idle | Training jobs and pipelines (this lab) |
| **Serverless compute** | Azure picks and manages the VMs for each job | Jobs where you do not want to manage a cluster |

**Minimum nodes = 0** is the most important setting on this page. With 0, the cluster costs nothing while idle. With 1 or more, at least one VM keeps running and billing even when no job is running.

---

## Step 5 — Look at the dataset

1. On your computer, open `iris.csv` from this lab folder in a text editor or Excel.
2. Note the columns:

| Column | Meaning |
|---|---|
| `sepal_length`, `sepal_width` | Sepal measurements of a flower, in cm |
| `petal_length`, `petal_width` | Petal measurements, in cm |
| `target` | The species: `0` = setosa, `1` = versicolor, `2` = virginica |

3. Count the rows: 120 flowers, 40 of each species.

The model must predict `target` from the four measurements. This is a **multi-class classification** task. The dataset is small and familiar on purpose, so that the lab can focus on the Azure tooling rather than on the data.

---

## Step 6 — Start an Automated ML job and upload the data

1. In studio, click **Automated ML** in the left menu, then **+ New Automated ML job**.
2. On **Training method**, select **Train automatically**, then click **Start configuring job**.
3. On **Basic settings** enter:
   - Job name: leave the generated name
   - Experiment name: click **Create new** and enter `iris-automl`
4. Click **Next**. On **Task type & data**, set **Select task type** to `Classification`.
5. Under the data list, click **Create** to upload a new data asset, and work through the wizard:
   - **Data type**: Name `iris-training`, Type `Tabular`. Click **Next**.
   - **Data source**: `From local files`. Click **Next**.
   - **Destination storage type**: `Azure Blob Storage`, datastore `workspaceblobstore`. Click **Next**.
   - **File and folder selection**: click **Upload files or folder** > **Upload files**, choose `iris.csv`, then click **Next**.
   - **Settings**: File format `Delimited`, Delimiter `Comma`, Encoding `UTF-8`, Column headers `Only first file has headers`. Check that the preview shows five separate columns. Click **Next**.
   - **Schema**: leave all five columns included. Click **Next**, then **Create**.
6. Back on **Task type & data**, select `iris-training` in the list and click **Next**.

A **data asset** is a named, versioned pointer to data in the workspace's storage account. Jobs refer to `iris-training:1` instead of a file on your laptop, so anyone in the workspace can rerun the job on exactly the same data. Open **Data** later and you will find it listed there.

---

## Step 7 — Configure the task, limits and compute, then submit

1. On **Task settings**, set **Target column** to `target`.
2. Click **View additional configuration settings** and set:
   - Primary metric: `Accuracy`
   - Enable ensemble stacking: unticked
   - Explain best model: ticked
   - Click **Save**.
3. Expand **Limits** and set:
   - Max trials: `6`
   - Max concurrent trials: `1`
   - Experiment timeout (minutes): `30`
4. Expand **Validate and test** and set:
   - Validation type: `k-fold cross validation`
   - Number of cross validations: `5`
5. Click **Next**. On **Compute**, set **Select compute type** to `Compute cluster` and choose `cpu-cluster`.
6. Click **Next**, review the summary, then click **Submit training job**.
7. The job's details page opens with status **Not started** or **Running**. Leave it open.

The limits keep the experiment small and cheap: 6 trials, one at a time, on one 2-core node. **Primary metric** is the score AutoML uses to rank candidate models. **5-fold cross-validation** splits the 120 rows into five parts. Each model trains on four parts and is scored on the fifth, five times over. With so little data, this gives a more reliable score than a single train/test split.

---

## Step 8 — Watch the job and inspect the results

The job takes 15–25 minutes. The first few minutes are spent starting a node and building the environment.

1. On the job page, open each tab while it runs:
   - **Overview**: status, compute, data, and the **Best model summary** once a trial finishes
   - **Data guardrails**: AutoML's automatic checks, such as class balance and missing values
   - **Models + child jobs**: one row per algorithm tried, ranked by accuracy
   - **Outputs + logs**: log files from the job
2. In another tab, open **Compute** > **Compute clusters** > `cpu-cluster` and watch the node count go from 0 to 1.
3. When the status is **Completed**, open **Models + child jobs**. Note the algorithm names (for example `LogisticRegression`, `LightGBM`, `RandomForest`) and their accuracy.
4. Click the top **Algorithm name** and open its **Metrics** tab. Select `confusion_matrix` and read it: rows are the true species, columns are the predicted species.
5. Open the **Explanations (preview)** tab, then **Aggregate feature importance**. Note which measurements matter most.
6. On the parent job's **Overview**, find the **Environment** link. Click it to see the curated environment (Docker image and Python packages) that AutoML used.

Every trial is a separate **child job** with its own metrics and logs, so you can compare algorithms side by side without writing any code. Feature importance shows which inputs the model relied on. It does not show that a measurement *causes* the species.

---

## Step 9 — Register the best model

1. In the left menu click **Models**, then **+ Register** > **From a job output**.
2. Select the AutoML job you just ran, then select the **best child job** (the top row from Step 8). Click **Next**.
3. Select the output named `mlflow-model` (or similar). Set **Model type** to `MLflow` and click **Next**.
4. On **Model settings** enter:
   - Name: `iris-classifier`
   - Description: `AutoML best model, Lab 7`
5. Click **Next**, then **Register**.
6. Open **Models** > `iris-classifier`. Note **Version 1** and the **Job (lineage)** link back to the training job.

The model registry turns an output file into a named, versioned asset. Lab 8 deploys `iris-classifier:1`. If you retrain and register again under the same name, it becomes version 2, and the lineage link always tells you which job and data produced each version.

---

## Step 10 — Open Designer and start a pipeline

1. In the left menu click **Designer**.
2. Under **Classic prebuilt**, click **Create a new pipeline using classic prebuilt components**. A blank canvas opens with the asset library on the left.
3. Click the **pencil icon** next to the default name and rename the pipeline `automobile-price-pipeline`.
4. Look at the asset library tabs: **Data** (your data assets), **Component** (prebuilt steps grouped by category, such as Data Transformation, Machine Learning Algorithms, Model Training and Model Scoring & Evaluation).

A **pipeline** is a training workflow broken into steps, where each step's output feeds the next. Unlike the AutoML job, which runs as one unit, every step here is a separate job you can inspect and rerun. Designer also has a **Custom** mode for steps your team writes in code. This lab uses the classic prebuilt steps because they need no code.

---

## Step 11 — Build the pipeline on the canvas

In the asset library, search each component by name and drag it onto the canvas, top to bottom. Connect them by dragging from the small circle at the bottom of one box (output port) to the circle at the top of the next (input port).

1. **Automobile price data (Raw)** (under **Component** > **Sample data**): a built-in dataset of cars and their prices.
2. **Select Columns in Dataset**: connect the data to it. Click the box, click **Edit column** in the right pane, choose **All columns**, then add an **Exclude** rule for `normalized-losses` (a column with many missing values). Click **Save**.
3. **Clean Missing Data**: connect it below. In the right pane, set **Columns to be cleaned** to all columns and **Cleaning mode** to `Remove entire row`.
4. **Split Data**: connect the left output (**Cleaned dataset**) of Clean Missing Data to it. Set **Fraction of rows in the first output dataset** to `0.7`.
5. **Linear Regression**: drag it beside Split Data. Leave its defaults.
6. **Train Model**: connect **Linear Regression** to its left input and the **left** output of Split Data to its right input. Click **Edit column** under **Label column** and enter `price`.
7. **Score Model**: connect **Train Model** to its left input and the **right** output of Split Data to its right input.
8. **Evaluate Model**: connect **Score Model** to its left input.

When you finish, every box should have no red warning icon. The flow reads: data > select columns > clean > split 70/30 > train on 70% > score the other 30% > evaluate.

The 30% of rows the model never sees in training is your test set. **Score Model** predicts a price for each of those cars, and **Evaluate Model** compares the predictions with the real prices.

---

## Step 12 — Submit the pipeline and inspect each step

1. Click **Configure & Submit** at the top right.
2. On **Basics**, choose **Create new** experiment and enter `automobile-pipeline`. Click **Next**.
3. On **Inputs & outputs**, click **Next**.
4. On **Runtime settings**, set **Select compute type** to `Compute cluster` and choose `cpu-cluster`. Click **Next**.
5. On **Review + Submit**, click **Submit**. Click the job link in the notification.
6. Watch the graph. Each box turns blue while it runs and green when it completes. The whole pipeline takes about 10–15 minutes.
7. When it completes, right-click **Score Model** > **Preview data** > **Scored dataset**. Compare the `price` column with the `Scored Labels` column.
8. Right-click **Evaluate Model** > **Preview data** > **Evaluation results**. Note the **Mean Absolute Error** and the **Coefficient of Determination** (R²).
9. Double-click any box and open **Outputs + logs** to see that step's own log files.

| Metric | What it means |
|---|---|
| **Mean Absolute Error** | The average size of a prediction error, in dollars. Lower is better |
| **Coefficient of Determination (R²)** | The share of price variation the model explains. 1.0 is perfect; 0 means no better than predicting the average |

Because each step is a separate job, Azure Machine Learning can reuse the output of steps that have not changed. Submit the pipeline again and the unchanged steps finish almost instantly. This is one reason teams use pipelines for repeatable training.

---

## Step 13 — Find GPU compute and check your quota

1. Open **Compute** > **Compute clusters** > **+ New**.
2. Set **Virtual machine type** to `GPU` and click **Select from all options**.
3. Look at the GPU sizes listed, for example the **NC** (training and inference) and **ND** (large-scale training) families. Note their GPU type, GPU count and price per hour.
4. Note the quota message next to the sizes. On a free account, GPU families have a quota of **0 cores**, so they cannot be created. Click **Cancel**.
5. In the Azure portal, open `mlw-ai-w8` and click **Usage + quotas** in the left menu. Compare your CPU family quota (for example **Standard DASv4 Family vCPUs**) with the GPU families.

| | CPU | GPU |
|---|---|---|
| **Good at** | General processing, small tabular models like the ones in this lab | Thousands of parallel calculations: deep learning, image and language models |
| **Example size** | `Standard_D2as_v4`: 2 cores, about USD 0.10/hour | NC-series with one NVIDIA GPU: several USD/hour |
| **Free account** | Small quota available | Quota is 0; needs a pay-as-you-go subscription and a quota request |

You do not need a GPU for anything in this lab: a linear model on 120 rows trains in seconds on a CPU. GPUs matter when you train neural networks, such as image classifiers and object detectors. For those, you would choose a GPU size in the same cluster form, after Microsoft approves a quota increase.

---

## Clean up

1. Open **Compute** > **Compute clusters** and confirm `cpu-cluster` shows **0** nodes (it scales down automatically 5 minutes after the last job).
2. If you created a compute instance while exploring, select it and click **Stop**, then **Delete**.
3. **Keep** the workspace `mlw-ai-w8`, the cluster and the model `iris-classifier`. Lab 8 deploys this model. A cluster with 0 nodes costs nothing.

## What you learned

- An Azure Machine Learning workspace is an Azure resource that brings its own storage account, key vault and Application Insights.
- How to find your way around studio: Data, Compute, Automated ML, Designer, Jobs, Components, Environments, Models and Endpoints.
- Compute instances are for interactive work and compute clusters are for jobs. Minimum nodes = 0 keeps an idle cluster free.
- Automated ML trains and ranks many algorithms from a form, with each trial recorded as a child job with metrics and explanations.
- The model registry stores named, versioned models linked to the job that produced them.
- A Designer pipeline splits training into separate steps (prepare, split, train, score, evaluate) that you can inspect and rerun individually.
- GPUs speed up deep learning, and their quota starts at zero, so they need planning and a paid subscription.

---

## Files in this lab folder

| File | What it is |
|------|------------|
| `iris.csv` | 120 flower measurements with species labels. Upload it in Step 6. |

## Microsoft Learn

- [Create workspace resources](https://learn.microsoft.com/en-us/azure/machine-learning/quickstart-create-resources)
- [Create a compute cluster](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-create-attach-compute-cluster)
- [Set up no-code AutoML training in studio](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-use-automated-ml-for-ml-models)
- [Create data assets](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-create-data-assets)
- [Manage models in the registry](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-manage-models)
- [What is Designer?](https://learn.microsoft.com/en-us/azure/machine-learning/concept-designer)
- [Manage and increase quotas](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-manage-quotas)
- [Learning path: Operationalize machine learning models (DP-100)](https://learn.microsoft.com/en-us/training/paths/explore-azure-machine-learning-workspace/)
