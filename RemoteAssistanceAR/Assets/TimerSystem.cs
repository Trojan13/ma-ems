using UnityEngine;

public class TimerSystem : MonoBehaviour
{
    public float TimePassed { get; private set; }
    public bool IsTiming { get; private set; }

    public void StartTiming()
    {
        IsTiming = true;
    }

    public void StopTiming()
    {
        IsTiming = false;
    }

    public void ResetTimer()
    {
        TimePassed = 0f;
    }

    private void Update()
    {
        if (IsTiming)
        {
            TimePassed += Time.deltaTime;
        }
    }
}
