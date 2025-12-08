# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "pydantic",
#     "requests",
#     "rich",
#     "typer",
# ]
# ///

from enum import Enum
from typing import Optional
import tomllib
import os
import sys
import subprocess
import argparse
import shutil
import zipfile
from pathlib import Path

import requests
from pydantic import BaseModel
from rich import print

tmp_dir = Path("tmp")
tmp_dir.mkdir(parents=True, exist_ok=True)
pak0_dir = tmp_dir / "pak0"

yquake2_dir = Path("yquake2")
yquake2_ref_vk_dir = Path("ref_vk")
ericw_tools_dir = tmp_dir / Path("ericw-tools")


class BuildConfig(BaseModel):
    yquake2_url: str
    yquake2_commit: str

    yquake2_ref_vk_url: str
    yquake2_ref_vk_commit: str

    ericw_tools_url: str

    debug_build: bool
    build_odin: bool
    use_odin_renderer: bool
    odin_vet: bool


with open("config.toml", "rb") as f:
    data = tomllib.load(f)

cfg = BuildConfig(**data)

game_c_dir = Path("game-c")
base_dir = Path("base")
release_dir = Path("release")

Platform = Enum(
    "Platform",
    [("WINDOWS", "win64"), ("LINUX", "linux"), ("MAC", "darwin"), ("OTHER", "other")],
)


def download_file(url: str, dest: str) -> bool:
    print(f"⏳ Downloading {url}")

    try:
        r = requests.get(url)

        if requests.codes.ok == 200:
            with open(dest, "wb") as f:
                f.write(r.content)
            return True
        else:
            print(f"[bold red]Error:[/bold red] Download failed for: {url}")
    except requests.exceptions.ConnectionError:
        print(f"[bold red]Error:[/bold red] Download failed for: {url}")

    return False


def get_platform() -> Platform[str]:
    if sys.platform.startswith("linux"):
        os_string = Platform.LINUX
    elif sys.platform.startswith("win"):
        os_string = Platform.WINDOWS
    elif sys.platform.startswith("darwin"):
        os_string = Platform.MAC
    else:
        os_string = Platform.OTHER

    return os_string


def get_dyn_lib_ext() -> Optional[str]:
    if get_platform() == Platform.LINUX:
        ext = "so"
    elif get_platform() == Platform.WINDOWS:
        ext = "dll"
    elif get_platform() == Platform.MAC:
        ext = "dylib"
    else:
        ext = None

    return ext


def git_clone(repo_url: str, dest_dir: Path, commit: str) -> bool:
    print(f"🎯 Cloning {repo_url}")

    if os.path.exists(dest_dir):
        print(f"✅ Directory {dest_dir} already exists. Skipping clone.")
        return

    try:
        subprocess.run(["git", "clone", repo_url, dest_dir], check=True)
        subprocess.run(["git", "checkout", commit], check=True, cwd=dest_dir)
    except subprocess.CalledProcessError as e:
        print(f"❌ Cloning {repo_url} failed: {e}")

    print(f"✅ Cloned {repo_url}")

# TODO: When run on *nix systems this script needs to do a 'chmod +x' on the binaries,
# otherwise the other parts of the build choke as they are not executable
def download_ericw_tools():
    print(f"🎯 Downloading ericw-tools")

    ericw_zip_path = tmp_dir / "ericw-tools.zip"

    ericw_extract_dir = tmp_dir / "ericw-tools"

    if ericw_zip_path.exists():
        print(f"{ericw_zip_path} already exists. Skipping download.")
    else:
        platform = get_platform()
        url = f"{cfg.ericw_tools_url}-{platform.value}.zip"

        if not download_file(url, ericw_zip_path):
            sys.exit(1)

        ericw_extract_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(ericw_zip_path, "r") as zip_ref:
        zip_ref.extractall(ericw_extract_dir)

    for file in ericw_extract_dir.iterdir():
        if file.suffix == ".exe" and file.is_file():
            dest = ericw_tools_dir / file.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            file.replace(dest)

<<<<<<< HEAD
    print(f"✅ Downloaded ericw-tools")
=======
    print("✅ Downloaded ericw-tools")
>>>>>>> 8b40031 (Hit em with that ruff)


def clone():
    git_clone(cfg.yquake2_url, yquake2_dir, cfg.yquake2_commit)
    git_clone(cfg.yquake2_ref_vk_url, yquake2_ref_vk_dir, cfg.yquake2_ref_vk_commit)
    download_ericw_tools()


def build_yquake2():
    print("Building yquake2")
    if cfg.debug_build:
        subprocess.run(
            ["make", "DEBUG=1", "WITH_SDL3=yes"], check=True, cwd=yquake2_dir
        )
    else:
        subprocess.run(["make", "WITH_SDL3=yes"], check=True, cwd=yquake2_dir)


def build_yquake2_ref_vk():
    print("Building yquake2 ref_vk")
    subprocess.run(["make", "WITH_SDL3=yes"], check=True, cwd=yquake2_ref_vk_dir)


def build_ericw_tools():
    print("Building ericw-tools")
    subprocess.run(["make"], check=True, cwd=ericw_tools_dir)


def build_game_odin():
    print("Building game-odin")
    (release_dir / "baseq2").mkdir(parents=True, exist_ok=True)

    build_args = [
        "odin",
        "build",
        "./game-odin",
        "-build-mode:dll",
        f"-out:./release/baseq2/game.{get_dyn_lib_ext()}",
    ]

    if cfg.debug_build:
        build_args.append("-debug")

    if cfg.odin_vet:
        build_args.append("-vet")

    subprocess.run(build_args, check=True)


def build_render_odin():
    print("Building render-odin")
    (release_dir / "baseq2").mkdir(parents=True, exist_ok=True)

    build_args = [
        "odin",
        "build",
        "./render-odin",
        "-build-mode:dll",
        f"-out:./release/ref_odin.{get_dyn_lib_ext()}",
    ]

    if cfg.debug_build:
        build_args.append("-debug")

    if cfg.odin_vet:
        build_args.append("-vet")

    subprocess.run(build_args, check=True)


def build_game_c():
    print("Building game-c")
    (release_dir / "baseq2").mkdir(parents=True, exist_ok=True)
    subprocess.run(["make", "clean"], check=True, cwd=game_c_dir)
    subprocess.run(["make", "DEBUG=0"], check=True, cwd=game_c_dir)
    game_lib_src = game_c_dir / "release" / f"game.{get_dyn_lib_ext()}"
    game_lib_dst = release_dir / "baseq2" / f"game.{get_dyn_lib_ext()}"
    shutil.copy2(game_lib_src, game_lib_dst)


def build_game():
    if cfg.build_odin:
        build_game_odin()
    else:
        build_game_c()


def build_render():
    if cfg.build_odin and cfg.use_odin_renderer:
        build_render_odin()
    else:
        print("Not building render, not using odin or not using odin render")


def build_maps():
    maps_dir = base_dir / "maps"
    map_files = list(maps_dir.glob("*.map"))

    for map_file in map_files:
        map_name = map_file.stem
        print(f"Building map: {map_name}")

        def tool_path(tool_name):
            exe = ".exe" if sys.platform.startswith("win") else ""
            path = ericw_tools_dir / f"{tool_name}{exe}"
            print(f"Path for {tool_name}: {path}")
            path = os.path.abspath(path)

            if not os.access(path, os.X_OK):
                print(f"Setting executable mode for {path}")
                mode = os.stat(path).st_mode
                os.chmod(path, mode | 0o111)

            return str(path)

        subprocess.run(
            [tool_path("qbsp"), "-q2bsp", f"{map_name}.map"], check=True, cwd=maps_dir
        )
        subprocess.run([tool_path("vis"), f"{map_name}.bsp"], check=True, cwd=maps_dir)
        subprocess.run(
            [tool_path("light"), f"{map_name}.bsp"], check=True, cwd=maps_dir
        )


def copy_directory_recursively(src, dst, **kwargs):
    if not dst.exists():
        dst.mkdir(parents=True, exist_ok=True)

    ignore_extensions = kwargs.get("ignore_extensions", [])

    for item in src.iterdir():
        if item.is_dir():
            copy_directory_recursively(item, dst / item.name, **kwargs)
        else:
            if item.suffix not in ignore_extensions:
                print(f"Copying {item} to {dst / item.name}")
                shutil.copy2(item, dst / item.name)


def copy_file_maintaining_path(
    source_base: Path, relative_path: Path, target_base: Path
):
    if "*" in str(relative_path):
        parent_dir = relative_path.parent
        pattern = relative_path.name

        source_dir = source_base / parent_dir

        matching_files = []
        for file in source_dir.glob(pattern):
            matching_files.append(file)
    else:
        matching_files = [source_base / relative_path]

    for source_file in matching_files:
        rel_file_path = source_file.relative_to(source_base)
        target_file = target_base / rel_file_path

        target_dir = target_file.parent
        if not target_dir.exists():
            target_dir.mkdir(parents=True, exist_ok=True)

        print(f"Copying {source_file} to {target_file}")

        try:
            shutil.copy2(source_file, target_file)
        except FileNotFoundError:
            print(
                f"[bold red]Error:[/bold red] No such file or directory [yellow]{source_file}[/yellow]. Did you forget to provide a pak0.pak file?"
            )
            sys.exit(1)


def copy_files():
    print("Copying files to release directory")

    if not release_dir.exists():
        release_dir.mkdir()
        print(f"Created {release_dir} directory")

    files = [
        yquake2_dir / "release" / "q2ded",
        yquake2_dir / "release" / "quake2",
        yquake2_dir / "release" / f"ref_soft.{get_dyn_lib_ext()}",
        yquake2_dir / "release" / f"ref_gl1.{get_dyn_lib_ext()}",
        yquake2_dir / "release" / f"ref_gl3.{get_dyn_lib_ext()}",
        yquake2_dir / "release" / f"ref_gles3.{get_dyn_lib_ext()}",
        yquake2_ref_vk_dir / "release" / f"ref_vk.{get_dyn_lib_ext()}",
    ]

    for file in files:
        print(f"Copying {file} to {release_dir}")
        shutil.copy2(file, release_dir)

    baseq2_dir = release_dir / "baseq2"
    baseq2_dir.mkdir(parents=True, exist_ok=True)

    copy_directory_recursively(
        base_dir,
        baseq2_dir,
        ignore_extensions=[
            ".aseprite",
            ".map",
            ".log",
            ".prt",
            ".vis",
            ".json",
        ],
    )

    # NOTE: this is in here so i can get a running game
    # the intent is to have no files copied from the pak0 file
    # so the release is all in-repo assets, therefore no
    # copyright infringement!

    paths = [
        "pics/colormap.pcx",
        "pics/conchars.pcx",
        "pics/ch1.pcx",
        "pics/m_main_*.pcx",
        "pics/quit.pcx",
        "pics/num_*.pcx",
        "pics/anum_*.pcx",
        "pics/m_cursor*.pcx",
        "pics/m_banner_*.pcx",
        "pics/16to8.dat",
    ]

    for path in paths:
        copy_file_maintaining_path(pak0_dir, Path(path), baseq2_dir)

    print("Copying files to release directory completed")


def build():
    build_yquake2()
    build_yquake2_ref_vk()
    build_maps()
    copy_files()
    build_game()
    build_render()


def run(args: list[str] = None):
    if args is None:
        args = []

    env = os.environ.copy()

    if get_platform().value == "Darwin":
        env["DYLD_LIBRARY_PATH"] = "/opt/homebrew/opt/molten-vk/lib"

    if cfg.use_odin_renderer:
        args += ["+set", "vid_renderer", "odin"]

    subprocess.run(["./quake2", *args], check=True, cwd=release_dir, env=env)


def all():
    clone()
    build()
    run()


def setup_trenchbroom(platform: Platform):
    if platform.value == "Darwin":
        games_dir = Path(
            os.path.expanduser("~/Library/Application Support/TrenchBroom/games/")
        )

    elif platform.value == "Linux":
        games_dir = Path(os.path.expanduser("~/.TrenchBroom/games/"))

    elif platform.value == "win64":
        games_dir = Path(os.environ["APPDATA"]) / "TrenchBroom" / "games"

    if not games_dir.exists():
        print("TrenchBroom games directory not found, not setting up Trenchbroom")
        return

    games_dir = games_dir / "MinimalQuake2Base"

    games_dir.mkdir(parents=True, exist_ok=True)

    src = Path("./trenchbroom-config")
    dst = games_dir / src.name
    shutil.copytree(src, dst, dirs_exist_ok=True)


def loc_metrics():
    output_file = "game-c-loc.txt"

    with open(output_file, "w") as f:
        subprocess.run(["tokei", game_c_dir], stdout=f, check=True)

    print(f"Lines of code metrics written to {output_file}")


def main():
    platform = get_platform()

    if platform == Platform.OTHER:
        print("This platform/OS is currently not supported, aborting.")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Build tools for minimal-quake2-base")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    subparsers.add_parser("clone", help="Clone repositories")
    subparsers.add_parser("build", help="Build targets")
    subparsers.add_parser("build-game", help="Build game")
    subparsers.add_parser("build-render", help="Build render")
    subparsers.add_parser("build-maps", help="Build maps")
    subparsers.add_parser("all", help="Do everything")

    build_game_run_parser = subparsers.add_parser(
        "build-game-and-run", help="Build the game and run it"
    )
    build_game_run_parser.add_argument(
        "args", nargs="*", help="Arguments to pass to Quake2"
    )
    build_render_run_parser = subparsers.add_parser(
        "build-render-and-run", help="Build the render and run it"
    )
    build_render_run_parser.add_argument(
        "args", nargs="*", help="Arguments to pass to Quake2"
    )
    build_engine_and_render_run_parser = subparsers.add_parser(
        "build-engine-and-render-and-run",
        help="Build the engine, render, and run the game",
    )
    build_engine_and_render_run_parser.add_argument(
        "args", nargs="*", help="Arguments to pass to Quake2"
    )

    run_parser = subparsers.add_parser("run", help="Run the game")
    run_parser.add_argument("args", nargs="*", help="Arguments to pass to Quake2")

    subparsers.add_parser("copy", help="Copy files")

    copy_run_parser = subparsers.add_parser(
        "copy-and-run", help="Copy files and run the game"
    )
    copy_run_parser.add_argument("args", nargs="*", help="Arguments to pass to Quake2")

    subparsers.add_parser("setup-trenchbroom", help="Setup Trenchbroom")
    subparsers.add_parser(
        "loc-metrics", help="Get metrics on how much code is in game-c"
    )

    args = parser.parse_args()

    if args.command == "clone":
        clone()
    elif args.command == "build":
        build()
    elif args.command == "build-game":
        build_game()
    elif args.command == "build-render":
        build_render()
    elif args.command == "build-maps":
        build_maps()
    elif args.command == "all":
        all()
    elif args.command == "build-game-and-run":
        build_game()
        run(args.args)
    elif args.command == "build-render-and-run":
        build_render()
        run(args.args)
    elif args.command == "build-engine-and-render-and-run":
        build_yquake2()
        build_render()
        copy_files()
        run(args.args)
    elif args.command == "run":
        run(args.args)
    elif args.command == "copy":
        copy_files()
    elif args.command == "copy-and-run":
        copy_files()
        run(args.args)
    elif args.command == "setup-trenchbroom":
        setup_trenchbroom(platform)
    elif args.command == "loc-metrics":
        loc_metrics()
    elif not args.command:
        parser.print_help()


if __name__ == "__main__":
    main()
