using Arena.AI.Core;
using Arena.AI.Core.Models;
using Microsoft.AspNetCore.SignalR;

namespace Arena.AI.SignalR;

public class ExternalPlayerHub : Hub<IPlayerClient>
{
    override public Task OnConnectedAsync()
    {
        return base.OnConnectedAsync();
    }

    public async Task Join(string battleId)
    {
        var wasJoined = ActiveBattlesManager.JoinAsPlayer(battleId, Context.ConnectionId);
        await Clients.Client(Context.ConnectionId).Joined(wasJoined);
    }
}


public interface IPlayerClient
{
    Task Joined(bool wasSuccessful);
    Task<UserAction> Act();
    Task PendingMovement(BattleState state);
}
