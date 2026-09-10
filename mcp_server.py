import sys
import json
from client import PBFTEngine

def main():
    engine = PBFTEngine(node_id=0, f=1)
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        req = json.loads(line)
        method = req.get("method")
        params = req.get("params", {})
        if method == "pre_prepare":
            res = {"status": engine.receive_pre_prepare(params.get("view", 0), params.get("seq", 1), params.get("digest"))}
        elif method == "prepare":
            res = {"status": engine.receive_prepare(params.get("view", 0), params.get("seq", 1), params.get("digest"), params.get("sender_id"))}
        elif method == "commit":
            res = {"status": engine.receive_commit(params.get("view", 0), params.get("seq", 1), params.get("digest"), params.get("sender_id"))}
        else:
            res = {"error": "unknown method"}
        sys.stdout.write(json.dumps({"id": req.get("id"), "result": res}) + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
