using Arena.AI.Core.Models;

namespace Arena.AI.Core.Logic.BattleLogic;

public static class UnitPlacer
{
    public static List<BattleAction> PlaceUnits(Team team, Side side)
    {
        var actions = new List<BattleAction>();

        for(var i = 0; i < team.Units.Length; i++)
        {
            var unit = team.Units[i];

            unit.YPosition = 3 + i * 2;
            unit.XPosition = side == Side.Left ? 1 : Constants.ArenaWidth;

            actions.Add(BattleActionFactory.PlaceUnit(unit));
        }

        return actions;
    }
}

public enum Side
{
    Left, 
    Right
}
