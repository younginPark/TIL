using Microsoft.AspNetCore.SignalR;

namespace SignalRWebpack.Hubs;

public class ChatHub : Hub
{
    // 서버가 메시지를 수신한 후 수신된 메시지를 모든 연결된 사용자에게 브로드캐스트
    public async Task NewMessage(long username, string message) =>
        await Clients.All.SendAsync("messageReceived", username, message);
}