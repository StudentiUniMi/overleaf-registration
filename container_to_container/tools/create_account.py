import subprocess

def create_account(email: str = "davrot@uni-bremen.de", container_name: str = "overleafserver"):

    work_string: str = f"cd /overleaf/services/web && node modules/server-ce-scripts/scripts/create-user --email={email}"
    result = subprocess.run(["docker", "exec", container_name, "/bin/bash", "-ce", work_string ], capture_output=True, text=True)

    success: bool = False
    for i in result.stdout.splitlines():
        if i.startswith(f"Successfully created {email} as a"):
            success = True
    return success


