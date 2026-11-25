# GitHub repository setup

Use the following settings when creating the GitHub repository.

- **Repository name:** `Azure-AI-ML-Cloud-Deployment-Labs`
- **Description:** `24 hands-on Microsoft Azure labs covering AZ-900 fundamentals, Azure AI services, machine learning workflows, deployment, security, governance, and monitoring.`
- **Visibility:** Public (recommended if you have permission to share all included manuals and assets); otherwise choose Private until redistribution rights are confirmed.
- **Initialize with README:** No — this package already contains a README.
- **Add .gitignore:** No — this package already contains one.
- **Choose a license:** Do not add a license until you have confirmed that you own or have permission to license all included material. A license cannot grant rights to third-party content.

## Suggested repository topics

`microsoft-azure` `azure-fundamentals` `az-900` `azure-ai` `azure-machine-learning` `machine-learning` `mlops` `cloud-computing` `devops` `hands-on-labs` `learning-resources` `navttc` `netsol`

## Upload with Git

Run these commands from inside the extracted repository folder after creating the empty GitHub repository:

```bash
git init
git add .
git status
git commit -m "Add Azure fundamentals and AI/ML hands-on labs"
git branch -M main
git remote add origin https://github.com/<YOUR-GITHUB-USERNAME>/Azure-AI-ML-Cloud-Deployment-Labs.git
git push -u origin main
```

Replace `<YOUR-GITHUB-USERNAME>` with your GitHub username. Review `git status` before committing. Do not commit credentials, personal data or files you are not permitted to redistribute.
