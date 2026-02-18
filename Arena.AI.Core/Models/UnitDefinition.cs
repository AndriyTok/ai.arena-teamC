namespace Arena.AI.Core.Models;

public class UnitDefinition
{
    public UnitType Type { get; init; }
    public int Attack { get; init; }
    public int Defence { get; init; }
    public int Range { get; init; }
    public int Movement { get; init; }
}