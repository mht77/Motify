namespace Notification.Models;

public class Notification: ModelBase
{
    public string Message { get; set; }
    
    public DateTime CreatedAt { get; set; }

    public string User { get; set; }

    public Notification(string message, string user)
    {
        Message = message;
        CreatedAt = DateTime.UtcNow;
        User = user;
    }
}