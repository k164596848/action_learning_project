from os.path import abspath
from platform import system
from subprocess import PIPE, STDOUT, Popen
from warnings import warn
import asyncio




OPENPOSE_PATH = r"C:/Users/user/Desktop/openpose/"
OPENPOSE_PATH_UBUNTU = "$OPENPOSE"
OS = system().lower()


def get_executor_path() -> str:
    if "win" in OS:
        return r"bin\OpenPoseDemo.exe"
    elif "linux" in OS:
        return r"build/examples/openpose/openpose.bin"
    raise OSError("Not supported os")


async def save_to_json_path(video_path, folder_path, **kwargs) -> bool:#openpose轉成json 格式
    return run(video_path, folder_path, **kwargs)

def exec_command(command: str) -> bool: # 利用 powershell 執行指令(command)
    """Returns: Output folder absolute path"""
    log = open("openpose.log", "a")
    if "win" in OS:
        commands = ["powershell.exe", f"cd {OPENPOSE_PATH};" + command]
    else:
        commands = [f"cd {OPENPOSE_PATH_UBUNTU} && " + command]
    process = Popen(commands, shell=True, stdout=PIPE, stderr=STDOUT)
    with process.stdout as pipe:
        for line in iter(pipe.readline, b""):  # b'\n'-separated lines
            log.write(line.strip().decode(errors="ignore") + "\n")
        log.flush()
    success = process.wait() == 0  # 0 means success
    if not success:
        warn("Openpose command didn't execute successfully! Please check `openpose.log` in root folder!")
    return success


def run(video_path: str, folder_path: str, hand=False) -> bool:#main program runing
    #for only one person   
    command = f"{get_executor_path()} --video '{abspath(video_path)}' --number_people_max 1 --tracking 0 --write_json {abspath(folder_path)} "
    # for two more people 
    # command = f"{get_executor_path()} --video '{abspath(video_path)}' --number_people_max 5  --write_json {abspath(folder_path)} --display 0 --render_pose 0"
    if hand:
        command += " --hand"
    is_success = exec_command(command)
    return is_success

