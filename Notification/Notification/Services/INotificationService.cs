namespace Notification.Services;

public interface INotificationService
{
    Task<bool> NewMsg(dynamic msg);
    Task NewUser(dynamic account);
    Task DeleteUser(dynamic account);
}