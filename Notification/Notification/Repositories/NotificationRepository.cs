namespace Notification.Repositories;

public class NotificationRepository: RepositoryBase<Models.Notification>
{
    public NotificationRepository(ApplicationDBContext dbContext) : base(dbContext)
    {
    }
}