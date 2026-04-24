import sys
import subprocess
from pathlib import Path
from dotnet.dotnet import *
from files.files import *
from git.git import *

# See ReadMe.md file for script description.

settings_file_name = 'dotnet_set_up_identity_settings.json'
settings = get_settings_from_json_file(Path(__file__).parent.resolve(), settings_file_name)

GIT_EXE = settings["Git_exe"]
DOTNET_EXE = settings["Dotnet_exe"]
TEMP_DIR = Path(settings["Temp_dir"])
VARIOUS_FILES_REPO_URL = settings["Various_files_repo_url"]
VARIOUS_FILES_REPO_DESIRED_DIRECTORY = settings["Various_files_repo_desired_directory"]
VARIOUS_FILES_ROOT_DIR = TEMP_DIR / Path(VARIOUS_FILES_REPO_DESIRED_DIRECTORY)
PROJECT_NAME = settings["Project_name"]
PROJECT_ROOT_DIR = settings["Project_root_dir"]
MAJOR_VERSION = settings["Major_version"]
MINOR_VERSION = settings["Minor_version"]
PATCH_VERSION = settings["Patch_version"]

if not Path(GIT_EXE).is_file():
    print(f"{GIT_EXE} file doesn't exist", file=sys.stderr)
    sys.exit()

if not Path(DOTNET_EXE).is_file():
    print(f"{DOTNET_EXE} file doesn't exist", file=sys.stderr)
    sys.exit()

if not TEMP_DIR.is_dir():
    print(f"{TEMP_DIR} directory doesn't exist", file=sys.stderr)
    sys.exit()

if not Path(PROJECT_ROOT_DIR).is_dir():
    print(f"{PROJECT_ROOT_DIR} directory doesn't exist", file=sys.stderr)
    sys.exit()

def add_file(sub_dir: str, file_name: str, replacements: dict[str, str]):
  file_path = Path(PROJECT_ROOT_DIR) / Path(sub_dir)
  file_path.mkdir(parents=True, exist_ok=True)  # ensure directory exists
  contents = get_file_content(VARIOUS_FILES_ROOT_DIR / Path(sub_dir) / Path(file_name))
  contents = replace_strings_in_content(contents, replacements)
  write_file(Path(file_path / Path(file_name)), contents)

def replace_file(sub_dir: str | None, file_name: str, replacements: dict[str, str]):
  appended_path = Path(file_name) if sub_dir is None else Path(sub_dir) / Path(file_name)
  contents = get_file_content(VARIOUS_FILES_ROOT_DIR / appended_path)
  contents = replace_strings_in_content(contents, replacements)
  replace_file_contents(Path(PROJECT_ROOT_DIR) / appended_path, contents)

various_files_clone_args = [
    "clone",
    "--filter=blob:none",
    "--no-checkout",
    "--depth", "1",
    VARIOUS_FILES_REPO_URL,
    TEMP_DIR
]

try:
  # Sparse clone Various Files repo

  print(f"Cloning {VARIOUS_FILES_REPO_URL} (with partial + shallow settings...)")
  run_git_command(GIT_EXE, various_files_clone_args, TEMP_DIR)
  print("Clone completed successfully (no files checked out yet).")

  print("Checking out ", VARIOUS_FILES_REPO_DESIRED_DIRECTORY)
  run_git_command(GIT_EXE, ["sparse-checkout", "init", "--cone"], repo_path=TEMP_DIR)
  run_git_command(GIT_EXE, ["sparse-checkout", "set", VARIOUS_FILES_REPO_DESIRED_DIRECTORY], repo_path=TEMP_DIR)
  run_git_command(GIT_EXE, ["checkout"], repo_path=TEMP_DIR)
  print("Check out completed.")

except subprocess.CalledProcessError as e:
    print("Command failed!")
    print("Exit code:", e.returncode)
    print("Stderr:", e.stderr)

# Add <ProjectFolder>/Controllers/AccountsController.cs

add_file("Controllers", "AccountsController.cs", { "<ProjectName>" : PROJECT_NAME })

# Add <ProjectFolder>/Models/Accounts/AccountLoginViewModel.cs

add_file("Models/Accounts", "AccountLoginViewModel.cs", { "<ProjectName>" : PROJECT_NAME })

# Add file <ProjectFolder>/Data/ApplicationDbContext.cs

add_file("Data", "ApplicationDbContext.cs", { "<ProjectName>" : PROJECT_NAME })

# Add file <ProjectFolder>/Entities/AppUser.cs

add_file("Entities", "AppUser.cs", { "<ProjectName>" : PROJECT_NAME })

# Add <ProjectFolder>/Views/Accounts/Login.cshtml

add_file("Views/Accounts", "Login.cshtml", { "<ProjectName>" : PROJECT_NAME })

# Modify <ProjectFolder>/Views/Home/Index.cshtml

replace_file("Views/Home", "Index.cshtml", { "<ProjectName>" : PROJECT_NAME })

# Modify <ProjectFolder>/Views/Shared/_Layout.cshtml

replace_file("Views/Shared", "_Layout.cshtml", { "<ProjectName>" : PROJECT_NAME })

# Modify <ProjectFolder>/appsettings.Development.json

replace_file(None, "appsettings.Development.json", { "<ProjectName>" : PROJECT_NAME, "<MajorVersion>" : MAJOR_VERSION, "<MinorVersion>" : MINOR_VERSION, "<PatchVersion>" : PATCH_VERSION })

# Modify <ProjectFolder>/Program.cs

replace_file(None, "Program.cs", { "<ProjectName>" : PROJECT_NAME })

# Install packages

args = [
    "add",
    PROJECT_ROOT_DIR,
    "package",
    "Microsoft.AspNetCore.Identity.EntityFrameworkCore",
    "--version",
    "9.0.15"
]

try:
  print("Install Microsoft.AspNetCore.Identity.EntityFrameworkCore")
  run_dotnet_command(DOTNET_EXE, args)
except subprocess.CalledProcessError as e:
    print("Command failed!")
    print("Exit code:", e.returncode)
    print("Stderr:", e.stderr)

args = [
    "add",
    PROJECT_ROOT_DIR,
    "package",
    "Pomelo.EntityFrameworkCore.MySql",
    "--version",
    "9.0.0"
]

try:
  print("Install Pomelo.EntityFrameworkCore.MySql")
  run_dotnet_command(DOTNET_EXE, args)
except subprocess.CalledProcessError as e:
    print("Command failed!")
    print("Exit code:", e.returncode)
    print("Stderr:", e.stderr)

# State remaining tasks for user

print(f"Delete contents of temp directory {TEMP_DIR}")
print("Set up MySQL database to use with project with db name and user name given in appsettings.Development.json.")
print("Set <Server> in appsettings.Development.json for MySQL database.")
print("Set <Password> in appsettings.Development.json for MySQL database.")
print("Execute SQL to create various tables required by Identity and add the default app user.")