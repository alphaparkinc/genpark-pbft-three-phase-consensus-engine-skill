class PBFTEngine:
    """
    PBFT Three-Phase Consensus Engine tolerating up to f Byzantine faults
    within a network of 3f+1 replicas.
    """
    def __init__(self, node_id, f=1):
        self.node_id = node_id
        self.f = f
        self.quorum_size = 2 * f + 1
        self.pre_prepares = {}
        self.prepares = {}
        self.commits = {}
        self.committed_blocks = {}

    def receive_pre_prepare(self, view, seq, digest):
        self.pre_prepares[(view, seq)] = digest
        return self.receive_prepare(view, seq, digest, self.node_id)

    def receive_prepare(self, view, seq, digest, sender_id):
        key = (view, seq, digest)
        if key not in self.prepares:
            self.prepares[key] = set()
        self.prepares[key].add(sender_id)
        if len(self.prepares[key]) >= self.quorum_size:
            return "PREPARED"
        return "WAITING_PREPARE"

    def receive_commit(self, view, seq, digest, sender_id):
        key = (view, seq, digest)
        if key not in self.commits:
            self.commits[key] = set()
        self.commits[key].add(sender_id)
        if len(self.commits[key]) >= self.quorum_size:
            self.committed_blocks[seq] = digest
            return "COMMITTED"
        return "WAITING_COMMIT"
