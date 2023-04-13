using System.Linq.Expressions;

namespace Notification.Services;

public interface IRepository<T>
{
    Task<T?> GetById(string id);
    Task<List<T>> GetAll();
    Task<T> Add(T obj);
    Task<T> Update(T obj);
    Task Delete(string id);

    Task<List<T>> Find(Expression<Func<T, Boolean>> predicate);

}