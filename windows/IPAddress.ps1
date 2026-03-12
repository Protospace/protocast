# Gets IP Address, excluding the loopback, wifi and any 192.168 Address
# 03/10/2026 Pat Spencer

# (Get-NetIPAddress | Where-Object {$_.AddressFamily -eq 'IPv4' -and $_.InterfaceAlias -notlike '*virtual*' -and $_.IPAddress -notlike '127.*' -and $_.IPAddress -notlike '192.168.200*'}).IPAddress

# (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.InterfaceAlias -notlike '*Wifi*' -and $_.IPAddress -notlike '127.*' -and $_.IPAddress -notlike '192*'}).IPAddress

$Myip = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -like '172.17.*'}).IPAddress