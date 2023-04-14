using System.Linq.Expressions;
using Notification.Services;

namespace NotificationTest;

public class NotificationMockRepo : IRepository<Notification.Models.Notification>
{
    private List<Notification.Models.Notification> notifications = new()
    {
        new Notification.Models.Notification("first", "1"),
        new Notification.Models.Notification("second", "2"),
    };
    public Task<Notification.Models.Notification?> GetById(string id)
    {
        return Task.FromResult(notifications.Find(x=>x.Id.ToString() == id));
    }

    public Task<List<Notification.Models.Notification>> GetAll()
    {
        return Task.FromResult(notifications);
    }

    public Task<Notification.Models.Notification> Add(Notification.Models.Notification obj)
    {
        notifications.Add(obj);
        return Task.FromResult(obj);
    }

    public Task<Notification.Models.Notification> Update(Notification.Models.Notification obj)
    {
        throw new NotImplementedException();
    }

    public Task Delete(string id)
    {
        throw new NotImplementedException();
    }

    public Task<List<Notification.Models.Notification>> Find(Expression<Func<Notification.Models.Notification, bool>> predicate)
    {
        return Task.FromResult(notifications.Where(predicate.Compile()).ToList());
    }
}