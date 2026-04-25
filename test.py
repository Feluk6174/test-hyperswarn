#!/usr/bin/env python3
import sys
import threading
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hyperswarm import HyperswarmInterface

class TestClient:
    def __init__(self):
        self.hs = None
        self.running = True
        self.topic = None

    def start(self):
        print("=== Hyperswarm Chat Test ===")
        print()

        self.topic = input("Enter topic: ").strip()
        if not self.topic:
            print("Topic required!")
            return

        print(f"Connecting to topic: {self.topic}...")
        result = self.hs.create(self.topic)

        if result.get('status') == 'ok':
            print(f"[OK] Connected to swarm")
            print(f"[OK] Topic hash: {self.topic}")
        else:
            print(f"[ERROR] Failed to connect: {result}")
            return

        receiver_thread = threading.Thread(target=self._receive_messages, daemon=True)
        receiver_thread.start()

        print()
        print("=== Commands ===")
        print("s <msg> - Send message")
        print("r        - Try to receive (non-blocking)")
        print("q        - Quit")
        print()

        while self.running:
            try:
                cmd = input("> ").strip()
            except EOFError:
                break

            if not cmd:
                continue

            if cmd == 'q':
                self.running = False
                break

            if cmd.startswith('s '):
                msg = cmd[2:]
                self.hs.send(msg)
                print(f"[SENT] {msg}")
                continue

            if cmd == 'r':
                msg = self.hs.nrecv()
                if msg:
                    print(f"[RECV] {msg}")
                else:
                    print("[EMPTY] No messages")
                continue

            print("Unknown command")

        self.hs.close()
        print("Goodbye!")

    def _receive_messages(self):
        while self.running:
            try:
                msg = self.hs.recv()
                print(f"\n[RECV] {msg}\n> ", end='')
            except Exception as e:
                if self.running:
                    print(f"\n[ERROR] {e}\n> ", end='')


def main():
    client = TestClient()
    client.hs = HyperswarmInterface()
    try:
        client.start()
    except KeyboardInterrupt:
        client.running = False
        client.hs.close()


if __name__ == '__main__':
    main()