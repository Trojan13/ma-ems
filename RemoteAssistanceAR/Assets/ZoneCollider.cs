using UnityEngine;

public class ZoneCollider : MonoBehaviour
{
    private StroopButton stroopButtonParentScript;
    private StroopTestController stroopTestControllerParentScript;

    [SerializeField]
    private bool isInnerZone;

    private void Start()
    {
        // Get the parent object's script
        stroopButtonParentScript = GetComponentInParent<StroopButton>();
        stroopTestControllerParentScript = GetComponentInParent<StroopTestController>();
    }

    private void OnTriggerEnter(Collider other)
    {
        if (
            other.transform.parent.name == "PinchPoint"
            || other.transform.parent.name == "GribPoint"
        )
        {
            if (
                stroopTestControllerParentScript.currentCondition
                    == StroopTestController.Conditions.Visual
                || stroopTestControllerParentScript.currentCondition
                    == StroopTestController.Conditions.EMSVisual
            )
            {
                stroopButtonParentScript.OnShowVisualWarningTriggerEnter(isInnerZone);
            }
            stroopTestControllerParentScript.OnZoneColliderTriggerEnter(
                isInnerZone,
                stroopButtonParentScript
            );
        }
    }

    private void OnTriggerExit(Collider other)
    {
        if (
            other.transform.parent.name == "PinchPoint"
            || other.transform.parent.name == "GribPoint"
        )
        {
            if (
                stroopTestControllerParentScript.currentCondition
                    == StroopTestController.Conditions.Visual
                || stroopTestControllerParentScript.currentCondition
                    == StroopTestController.Conditions.EMSVisual
            )
            {
                stroopButtonParentScript.OnShowVisualWarningTriggerExit(isInnerZone);
            }
            stroopTestControllerParentScript.OnZoneColliderTriggerExit(
                isInnerZone,
                stroopButtonParentScript
            );
        }
    }
}
