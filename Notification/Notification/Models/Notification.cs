namespace Notification.Models;

public class Notification: ModelBase
{
    public string Message { get; set; }
    
    public DateTime CreatedAt { get; set; }

    public string User { get; set; } = null!;

    public Notification(string message)
    {
        Message = message;
        CreatedAt = DateTime.Now;
    }
}