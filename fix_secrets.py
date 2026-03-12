import os
from pathlib import Path


def main() -> None:
    bearer_token = os.environ.get("BEARER_TOKEN")
    anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")

    missing = [
        name
        for name, value in {
            "BEARER_TOKEN": bearer_token,
            "ANTHROPIC_API_KEY": anthropic_api_key,
        }.items()
        if not value
    ]
    if missing:
        missing_vars = ", ".join(missing)
        raise SystemExit(f"Set these environment variables before running: {missing_vars}")

    streamlit_dir = Path(".streamlit")
    streamlit_dir.mkdir(exist_ok=True)
    secrets_path = streamlit_dir / "secrets.toml"

    with secrets_path.open("w", encoding="utf-8") as handle:
        handle.write(f'BEARER_TOKEN = "{bearer_token}"\n')
        handle.write(f'ANTHROPIC_API_KEY = "{anthropic_api_key}"\n')

    print(f"Updated {secrets_path} from environment variables.")


if __name__ == "__main__":
    main()
