from client import PBFTEngine

def main():
    print("=== Testing PBFT Three-Phase Consensus Engine ===")
    pbft = PBFTEngine(node_id=0, f=1)
    pbft.receive_pre_prepare(view=0, seq=1, digest="DIGEST_X")
    pbft.receive_prepare(view=0, seq=1, digest="DIGEST_X", sender_id=1)
    s_prep = pbft.receive_prepare(view=0, seq=1, digest="DIGEST_X", sender_id=2)
    print("Prepare state:", s_prep)
    assert s_prep == "PREPARED"

    pbft.receive_commit(view=0, seq=1, digest="DIGEST_X", sender_id=0)
    pbft.receive_commit(view=0, seq=1, digest="DIGEST_X", sender_id=1)
    s_comm = pbft.receive_commit(view=0, seq=1, digest="DIGEST_X", sender_id=2)
    print("Commit state:", s_comm)
    assert s_comm == "COMMITTED"
    print("=== All tests passed successfully! ===")

if __name__ == "__main__":
    main()
