using MessagePack;
using MessagePack.Resolvers;
using Notification.Services;
using RabbitMQ.Client;
using RabbitMQ.Client.Events;

namespace Notification.Utils;

public class RabbitMQConnection : IRabbitMQConnection
{
    private const string QueueName = "notif";
    private const string QueueUserCreated = "notif_user_created";
    private const string QueueUserDelete = "notif_user_delete";
    private const string Exchange = "notification";
    private readonly IModel channelNotif;
    private readonly IModel channelUser;
    private readonly IModel channelUserDelete;
    private readonly IConnection conn;
    private readonly ILogger logger;
    private readonly IServiceProvider serviceProvider;

    public RabbitMQConnection(ILogger<RabbitMQConnection> logger, IServiceProvider serviceProvider, IConfiguration configuration)
    {
        this.logger = logger;
        this.serviceProvider = serviceProvider;
        var factory = new ConnectionFactory
        {
            HostName = configuration["RabbitMQ"],
            ClientProvidedName = "Dotnet:Notification",
            DispatchConsumersAsync = true,
        };
        conn = factory.CreateConnection();
        
        channelNotif = conn.CreateModel();
        channelUser = conn.CreateModel();
        channelUserDelete = conn.CreateModel();
        
        channelNotif.ExchangeDeclare(Exchange, ExchangeType.Direct);
        
        channelNotif.QueueDeclare(QueueName, true, false, false, null);
        channelUser.QueueDeclare(QueueUserCreated, true, false, false, null);
        channelUser.QueueDeclare(QueueUserDelete, true, false, false, null);
        
        channelNotif.QueueBind(QueueName, Exchange, QueueName, null);
        channelUser.QueueBind(QueueUserCreated, "user-created", QueueUserCreated, null);
        channelUserDelete.QueueBind(QueueUserDelete, "user-delete", QueueUserDelete, null);
    }
    
    /// <summary>
    /// listen to the queues
    /// whenever there is a new msg on the queue, create a service and start the task
    /// </summary>
    public void StartConsuming()
    {
        var consumerNotif = new AsyncEventingBasicConsumer(channelNotif);
        var consumerUserCreated = new AsyncEventingBasicConsumer(channelUser);
        var consumerUserDelete = new AsyncEventingBasicConsumer(channelUser);
        consumerNotif.Received += OnConsumerNotifOnReceived;
        consumerUserCreated.Received += OnConsumerUserOnReceived;
        consumerUserDelete.Received += OnConsumerUserDeleteOnReceived;
        channelNotif.BasicConsume(queue: QueueName, autoAck: true, consumer: consumerNotif);
        channelUser.BasicConsume(queue: QueueUserCreated, autoAck: true, consumer: consumerUserCreated);
        channelUserDelete.BasicConsume(queue: QueueUserDelete, autoAck: true, consumer: consumerUserDelete);
    }

    private async Task OnConsumerUserDeleteOnReceived(object sender, BasicDeliverEventArgs ea)
    {
        using (var scope = serviceProvider.CreateScope())
        {
            var service = scope.ServiceProvider.GetRequiredService<INotificationService>();
            var msg = MessagePackSerializer.Deserialize<dynamic>(ea.Body, ContractlessStandardResolver.Options);
            await service.DeleteUser(msg);
        }

        await Task.Yield();
    }

    private async Task OnConsumerUserOnReceived(object sender, BasicDeliverEventArgs ea)
    {
        using (var scope = serviceProvider.CreateScope())
        {
            var service = scope.ServiceProvider.GetRequiredService<INotificationService>();
            var msg = MessagePackSerializer.Deserialize<dynamic>(ea.Body, ContractlessStandardResolver.Options);
            await service.NewUser(msg);
        }

        await Task.Yield();
    }

    private async Task OnConsumerNotifOnReceived(object _, BasicDeliverEventArgs ea)
    {
        var body = ea.Body.ToArray();
        logger.LogInformation(System.Text.Encoding.Default.GetString(body));
        using (var scope = serviceProvider.CreateScope())
        {
            var service = scope.ServiceProvider.GetRequiredService<INotificationService>();
            var msg = MessagePackSerializer.Deserialize<dynamic>(ea.Body, ContractlessStandardResolver.Options);
            Task task = service.NewMsg(msg);
            task.Start();
        }

        await Task.Yield();
    }

    public void Close()
    {
        channelNotif.Close();
        channelUser.Close();
        conn.Close();
    }
}

public interface IRabbitMQConnection
{
    void StartConsuming();
    void Close();
}