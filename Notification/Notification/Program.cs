using System.Runtime.InteropServices;
using Microsoft.AspNetCore.Server.Kestrel.Core;
using Microsoft.EntityFrameworkCore;
using Notification.Repositories;
using Notification.Services;

var builder = WebApplication.CreateBuilder(args);

if (RuntimeInformation.IsOSPlatform(OSPlatform.OSX))
    builder.WebHost.ConfigureKestrel(options =>
    {
        // Setup a HTTP/2 endpoint without TLS.
        options.ListenLocalhost(5038, o => o.Protocols = HttpProtocols.Http2);
    });

Console.WriteLine(builder.Configuration.GetConnectionString("Default"));
builder.Services.AddDbContext<ApplicationDBContext>(
    options => options.UseNpgsql(builder.Configuration.GetConnectionString("Default")));
builder.Services.AddGrpc();
builder.Services.AddTransient<IRepository<Notification.Models.Notification>, NotificationRepository>();

var app = builder.Build();

app.MapGrpcService<NotificationService>();
app.MapGet("/",
    () =>
        "Communication with gRPC endpoints must be made through a gRPC client. To learn how to create a client, visit: https://go.microsoft.com/fwlink/?linkid=2086909");

using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<ApplicationDBContext>();
    // var rabbit = scope.ServiceProvider.GetRequiredService<IRabbitMQConnection>();
    // rabbit.StartConsuming();
    db.Database.Migrate();
}

app.Run();