using Grpc.Core;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging.Abstractions;
using Moq;
using Notification;
using Notification.Services;

namespace NotificationTest;

public class NotificationServiceTest
{
    private readonly Notification.Services.NotificationService service;
    private readonly IRepository<Notification.Models.Notification> repository = new NotificationMockRepo();

    public NotificationServiceTest()
    {
        var serviceProvider = new ServiceCollection();
        serviceProvider.AddTransient<IRepository<Notification.Models.Notification>, NotificationMockRepo>();
        service = new Notification.Services.NotificationService(NullLogger<Notification.Services.NotificationService>.Instance, repository,
            serviceProvider.BuildServiceProvider());
    }


    [Fact]
    public void TestNewMsg()
    {
        // arrange
        dynamic msg = new Dictionary<string, string>
        {
            {"uid", "1"},
            {"msg", "test"}
        };
        
        // act
        var result = service.NewMsg(msg).Result;
        
        // assert
        Assert.True(result);
    }
    
    
    [Fact]
    public void TestGetNotifications()
    {
        // arrange
        var request = new NotificationRequest {Id = "1"};
        var responseStream = new Mock<IServerStreamWriter<NotificationResponse>>();
        var context = new Mock<ServerCallContext>();
        
        // act
        service.GetNotifications(request, responseStream.Object, context.Object).GetAwaiter().GetResult();

        // assert
        responseStream.Verify(
            x => x.WriteAsync(It.IsAny<NotificationResponse>()), Times.Once);
    }
}