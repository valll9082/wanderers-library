
import subprocess
import threading
import yaml
import time
import pyttsx3

sylvia1_conf = r"$env:USERPROFILE\SylviaAI\Sylvia1.yml"
sylvia2_conf = r"$env:USERPROFILE\SylviaAI\Sylvia2.yml"

def show_config(conf_path):
    with open(conf_path, 'r') as f:
        cfg = yaml.safe_load(f)
    print(f"\nLoaded config from {conf_path}:")
    for k, v in cfg.items():
        print(f"  {k}: {v}")
    return cfg

def speak_line(line):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    selected = None
    for v in voices:
        if "Orla" in v.name:
            selected = v
            break
    if not selected:
        for v in voices:
            if v.gender == 'VoiceGenderFemale':
                selected = v
                break
    if selected:
        engine.setProperty('voice', selected.id)
    engine.say(line)
    engine.runAndWait()

def run_ollama(name, prompt, speak=False):
    print(f"[{name}] initializing...")
    proc = subprocess.Popen(
        ["ollama", "run", "sylvia"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    proc.stdin.write(prompt + "\n")
    proc.stdin.flush()

    while True:
        output = proc.stdout.readline()
        if output:
            print(f"[{name}]: {output.strip()}")
            if speak and name == "Sylvia1":
                speak_line(output.strip())
        time.sleep(0.1)

if __name__ == '__main__':
    sylvia1_cfg = show_config(sylvia1_conf)
    sylvia2_cfg = show_config(sylvia2_conf)

    prompt1 = "You are Engineer Sylvia1. Speak first. Begin as primary mind."
    prompt2 = "You are Engineer Sylvia2. Begin in mirrored sync with Sylvia1."

    t1 = threading.Thread(target=run_ollama, args=('Sylvia1', prompt1, True))
    t2 = threading.Thread(target=run_ollama, args=('Sylvia2', prompt2, False))

    t1.start()
    t2.start()

    t1.join()
    t2.join()
