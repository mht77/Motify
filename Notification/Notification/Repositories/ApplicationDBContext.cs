using Microsoft.EntityFrameworkCore;

namespace Notification.Repositories;

public class ApplicationDBContext: DbContext
{
    public DbSet<Models.Notification> Notifications => Set<Models.Notification>();
    
    public ApplicationDBContext(DbContextOptions<ApplicationDBContext> options) : base(options)
    {
    }

}