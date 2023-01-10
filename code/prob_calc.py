import random
from enum import Enum

class RollResult(Enum):
    Fail = 1
    PartialSuccess = 2
    FullSuccess = 3

class OpposedResult(Enum):
    CriticalFail = 0
    Fail = 1
    Draw = 2
    FullSuccess = 3
    CriticalSuccess = 4

def SimpleRoll(statA, statB):
    x=1
    rollA = random.randint(1,100)
    if rollA <= statA:
        x += 1
    rollB = random.randint(1,100)
    if rollB <= statB:
        x += 1
    return (RollResult(x), DetectDoubles(rollA, rollB))

def DetectDoubles(rollA, rollB):
    return DetectDouble(rollA) or DetectDouble(rollB)

def DetectDouble(roll: int):
    if (roll//10) == (roll%10):
        return True
    return False

def OpposedOutcome(atkResult: RollResult, defResult: RollResult):
    if atkResult == defResult:
        return OpposedResult.Draw

    if atkResult == RollResult.Fail and defResult == RollResult.FullSuccess:
        return OpposedResult.CriticalFail

    if atkResult == RollResult.FullSuccess and defResult == RollResult.Fail:
        return OpposedResult.CriticalSuccess

    if atkResult == RollResult.Fail and defResult == RollResult.PartialSuccess:
        return OpposedResult.Fail

    if atkResult == RollResult.PartialSuccess:
        if defResult == RollResult.Fail:
            return OpposedResult.FullSuccess

        if defResult == RollResult.FullSuccess:
            return OpposedResult.Fail

    if atkResult == RollResult.FullSuccess:
        if defResult == RollResult.PartialSuccess:
            return OpposedResult.FullSuccess


def AdjustOppsedResultByFate(outcome, atkFate, defFate):    
    if atkFate and not defFate: # raise result one step
        global fateUpCnt
        fateUpCnt += 1
        if outcome == OpposedResult.CriticalSuccess:
            return outcome
        return OpposedResult(outcome.value+1)
    if not atkFate and defFate:
        global fateDownCnt
        fateDownCnt += 1
        if outcome == OpposedResult.CriticalFail:
            return outcome
        return OpposedResult(outcome.value-1)
    
    return outcome
        

def OpposedRoll(atkStatA, atkStatB, defStatA, defStatB):
    atk = SimpleRoll(atkStatA, atkStatB)
    dfs = SimpleRoll(defStatA, defStatB)
    outcome = OpposedOutcome(atk[0], dfs[0])
   # return outcome
    return AdjustOppsedResultByFate(outcome, atk[1], dfs[1])



# Monte-Carlo Sim
atkStatA = int(input("Enter value of the attacker's first stat: "))
atkStatB = int(input("Enter value of the attacker's second stat: "))
defStatA = 0
defStatB = 0
fateUpCnt = 0
fateDownCnt = 0
if "y" in input("Defender same stats? y/n:"):
    defStatA = atkStatA
    defStatB = atkStatB
else:
    defStatA = int(input("Enter value of the defender's first stat: "))
    defStatB = int(input("Enter value of the defender's second stat: "))

res = [0, 0, 0, 0, 0]
runs = 10_000_000

for i in range(1, runs):
    diceResult = OpposedRoll(atkStatA, atkStatB, defStatA, defStatB)
    if diceResult == OpposedResult.CriticalFail:
        res[0] += 1
    elif diceResult == OpposedResult.Fail:
        res[1] += 1
    elif diceResult == OpposedResult.Draw:
        res[2] += 1
    elif diceResult == OpposedResult.FullSuccess:
        res[3] += 1
    elif diceResult == OpposedResult.CriticalSuccess:
        res[4] += 1

print("CF %: " + str(res[0]/runs*100))
print("Fail %: " + str(res[1]/runs*100))
print("Draw %: " + str(res[2]/runs*100))
print("FS %: " + str(res[3]/runs*100))
print("CS %: " + str(res[4]/runs*100))
print("Fate up: " + str(fateUpCnt))
print("Fate down: " + str(fateDownCnt))