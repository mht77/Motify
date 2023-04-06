using Grpc.Core;

namespace Notification.Services;

public class NotificationService : Notification.NotificationService.NotificationServiceBase
{
    private readonly ILogger<NotificationService> logger;

    private readonly IRepository<Models.Notification> repository;

    public NotificationService(ILogger<NotificationService> logger, IRepository<Models.Notification> repository)
    {
        this.logger = logger;
        this.repository = repository;
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
}