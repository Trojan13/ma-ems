using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ConditionSelection : MonoBehaviour
{
    StroopTestController stroopTestController;
    GameObject[] conditionButtons;


    // Start is called before the first frame update
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {
        switch (stroopTestController.currentCondition)
        {
            case StroopTestController.Conditions.Control:
                break;
            case StroopTestController.Conditions.Visual:

                break;
            case StroopTestController.Conditions.EMS:

                break;
            case StroopTestController.Conditions.EMSVisual:

                break;
            default:

                break;
        }
    }

    private void SetButtonsEnabled()
    {

    }
}
