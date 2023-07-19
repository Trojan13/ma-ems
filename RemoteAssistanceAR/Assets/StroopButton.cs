using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Events;

using TMPro;

public class StroopButton : MonoBehaviour
{
    // Reference to the Button component
    [SerializeField]
    private GameObject button;

    // Reference to the TextMeshProUGUI component
    [SerializeField]
    private TextMeshPro buttonText;

    // Reference to the TextMeshProUGUI component
    [SerializeField]
    private TextMeshPro StopText;

    [SerializeField]
    private SpriteRenderer StopIcon;

    [SerializeField]
    private BoxCollider InnerZone;

    [SerializeField]
    private BoxCollider OuterZone;

    [SerializeField]
    private StroopTestController stroopTestController;

    private bool isCorrect;

    // Start is called before the first frame update
    void Start()
    {
        // Just to make sure the references are set
        if (button == null)
        {
            button = GetComponent<GameObject>();
        }

        if (buttonText == null)
        {
            // get component by name
            buttonText = GetComponentInChildren<TextMeshPro>();
        }

        if (StopText == null)
        {
            // get component by name
            StopText = GetComponentInChildren<TextMeshPro>();
        }

        if (StopIcon == null)
        {
            // get component by name
            StopIcon = GetComponentInChildren<SpriteRenderer>();
        }

        StopText.enabled = false;
        StopIcon.enabled = false;
    }

    // Call this function to set the color and text of the button
    // Pass in the color name and the actual Color
    public void SetButtonColorAndText(string text, Color buttonColor, Color textColor)
    {
        if (button == null || buttonText == null)
        {
            Debug.LogError("Button or TextMeshProUGUI references are not set!");
            return;
        }
        button.GetComponent<Renderer>().material.color = buttonColor;
        buttonText.text = text;
        buttonText.color = textColor;
    }

    public void SetIsCorrect(bool correct)
    {
        isCorrect = correct;
    }

    public void OnShowVisualWarningTriggerEnter(bool isInnerZone)
    {
        if (isCorrect || stroopTestController.state != StroopTestController.TestState.Playing)
        {
            return;
        }
        if (isInnerZone)
        {
            StopIcon.enabled = true;
        }
        else
        {
            StopText.enabled = true;
        }
    }

    public void OnShowVisualWarningTriggerExit(bool isInnerZone)
    {
        if (isInnerZone)
        {
            StopIcon.enabled = false;
        }
        else
        {
            StopText.enabled = false;
        }
    }
}
