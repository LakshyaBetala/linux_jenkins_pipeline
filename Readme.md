Perfect ✅ — here’s a **complete, professional `README.md`** for your Jenkins + Podman Flask CI/CD demo project.

It includes:

* Overview
* Architecture diagram (text-based)
* Step-by-step setup & demo instructions
* Commands for deployment, rollback, troubleshooting
* Demo flow description

---

```markdown
# 🚀 Flask CI/CD Pipeline with Jenkins & Podman

This project demonstrates a **complete CI/CD pipeline** for a Flask application using **Jenkins**, **Podman**, and a **local container registry** — all running locally under WSL or Linux.

The pipeline automates:
1. Running unit tests (with pytest)
2. Building a container image using Podman
3. Pushing it to a local container registry
4. Deploying the updated container automatically

---

## 🧠 Project Overview

**Tech Stack**
- **Flask** – Python web framework  
- **pytest** – Testing framework  
- **Jenkins** – CI/CD automation  
- **Podman** – Container engine (Docker alternative)  
- **Local Registry** – Image storage (`localhost:5000`)  

**Pipeline Flow**

```

Developer Commit (GitHub)
↓
Jenkins (CI/CD)
├── Checkout Source
├── Run Unit Tests (pytest)
├── Build Podman Image
├── Push to Local Registry
└── Deploy New Container on Port 5001

```

---

## 📁 Project Structure

```

flask-ci-demo/
├── app/
│   ├── **init**.py
│   └── main.py           # Flask entrypoint
├── tests/
│   └── test_sample.py    # pytest test case
├── requirements.txt       # Python dependencies
├── Dockerfile             # Podman build configuration
└── Jenkinsfile            # Jenkins pipeline definition

````

---

## ⚙️ Setup Instructions

### 1️⃣ Prerequisites
Make sure you have the following installed:
```bash
sudo apt install -y python3 python3-venv podman git jq
````

**Jenkins**

```bash
sudo systemctl enable --now jenkins
sudo systemctl status jenkins
```

Access Jenkins UI → [http://localhost:8080](http://localhost:8080)

---

### 2️⃣ Setup Local Registry

```bash
sudo /usr/bin/podman run -d --name registry -p 5000:5000 docker.io/library/registry:2
```

Verify:

```bash
curl -s http://localhost:5000/v2/_catalog | jq .
```

---

### 3️⃣ Clone Repository

```bash
git clone https://github.com/LakshyaBetala/linux_jenkins_pipeline.git
cd linux_jenkins_pipeline
```

---

### 4️⃣ Configure Jenkins Job

1. Create a new **Pipeline job** named `flask-ci-podman-pipeline`.
2. Under **Pipeline → Definition → Pipeline script from SCM**

   * SCM: `Git`
   * Repository URL: `https://github.com/LakshyaBetala/linux_jenkins_pipeline`
   * Branch: `main`
3. Add GitHub credentials (PAT or SSH key).
4. Save and build once manually to verify.

---

## 🧩 Jenkinsfile (Pipeline Breakdown)

| Stage           | Description                                      |
| --------------- | ------------------------------------------------ |
| **Checkout**    | Clones repository from GitHub                    |
| **Test**        | Runs pytest inside a virtual environment         |
| **Build Image** | Builds Flask app image via Podman                |
| **Push Image**  | Pushes to local registry (`localhost:5000`)      |
| **Deploy**      | Stops old container, runs new one on port `5001` |

---

## ▶️ Running the Demo (Step-by-Step)

### Step 1 — Start Jenkins & Registry

```bash
sudo systemctl start jenkins
sudo /usr/bin/podman start registry
```

### Step 2 — Ensure Port 5001 is Free

```bash
sudo ss -ltnp | grep ':5001' || true
sudo /usr/bin/podman rm -f myflask-staging myflask-dev || true
```

### Step 3 — Make a Small Code Change

```bash
cd /mnt/c/Users/laksh/projects/flask-ci-demo/flask-app
git add app/main.py
git commit -m "demo: updated greeting message"
git push origin main
```

### Step 4 — Trigger Jenkins Build

* Jenkins automatically detects push (via webhook or manual **Build Now**)
* Watch the build console

### Step 5 — Verify Deployment

```bash
sudo /usr/bin/podman ps --filter name=myflask-staging
sudo /usr/bin/podman logs --tail 20 myflask-staging
curl http://localhost:5001
```

✅ You should see:

```
{"message": "Hello from Flask via Podman - demo ..."}
```

---

## 🔁 Rollback (Optional)

To roll back to a previous image:

```bash
sudo /usr/bin/podman rm -f myflask-staging
sudo /usr/bin/podman run -d --name myflask-staging -p 5001:5000 localhost:5000/myflask:<old-tag>
```

---

## 🧹 Cleanup After Demo

```bash
sudo /usr/bin/podman rm -f myflask-staging registry || true
sudo /usr/bin/podman rmi localhost:5000/myflask:*
```

---

## 🧪 Troubleshooting

| Issue                         | Cause                             | Fix                                                     |
| ----------------------------- | --------------------------------- | ------------------------------------------------------- |
| `Port 5001 already in use`    | Old container not removed         | `sudo podman rm -f myflask-staging`                     |
| `cannot find subuid ranges`   | Podman rootless mapping issue     | Use `sudo /usr/bin/podman` or `podman system migrate`   |
| `Jenkins build fails at Test` | pytest error                      | Run `PYTHONPATH=. pytest -q` locally                    |
| `Webhook not triggered`       | GitHub → Jenkins connection issue | Use `ngrok http 8080` for local webhook or manual build |

---

## 📸 Demo Flow Summary

| Step | Action                   | What to Show                                |
| ---- | ------------------------ | ------------------------------------------- |
| 1    | Edit code & push         | GitHub commit                               |
| 2    | Jenkins pipeline runs    | Jenkins UI Console Output                   |
| 3    | Podman builds image      | Logs with build stages                      |
| 4    | Image pushed to registry | `curl localhost:5000/v2/_catalog`           |
| 5    | Container deployed       | `curl localhost:5001` shows updated message |

---

## 🧭 Future Enhancements

* Add blue-green deployment
* Integrate GitHub webhooks via ngrok
* Deploy to Kubernetes using Jenkins agents
* Add email or Slack notifications
* Automate rollback on failed test

---

## 👨‍💻 Author

**Lakshya Betala**
Flask + CI/CD + Podman + Jenkins Pipeline Demo
📍 SRM Hackathon / Project Expo Winner 🏆
💻 LinkedIn / GitHub: [LakshyaBetala](https://github.com/LakshyaBetala)

---

## 📜 License

MIT License © 2025 Lakshya Betala

```

---

Would you like me to:
1. ✅ **Generate this `README.md` file and add it directly to your repo folder** (so you can commit it),  
or  
2. 📄 **Include diagrams (architecture + pipeline flow)** in Markdown (mermaid syntax or PNG version) for the README?
```
