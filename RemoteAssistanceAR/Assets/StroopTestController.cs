using UnityEngine;
using UnityEngine.UI;
using System.IO;

using System.Collections;
using TMPro;

public class StroopTestController : MonoBehaviour
{
    [Header("UI Elements")]
    [SerializeField]
    private StroopButton[] stroopButtons;

    [SerializeField]
    private TextMeshPro startButtonText;

    [SerializeField]
    private TextMeshPro timerText;

    [SerializeField]
    private TextMeshPro stateText;

    [SerializeField]
    private TextMeshPro errorText;

    [SerializeField]
    private TextMeshPro tryCounterText;

    [SerializeField]
    private StroopTestFeedback stroopTestFeedback;

    [SerializeField]
    private EMSControl EMSControl;

    [SerializeField]
    private static string[] colorNames = { "Rot", "Blau", "Grün", "Gelb" };

    [Header("Test Parameters")]
    private TimerSystem timer;

    private StroopTestSequenceLoader currentStroopTestSequence;

    private TestState state = TestState.Idle;
    private int currentTestItemIndex = 0;
    private int correctCount = 0;
    private float tmpReactionTime;
    private float tmpTimeInZoneHigh;
    private float tmpTimeInZoneLow;
    private bool isButtonPressed = false;

    [Header("Dependent Variables")]
    [SerializeField]
    private string subjectID;

    private int errorCount = 0;
    private float totalTime;
    private float averageTimeReactionTime;
    private float timeInZoneHigh;
    private float timeInZoneLow;

    [Header("Independent Variables")]
    [SerializeField]
    public Conditions currentCondition;

    public enum TestState
    {
        Idle,
        Playing,
        Pause
    }

    public enum Conditions
    {
        Control,
        Visual,
        EMS,
        EMSVisual
    }

    void Start()
    {
        timer = GetComponent<TimerSystem>();

        InitializeUI();
        string filePath = Application.dataPath + "/sequence.json";

        if (File.Exists(filePath))
        {
            currentStroopTestSequence = new StroopTestSequenceLoader(File.ReadAllText(filePath));
        }
        else
        {
            Debug.LogError("Cannot load game data!");
        }
        Debug.Log("Sequence loaded. Rounds: " + currentStroopTestSequence.getRoundsCount());
    }

    // Update is called once per frame
    void Update()
    {
        if (timer.IsTiming)
        {
            int minutes = Mathf.FloorToInt(timer.TimePassed / 60F);
            int seconds = Mathf.FloorToInt(timer.TimePassed - minutes * 60);
            int milliseconds = Mathf.FloorToInt((timer.TimePassed * 1000) % 1000);

            timerText.text = string.Format("{0:00}:{1:00}:{2:000}", minutes, seconds, milliseconds);
        }

        if (Input.GetKeyDown(KeyCode.D))
        {
            StartCoroutine(stroopTestFeedback.Correct());
        }
    }

    public void StartTest()
    {
        switch (state)
        {
            case TestState.Idle:
                BeginTest();
                break;
            case TestState.Playing:
                PauseTest();
                break;
            case TestState.Pause:
                ResumeTest();
                break;
        }
    }

    private void BeginTest()
    {
        state = TestState.Playing;
        startButtonText.text = "Pause";

        timer.ResetTimer();
        timer.StartTiming();
        SetButtonsEnabled(true);

        StartCoroutine(ExecuteSequence());

        Debug.Log("Test started. Total time: " + timer.TimePassed);
    }

    private void PauseTest()
    {
        startButtonText.text = "Resume";
        timer.StopTiming();
        state = TestState.Pause;
        SetButtonsEnabled(false);

        Debug.Log("Test paused. Total time: " + timer.TimePassed);
    }

    private void ResumeTest()
    {
        startButtonText.text = "Pause";
        timer.StartTiming();
        state = TestState.Playing;
        SetButtonsEnabled(true);

        Debug.Log("Test resumed. Total time: " + timer.TimePassed);
    }

    public void EndTest()
    {
        timer.StopTiming();
        totalTime = timer.TimePassed;
        // Test is over
        Debug.Log("Test finished. Total time: " + timer.TimePassed);
        Debug.Log("Correct: " + correctCount + ", Error: " + errorCount);
        // Calc average reaction time
        averageTimeReactionTime = averageTimeReactionTime / (correctCount + errorCount);

        state = TestState.Idle;
        startButtonText.text = "Start";
        SetButtonsEnabled(false);

        WriteDataToFile(
            subjectID,
            currentCondition.ToString(),
            errorCount,
            correctCount,
            totalTime,
            averageTimeReactionTime,
            timeInZoneHigh,
            timeInZoneLow
        );

        Debug.Log("Test ended. Total time: " + timer.TimePassed);
    }

    private IEnumerator ExecuteSequence()
    {
        int sequenceRoundCount = currentStroopTestSequence.getRoundsCount();
        for (int i = 0; i < sequenceRoundCount; i++)
        {
            // Show the Stroop test item
            StroopTestRound currendRound = currentStroopTestSequence.GetRound(currentTestItemIndex);
            for (int j = 0; j < 4; j++)
            {
                StroopTestButton currentButtonFromRound = currentStroopTestSequence.GetButton(
                    currentTestItemIndex,
                    j
                );
                stroopButtons[j].SetButtonColorAndText(
                    currentButtonFromRound.buttonText,
                    currentButtonFromRound.GetButtonColor(),
                    currentButtonFromRound.GetTextColor()
                );
                stroopButtons[j].SetIsCorrect(currentButtonFromRound.isCorrect);
            }

            // Show the correct color name
            PlayColorSound(currendRound.outputColor);
            tmpReactionTime = Time.time * 1000; // Store the current time

            // Wait for a button press
            isButtonPressed = false;
            yield return new WaitUntil(() => isButtonPressed);
            currentTestItemIndex++;
        }

        // If there are more sequences, wait for 3 seconds before starting the next one
    }

    public void StroopButtonPressed(StroopButton button)
    {
        if (state == TestState.Playing)
        {
            // Calculate reaction time and store it
            averageTimeReactionTime += (Time.time * 1000 - tmpReactionTime);
            int pressedButtonIndex = System.Array.IndexOf(stroopButtons, button);

            StroopTestButton clickedButtonFromRound = currentStroopTestSequence.GetButton(
                currentTestItemIndex,
                pressedButtonIndex
            );

            StroopTestRound currendRound = currentStroopTestSequence.GetRound(currentTestItemIndex);

            if (clickedButtonFromRound.isCorrect)
            {
                correctCount++;
                Debug.Log("Correct Controller");
                StartCoroutine(stroopTestFeedback.Correct());
            }
            else
            {
                errorCount++;
                Debug.Log("Wrong Controller");
                StartCoroutine(stroopTestFeedback.Wrong());
            }
            tryCounterText.text = string.Format(
                "{0}/{1}",
                correctCount + errorCount,
                currentStroopTestSequence.getRoundsCount()
            );

            isButtonPressed = true;

            Debug.Log(
                $"Button {pressedButtonIndex} pressed. Correct: {currendRound.outputColor}, Time: {tmpReactionTime}"
            );

            // check if the test is over
            if (correctCount + errorCount == currentStroopTestSequence.getRoundsCount())
            {
                EndTest();
            }
        }
    }

    private void SetButtonsEnabled(bool enabled)
    {
        foreach (StroopButton button in stroopButtons)
        {
            button.enabled = enabled;
        }
    }

    private void InitializeUI()
    {
        timerText.text = "00:00:000";
        stateText.text = "Idle";
        errorText.text = "0";
        tryCounterText.text = "0/0";
        SetButtonsEnabled(false);
    }

    public void PlayColorSound(string colorString)
    {
        if (colorString == "Rot")
        {
            stroopTestFeedback.PlayRed();
        }
        if (colorString == "Grün")
        {
            stroopTestFeedback.PlayGreen();
        }
        if (colorString == "Blau")
        {
            stroopTestFeedback.PlayBlue();
        }
        if (colorString == "Gelb")
        {
            stroopTestFeedback.PlayYellow();
        }
    }

    public void WriteDataToFile(
        string subjectID,
        string currentCondition,
        int errorCount,
        int correctCount,
        float totalTime,
        float avgReactionTime,
        float timeInZoneHigh,
        float timeInZoneLow
    )
    {
        string filePath = Path.Combine(Application.dataPath, "data.csv");

        // Write the header to the file
        if (!File.Exists(filePath))
        {
            string header =
                "SubjectID,Condition,ErrorCount,CorrectCount,TotalTime,AvgReactionTime,TimeInZoneHigh,TimeInZoneLow\n";
            File.WriteAllText(filePath, header);
        }
        string data =
            $"{subjectID},{currentCondition},{errorCount},{correctCount},{totalTime},{avgReactionTime},{timeInZoneHigh},{timeInZoneLow}\n";
        File.AppendAllText(filePath, data);
    }

    public void OnZoneColliderTriggerEnter(bool isInnerZone, StroopButton button)
    {
        if (state != TestState.Playing)
        {
            return;
        }

        int pressedButtonIndex = System.Array.IndexOf(stroopButtons, button);

        StroopTestButton hoveredButton = currentStroopTestSequence.GetButton(
            currentTestItemIndex,
            pressedButtonIndex
        );

        if (hoveredButton.isCorrect)
        {
            return;
        }

        // Use the timer to measure the time in the zone
        if (isInnerZone)
        {
            tmpTimeInZoneLow = Time.time * 1000;
        }
        else
        {
            tmpTimeInZoneHigh = Time.time * 1000;
        }
        // Enable EMS
        if (currentCondition == Conditions.EMS || currentCondition == Conditions.EMSVisual)
        {
            if (isInnerZone)
            {
                EMSControl.setChannel0Enabled(true);
            }
            else
            {
                EMSControl.setChannel1Enabled(true);
            }
        }
    }

    public void OnZoneColliderTriggerExit(bool isInnerZone, StroopButton button)
    {
        if (state != TestState.Playing)
        {
            return;
        }
        // Use the timer to measure the time in the zone
        if (isInnerZone)
        {
            timeInZoneHigh = timeInZoneHigh + (Time.time - tmpTimeInZoneHigh) * 1000;
        }
        else
        {
            timeInZoneLow = timeInZoneLow + (Time.time - tmpTimeInZoneLow) * 1000;
        }
        // Disable EMS
        if (currentCondition == Conditions.EMS || currentCondition == Conditions.EMSVisual)
        {
            if (isInnerZone)
            {
                EMSControl.setChannel0Enabled(false);
            }
            else
            {
                EMSControl.setChannel1Enabled(false);
            }
        }
    }
}
