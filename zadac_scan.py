import requests
import sys
import json

def fetch_metadata(code):
    url = f"https://api.pcloud.com/showpublink?code={code}"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()


def traverse(node, path="", files=None):
    if files is None:
        files = []
    if node.get('isfolder'):
        name = node.get('name', '')
        contents = node.get('contents', [])
        for child in contents:
            traverse(child, f"{path}/{name}" if name else name, files)
    else:
        files.append({
            'path': f"{path}/{node.get('name', '')}".lstrip('/'),
            'size': node.get('size', 0)
        })
    return files


def analyze(files):
    anomalies = []
    name_count = {}
    total_size = 0
    for f in files:
        total_size += f['size']
        basename = f['path'].split('/')[-1]
        name_count[basename] = name_count.get(basename, 0) + 1
        if f['size'] == 0:
            anomalies.append(f"Zero-size file: {f['path']}")
        if basename.endswith(('.exe', '.dll')):
            anomalies.append(f"Executable file: {f['path']}")
    dupes = [name for name, count in name_count.items() if count > 1]
    for dupe in dupes:
        anomalies.append(f"Duplicate file name: {dupe}")
    return total_size, anomalies


def main():
    if len(sys.argv) < 2:
        print("Usage: zadac_scan.py <pcloud_code>")
        return
    code = sys.argv[1]
    data = fetch_metadata(code)
    files = traverse(data.get('metadata', {}))
    total_size, anomalies = analyze(files)
    print(f"Total files: {len(files)}")
    print(f"Total size: {total_size} bytes")
    if anomalies:
        print("Anomalies detected:")
        for a in anomalies:
            print(f" - {a}")
    else:
        print("No anomalies detected.")

if __name__ == '__main__':
    main()
