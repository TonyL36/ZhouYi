param(
    [switch]$BuildBackend
)

$ServerIP = "47.109.193.180"

$RemoteRoot = "ZhouYi_Final"

Write-Host "Uploading deployment files..."

scp docker-compose.yml root@${ServerIP}:${RemoteRoot}/docker-compose.yml
if ($LASTEXITCODE -ne 0) { throw "Failed to upload docker-compose.yml" }

scp deployment\nginx\nginx.conf root@${ServerIP}:${RemoteRoot}/deployment/nginx/nginx.conf
if ($LASTEXITCODE -ne 0) { throw "Failed to upload nginx.conf" }

scp backend\src\main\resources\application.properties root@${ServerIP}:${RemoteRoot}/backend/src/main/resources/application.properties
if ($LASTEXITCODE -ne 0) { throw "Failed to upload backend application.properties" }

scp backend\src\main\java\com\zhouyi\demo\service\HexagramService.java root@${ServerIP}:${RemoteRoot}/backend/src/main/java/com/zhouyi/demo/service/HexagramService.java
if ($LASTEXITCODE -ne 0) { throw "Failed to upload HexagramService.java" }

Write-Host "Uploading frontend dist..."
scp -r frontend\dist\* root@${ServerIP}:${RemoteRoot}/frontend/dist/
if ($LASTEXITCODE -ne 0) { throw "Failed to upload frontend dist" }

Write-Host "Uploading ZhouYi.md..."
scp backend\src\main\resources\data\ZhouYi.md root@${ServerIP}:${RemoteRoot}/backend/src/main/resources/data/ZhouYi.md
if ($LASTEXITCODE -ne 0) { throw "Failed to upload ZhouYi.md" }

Write-Host "Cleaning old deployment folder (if exists)..."
ssh -t root@${ServerIP} "rm -rf ZhouYi || true"

Write-Host "Restarting cloud services..."
$BuildBackendFlag = if ($BuildBackend) { "1" } else { "0" }
ssh -t root@${ServerIP} @"
set -e
cd ${RemoteRoot}

if command -v docker >/dev/null 2>&1; then
  if docker compose version >/dev/null 2>&1; then
    DC="docker compose"
  else
    DC="docker-compose"
  fi
else
  echo "docker not found"
  exit 1
fi

`$DC down --remove-orphans || true
if [ "${BuildBackendFlag}" = "1" ]; then
  `$DC build backend
fi
`$DC up -d

echo "Smoke test:"
for i in 1 2 3 4 5 6 7 8 9 10; do
  code=`$(curl -s -o /dev/null -w '%{http_code}' http://localhost:6400/api/hexagrams || true)
  echo "api/hexagrams: `$code"
  if [ "`$code" = "200" ]; then break; fi
  sleep 2
done
for i in 1 2 3 4 5; do
  code=`$(curl -s -o /dev/null -w '%{http_code}' 'http://localhost:6400/images/01_%E4%B9%BE.svg' || true)
  echo "images/01: `$code"
  if [ "`$code" = "200" ]; then break; fi
  sleep 2
done
"@

Write-Host "Cloud deployment finished."
