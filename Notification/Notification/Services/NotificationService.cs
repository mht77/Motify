using Grpc.Core;

namespace Notification.Services;

public class NotificationService : Notification.NotificationService.NotificationServiceBase, INotificationService
{
    private readonly ILogger<NotificationService> logger;

    private readonly IRepository<Models.Notification> repository;

    private readonly IServiceProvider serviceProvider;

    public NotificationService(ILogger<NotificationService> logger, IRepository<Models.Notification> repository, IServiceProvider serviceProvider)
    {
        this.logger = logger;
        this.repository = repository;
        this.serviceProvider = serviceProvider;
    }

    public override async Task GetNotifications(NotificationRequest request, IServerStreamWriter<NotificationResponse> responseStream, ServerCallContext context)
    {
        var notifications = await repository.Find(x => x.User == request.Id);
        
        foreach (var notification in notifications)
        {
            await responseStream.WriteAsync(new NotificationResponse
            {
                CreatedAt = notification.CreatedAt.ToString(),
                Msg = notification.Message
            });
        }
    }

    public async Task<bool> NewMsg(dynamic msg)
    {
        using var scope = serviceProvider.CreateScope();
        var repo = scope.ServiceProvider.GetRequiredService<IRepository<Models.Notification>>();
        try
        {
            Models.Notification notification = new (msg["msg"], msg["uid"]);
            await repo.Add(notification);
            return true;
        }
        catch (Exception e)
        {
            logger.LogWarning(e.Message);
            return false;
        }
    }

    public async Task NewUser(dynamic account)
    {
        try
        {
            Models.Notification notification = new Models.Notification
            (
                message: "Welcome to Motify",
                user: account["id"]
            );
            await repository.Add(notification);
        }
        catch (Exception e)
        {
            logger.LogWarning(e.Message);
        }
    }

    public async Task DeleteUser(dynamic account)
    {
        using var scope = serviceProvider.CreateScope();
        var repo = scope.ServiceProvider.GetRequiredService<IRepository<Models.Notification>>();
        try
        {
            var id = account["id"] as string;
            var notifications = await repo.Find(x => x.User == id);
            foreach (var notification in notifications)
            {
                await repo.Delete(notification.Id.ToString());
            }
        }
        catch (Exception e)
        {
            logger.LogWarning(e.Message);
        }
    }
}