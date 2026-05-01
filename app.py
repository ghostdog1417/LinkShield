from __future__ import annotations


def main() -> int:
    print(
        "LinkShield has been migrated to a React frontend with a Flask backend.\n"
        "Run the new app with:\n"
        "  1. cd backend && python app.py\n"
        "  2. cd frontend && npm start\n"
        "See DEPLOY_COMPLETE.md for hosting instructions."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())