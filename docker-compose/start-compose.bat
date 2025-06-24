@echo off
if not exist .env (
    for /f "delims=" %%A in ('powershell -Command "[Convert]::ToBase64String((1..32 | %%{Get-Random -Maximum 256}))"') do (
        echo SHARED_PASSWORD=%%A > .env
    )
    echo .env created with random password.
)

docker-compose --env-file .env up