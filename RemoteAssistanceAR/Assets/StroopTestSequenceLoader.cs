using System.Collections.Generic;
using UnityEngine;

[System.Serializable]
public class StroopTestButton
{
    public string buttonColor;
    public string buttonText;
    public string textColor;
    public bool isCorrect;

    public Color GetButtonColor()
    {
        return ColorStringToColor(buttonColor);
    }

    public Color GetTextColor()
    {
        return ColorStringToColor(textColor);
    }

    public Color ColorStringToColor(string colorString)
    {
        switch (colorString)
        {
            case "Red":
                return Color.red;
            case "Green":
                return Color.green;
            case "Blue":
                return Color.blue;
            case "Yellow":
                return Color.yellow;
            default:
                return Color.white;
        }
    }
}

[System.Serializable]
public class StroopTestRound
{
    public int roundNumber;
    public string outputColor;
    public List<StroopTestButton> buttons;
}

[System.Serializable]
public class StroopTestSequence
{
    public List<StroopTestRound> rounds;
}

public class StroopTestSequenceLoader
{
    private StroopTestSequence sequence;

    public StroopTestSequenceLoader(string jsonString)
    {
        // check if jsonString is set if not throw error and exit
        if (string.IsNullOrEmpty(jsonString))
        {
            Debug.LogError("jsonString is not set!");
            return;
        }

        sequence = JsonUtility.FromJson<StroopTestSequence>(jsonString);
        // check if sequence is set if not throw error and exit
        if (sequence == null || sequence.rounds == null)
        {
            Debug.LogError("sequence or sequence.rounds is not set!");
            return;
        }

        // Log the loaded data for debugging
        Debug.Log("Loaded " + sequence.rounds.Count + " rounds.");
    }

    public StroopTestRound GetRound(int index)
    {
        return sequence.rounds[index];
    }

    public int getRoundsCount()
    {
        return sequence.rounds.Count;
    }

    public StroopTestButton GetButton(int roundIndex, int buttonIndex)
    {
        return sequence.rounds[roundIndex].buttons[buttonIndex];
    }
}
