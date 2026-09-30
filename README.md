# Failover Pulse

Health probes, failover, alerts. One failed sample does not flip a target.

```
src/backend   :8060
src/frontend  :3060
```

```bash
cd ~/failover-pulse/src/backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8060
```
