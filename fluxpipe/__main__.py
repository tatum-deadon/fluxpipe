"""CLI entry point."""

import argparse


def main():
    parser = argparse.ArgumentParser(prog="fluxpipe", description="CI/CD Pipeline Engine")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("init", help="Initialize pipeline config")
    run_p = sub.add_parser("run", help="Run pipeline")
    run_p.add_argument("--config", default="fluxpipe.yaml")
    sub.add_parser("history", help="Show run history")

    args = parser.parse_args()

    if args.command == "init":
        from fluxpipe.config.loader import create_default_config
        path = create_default_config()
        print(f"Created: {path}")
    elif args.command == "run":
        from fluxpipe.pipeline import Pipeline
        pipeline = Pipeline.from_yaml(args.config)
        result = pipeline.run()
        print(result.summary())
    elif args.command == "history":
        print("No runs yet.")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
