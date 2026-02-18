using Arena.AI.Core.Models;

namespace Arena.AI.Core.Logic;

public static class BattleActionFactory
{
    public static BattleAction PlaceUnit(Unit unit)
    {
        return new BattleAction
        {
            ActionType = BattleActionType.Appears,
            UnitName = unit.Name,
            UnitType = unit.Type,
            Destination = unit.GetPositionOnArena()
        };
    }

    public static BattleAction Move(Unit unit)
    {
        return new BattleAction
        {
            ActionType = BattleActionType.Moves,
            UnitName = unit.Name,
            UnitType = unit.Type,
            Destination = unit.GetPositionOnArena()
        };
    }

    public static BattleAction Attack(Unit actor, Unit target)
    {
        return new BattleAction
        {
            ActionType = BattleActionType.Attacks,
            UnitName = actor.Name,
            UnitType = actor.Type,
            Target = target.Name
        };
    }

    public static BattleAction LooseHealth(Unit actor, int healthAmount)
    {
        return new BattleAction
        {
            ActionType = BattleActionType.LoosesHealth,
            UnitName = actor.Name,
            UnitType = actor.Type,
            Amount = healthAmount
        };
    }

    public static BattleAction Die(Unit actor)
    {
        return new BattleAction
        {
            ActionType = BattleActionType.Dies,
            UnitName = actor.Name,
            UnitType = actor.Type
        };
    }
}
