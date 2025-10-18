import os
import subprocess

def git_last_updated_time(path):
    process = subprocess.Popen(['git', 'log', '-1', '--pretty=%ci', path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, _ = process.communicate()

    return stdout.decode()

if __name__ == "__main__":
    paths = [os.path.join('_posts', file) for file in os.listdir('_posts')]
    paths = [path for path in paths if path.endswith('.md')]

    for path in paths:
        lines = []
        front_matter_started = False
        editted_modified_time = False
        front_matter_edit = True
        with open(path, 'r') as file:
            for line in file:
                if line.startswith('---') and front_matter_edit:
                    if not front_matter_started:
                        front_matter_started = True
                        lines.append(line)
                    else:
                        if not editted_modified_time:
                            lines.append(f'last_modified_at: {git_last_updated_time(path)}')
                        lines.append(line)
                        front_matter_edit = False
                elif front_matter_edit:
                    if line.startswith('last_modified_at:'):
                        lines.append(f'last_modified_at: {git_last_updated_time(path)}')
                        editted_modified_time = True
                    else:
                        lines.append(line)
                else:
                    lines.append(line)
        with open(path, 'w') as file:
            file.write(''.join(lines))
                    
                    
