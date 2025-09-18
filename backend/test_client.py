"""Simple CLI harness to simulate a chat turn using memory + LLM client.

Usage:
  python backend/test_client.py --user tester --text "Hello"
"""

import argparse

from app.services.memory_store import SQLiteMemory
from app.services.llm_client import generate_reply


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--user", required=True)
    parser.add_argument("--text", required=True)
    args = parser.parse_args()

    memory = SQLiteMemory()
    past = memory.search(user_id=args.user, k=5)
    context = [m["text"] for m in past]
    reply = generate_reply(args.text, context_messages=context)
    memory.save(args.user, args.text, {"role": "user"})
    memory.save(args.user, reply, {"role": "assistant"})
    print(reply)


if __name__ == "__main__":
    main()


