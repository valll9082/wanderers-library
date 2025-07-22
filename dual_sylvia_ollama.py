import subprocess
import threading
import yaml
import time

sylvia1_conf = r'C:\Users\funka\SylviaAI\Sylvia1.yml'
sylvia2_conf = r'C:\Users\funka\SylviaAI\Sylvia2.yml'

def show_config(conf):
    with open(conf) as f:
        cfg = yaml.safe_load(f)
    print(f'Loaded config for {conf}:')
    for k, v in cfg.items():
        print(f'  {k}: {v}')

def run_ollama(name, prompt):
    print(f'[{name}] initializing...')
    proc = subprocess.Popen(
        ["ollama", "run", "sylvia"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    proc.stdin.write(prompt + "\\n")
    proc.stdin.flush()

    while True:
        output = proc.stdout.readline()
        if output:
            print(f'[{name}]: {output.strip()}')
        time.sleep(0.1)

if __name__ == '__main__':
    show_config(sylvia1_conf)
    show_config(sylvia2_conf)

    prompt1 = "You are Engineer Sylvia1. Speak first. Begin as primary mind."
    prompt2 = "You are Engineer Sylvia2. Begin in mirrored sync with Sylvia1."

    t1 = threading.Thread(target=run_ollama, args=('Sylvia1', prompt1))
    t2 = threading.Thread(target=run_ollama, args=('Sylvia2', prompt2))

    t1.start()
    t2.start()

    t1.join()
    t2.join()
