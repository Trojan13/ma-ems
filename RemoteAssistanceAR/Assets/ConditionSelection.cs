using System.Collections;
using System.Collections.Generic;
using Oculus.Interaction;
using UnityEngine;
using UnityEngine.UI;

public class ConditionSelection : MonoBehaviour
{
    public StroopTestController stroopTestController;
    public PokeInteractable[] conditionButtons;

    // Start is called before the first frame update
    void Start() { }

    // Function to set the current condition
    public void SetCondition(StroopTestController.Conditions newCondition)
    {
        stroopTestController.currentCondition = newCondition;
    }

    // Update is called once per frame
    void Update()
    {
        if (stroopTestController.state != StroopTestController.TestState.Playing)
            // Update the state of the buttons
            foreach (var button in conditionButtons)
            {
                StroopTestController.Conditions condition;
                if (System.Enum.TryParse(button.gameObject.name, out condition))
                {
                    if (condition == stroopTestController.currentCondition)
                    {
                        // Disable and gray out the button corresponding to the active condition
                        button.Disable();
                    }
                    else
                    {
                        // Enable the other buttons and set their color to white
                        button.Enable();
                    }
                }
            }
    }
}
