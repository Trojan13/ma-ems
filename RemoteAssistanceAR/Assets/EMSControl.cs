using UnityEngine;
using System.Collections;
using System.Timers;

public class EMSControl : MonoBehaviour
{
    public SerialController serialController;
    private Timer timer0;
    private Timer timer1;
    private bool channel0Active;
    private bool channel1Active;

    // Intensity in percentage (0-100)
    [SerializeField]
    private int intensity = 100;

    // On-time in ms (1-50000)
    [SerializeField]
    private int onTime = 5000;

    void Start()
    {
        serialController = GameObject.Find("SerialController").GetComponent<SerialController>();

        timer0 = new Timer(onTime);
        timer0.Elapsed += (sender, e) => SendCommand(0);
        timer0.AutoReset = true;

        timer1 = new Timer(onTime);
        timer1.Elapsed += (sender, e) => SendCommand(1);
        timer1.AutoReset = true;

        // Initialise both channels to be off
        channel0Active = false;
        channel1Active = false;
    }

    private void SendCommand(int channel)
    {
        if ((channel == 0 && channel0Active) || (channel == 1 && channel1Active))
        {
            serialController.SendSerialMessage($"C{channel}I{intensity}T{onTime}G");
        }
    }

    private void StopCommand(int channel)
    {
        serialController.SendSerialMessage($"C{channel}I{0}T{0}G");
    }

    public void setChannel0Enabled(bool enabled)
    {
        channel0Active = enabled;
        if (channel0Active)
        {
            timer0.Start();
        }
        else
        {
            StopCommand(0);
            timer0.Stop();
        }
    }

    public void setChannel1Enabled(bool enabled)
    {
        channel1Active = enabled;
        if (channel1Active)
        {
            timer1.Start();
        }
        else
        {
            StopCommand(1);
            timer1.Stop();
        }
    }
}
