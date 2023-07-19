using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MoveDebugMenu : MonoBehaviour
{
    [SerializeField]
    private GameObject debugPanel;

    [SerializeField]
    private GameObject centerEyeAnchor;

    // Start is called before the first frame update
    void Start()
    {
        debugPanel = GameObject.Find("DebugPanel");
        centerEyeAnchor = GameObject.Find("CenterEyeAnchor");
    }

    // Update is called once per frame
    void Update()
    {
        if (debugPanel && centerEyeAnchor)
        {
            // Set debug panels X postition to the center eye anchors X position
            debugPanel.transform.position = new Vector3(
                centerEyeAnchor.transform.position.x,
                centerEyeAnchor.transform.position.y,
                debugPanel.transform.position.z
            );
            // Set debug panels Z postition to the center eye anchors Z position
        }
    }
}
