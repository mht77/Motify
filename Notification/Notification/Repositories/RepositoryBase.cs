using System.Linq.Expressions;
using Microsoft.EntityFrameworkCore;
using Notification.Models;
using Notification.Services;

namespace Notification.Repositories;

public abstract class RepositoryBase<T> : IRepository<T> where T: ModelBase
{
    protected readonly ApplicationDBContext DBContext;

    protected RepositoryBase(ApplicationDBContext dbContext)
    {
        DBContext = dbContext;
    }

    /// <summary>
    /// find an entity by id
    /// </summary>
    /// <param name="id">the id to look for</param>
    /// <returns> the entity or null if cannot find</returns>
    public virtual async Task<T?> GetById(string id)
    {
        return await DBContext.Set<T>().FindAsync(id);
    }

    /// <summary>
    /// list of all entities
    /// </summary>
    /// <returns>list of generic type</returns>
    public virtual async Task<List<T>> GetAll()
    {
        return await DBContext.Set<T>().ToListAsync();
    }

    /// <summary>
    /// create an entity with the given data(obj)
    /// </summary>
    /// <param name="obj">the new obj to be created</param>
    /// <returns> the created entity</returns>
    public virtual async Task<T> Add(T obj)
    {
        var res = await DBContext.Set<T>().AddAsync(obj);
        
        bool saveFailed;
        do
        {
            saveFailed = false;
            try
            {
                await DBContext.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException ex)
            {
                saveFailed = true;

                var entry = ex.Entries.Single();
                entry.OriginalValues.SetValues((await entry.GetDatabaseValuesAsync())!);
            }

        } while (saveFailed);

        return res.Entity;
    }

    /// <summary>
    /// modify an entity
    /// </summary>
    /// <param name="obj">the updated obj</param>
    /// <returns>the updated entity</returns>
    public virtual async Task<T> Update(T obj)
    {
        var local = DBContext.Set<T>().Local.FirstOrDefault(entry => entry.Id.Equals(obj.Id));
        
        if (local != null)
            DBContext.Entry(local).State = EntityState.Detached;
        
        DBContext.Entry(obj).State = EntityState.Modified;
        
        bool saveFailed;
        do
        {
            saveFailed = false;
            try
            {
                await DBContext.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException ex)
            {
                saveFailed = true;

                var entry = ex.Entries.Single();
                entry.OriginalValues.SetValues((await entry.GetDatabaseValuesAsync())!);
            }

        } while (saveFailed);
        
        return obj;
    }

    /// <summary>
    /// remove an entity by id
    /// </summary>
    /// <param name="id">the id to look for</param>
    public virtual async Task Delete(string id)
    {
        var obj = await GetById(id);
        DBContext.Set<T>().Remove(obj!);
        await DBContext.SaveChangesAsync();
    }
    
    /// <summary>
    /// find entities match with a filter
    /// </summary>
    /// <param name="predicate">the function to filter</param>
    /// <returns>the list of entities</returns>
    public virtual async Task<List<T>> Find(Expression<Func<T, Boolean>> predicate)
    {
        return await DBContext.Set<T>().Where(predicate).ToListAsync();
    }
}