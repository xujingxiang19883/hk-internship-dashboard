$p = 'C:\Windows\System32\drivers\etc\hosts'
(Get-Content $p) -replace '140\.82\.112\.3 github\.com', '140.82.116.3 github.com' | Set-Content $p -Encoding ASCII
ipconfig /flushdns
