using MessagePack;
using MessagePack.Resolvers;
using Notification.Services;
using RabbitMQ.Client;
using RabbitMQ.Client.Events;

namespace Notification.Utils;

public class RabbitMQConnection : IRabbitMQConnection
{
    private const string QueueName = "notif";
    private const string QueueUser = "notif_user";
    private const string Exchange = "notification";
    private readonly IModel channelNotif;
    private readonly IModel channelUser;
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
        
        channelNotif.ExchangeDeclare(Exchange, ExchangeType.Direct);
        
        channelNotif.QueueDeclare(QueueName, true, false, false, null);
        channelUser.QueueDeclare(QueueUser, true, false, false, null);
        
        channelNotif.QueueBind(QueueName, Exchange, QueueName, null);
        channelUser.QueueBind(QueueUser, "user-created", QueueUser, null);
    }
    
    /// <summary>
    /// listen to the queues
    /// whenever there is a new msg on the queue, create a service and start the task
    /// </summary>
    public void StartConsuming()
    {
        var consumerNotif = new AsyncEventingBasicConsumer(channelNotif);
        var consumerUser = new AsyncEventingBasicConsumer(channelUser);
        consumerNotif.Received += OnConsumerNotifOnReceived;
        consumerUser.Received += OnConsumerUserOnReceived;
        channelNotif.BasicConsume(queue: QueueName, autoAck: true, consumer: consumerNotif);
        channelUser.BasicConsume(queue: QueueUser, autoAck: true, consumer: consumerUser);
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