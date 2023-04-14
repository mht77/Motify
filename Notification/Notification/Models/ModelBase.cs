using System.ComponentModel.DataAnnotations;

namespace Notification.Models;

public class ModelBase
{
    [Key]
    public Guid Id { get; set; }

    public ModelBase()
    {
        Id = new Guid();
    }
}