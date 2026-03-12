<#
 Script to send a "protocast me" request to the display server at Protospace
 2026/03/10 Pat.Spencer 
	V1.1 updated code to send the request with the IP Address of the requesting PC. 
#>

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("start", "stop")]
    [string]$Action = "start"
)

$Myipaddress = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -like '172.17.*'}).IPAddress

    $body = @{
    "action"  = $Action
	"ip_address" = $Myipaddress
    }

    if ($action -eq "stop") {
        $response = Invoke-WebRequest -UseBasicParsing  -Uri "http://10.139.88.128:5000/stop" -Method "POST" -Body $body
        $response.Content
    } else {
        $response = Invoke-WebRequest -UseBasicParsing -Uri "http://10.139.88.128:5000/cast" -Method "POST" -Body $body
        $response.Content
	}
	
	