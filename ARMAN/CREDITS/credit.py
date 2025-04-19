import os
import base64 as b, os as o, sys as s, hashlib as h  

# Define the list of required files
r = ['developer.txt', 'attack.txt']

# Check if each file exists
for f in r:  
    if not o.path.isfile(f):  
        print(f"{f} nahi mila. Script band kiya jaa raha hai.")  
        s.exit()  

# Read the contents of developer.txt
with open('developer.txt', 'r') as d:  
    o_t = d.read()  

# Read the contents of attack.txt
with open('attack.txt', 'r') as a:  
    e_h = a.read().strip()  

# Function to compute SHA-256 hash
def g_h(t):  
    return h.sha256(t.encode()).hexdigest()  

# Compute hash of developer.txt content
c_h = g_h(o_t)  

# Compare hashes
if c_h == e_h:  
    print(o_t)  
else:  
    print(b.b64decode("RE9OVCBDSEFOR0UgVEhFIERFVkVMT1BFUiBORU1FCi8vIEZHIC0tIEBwYl9YMDE=").decode())  
    s.exit()