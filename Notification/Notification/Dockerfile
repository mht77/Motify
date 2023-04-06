FROM mcr.microsoft.com/dotnet/aspnet:6.0 AS base
WORKDIR /app
EXPOSE 80
EXPOSE 443

FROM mcr.microsoft.com/dotnet/sdk:6.0 AS build
COPY /protos/notification.proto ./protos/
WORKDIR /src
COPY ["Notification/Notification/Notification.csproj", "Notification/"]
RUN dotnet restore "Notification/Notification.csproj"
COPY /Notification .
WORKDIR "/src/Notification"
RUN dotnet build "Notification.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "Notification.csproj" -c Release -o /app/publish /p:UseAppHost=false

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "Notification.dll"]
