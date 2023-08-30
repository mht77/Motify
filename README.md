# Motify
A Spotify Clone by Mohammad Toosi

This project consists of 3 services and a custom API Gateway.
(This repo is a copy of the original repo in Azure DevOps)

- API Gateway: Python - Django (+DRF)
- Music Service: Python Django
- Notification Service: ASP.NET
- Playlist Service: Golang
- Frontend: [Github](https://github.com/mht77/Motify-WebClient)

- Communications between services: gRPC & message broker (rabbitmq)
- DB: Postgres, Azure Blob Storage for files
- Deployment: Azure Container Apps
- Cache: Redis
  
