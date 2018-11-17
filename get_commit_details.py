import json
from collections import Counter
import subprocess

cmd = ['curl', '-i', 'https://api.github.com/repos/<username>/<repo_name>/commits']
st = subprocess.run(cmd,  stdout=subprocess.PIPE)
f = st.stdout.decode('utf-8')
f = f[f.index('['):]
print(f)
j= json.loads(f)

commits = []
for commit in j:
	commits.append(commit['commit'])

print(Counter([x['author']['name'] for x in commits]))