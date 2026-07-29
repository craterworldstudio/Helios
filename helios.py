import argparse as ap
import os
from src.lexer import Lexer

def handle_build(args):
    # Resolve the path to an absolute path for reliability
    target_path = os.path.abspath(args.path)

    with open(target_path, 'r+') as f: 
        source = f.read()
        lexer = Lexer(source, target_path)

    #print(lexer.process_tokens())
    tokens, err = lexer.process_tokens()
    if err: 
        print(err)
    else:
        for _ in list(tokens):
            print(_)


def handle_run(args):
    target_path = os.path.abspath(args.path)


if __name__ == "__main__":
    parser = ap.ArgumentParser(
        prog="helios",
        description="Helios development utility pipeline tool."
    )
    
    # Create a subparser container to distinguish 'build' from 'run'
    subparsers = parser.add_subparsers(
        dest="command", 
        required=True, 
        help="Available action commands"
    )
    build_parser = subparsers.add_parser("build", help="Compile target directory or file assets")
    build_parser.add_argument("path", type=str, help="Target file or directory system location")
    build_parser.set_defaults(func=handle_build)

    run_parser = subparsers.add_parser("run", help="Boot up target runtime application")
    run_parser.add_argument("path", type=str, help="Target file or directory system location")
    run_parser.set_defaults(func=handle_run)

    args = parser.parse_args()
    
    args.func(args)


