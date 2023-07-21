using System.Collections;
using System.Linq;
using UnityEngine;

namespace MetaAdvancedFeatures.SceneUnderstanding
{
    public class MoveTestSetup : MonoBehaviour
    {
        public Transform MyTestSetupTransform;
        public Transform RightHandTransform;
        public bool isManualPositioning = false;
        public bool isManualRotating = false;
        public OVRSceneManager SceneManager;
        public float moveAmount = 0.1f; // the distance to move in each direction
        public float rotateAmount = 0.5f; // the angle to rotate in degrees

        private void Awake()
        {
            SceneManager = GetComponentInParent<OVRSceneManager>();
        }

        void Start()
        {
            SceneManager.SceneModelLoadedSuccessfully += OnSceneModelLoadedSuccessfully;
        }

        private void OnDestroy()
        {
            SceneManager.SceneModelLoadedSuccessfully -= OnSceneModelLoadedSuccessfully;
        }

        public void OnSceneModelLoadedSuccessfully()
        {
            Debug.Log("[Moving] Laoded scene model successfully");
            StartCoroutine(MoveTestSetupToTableFunction());
        }

        private IEnumerator MoveTestSetupToTableFunction()
        {
            Debug.Log("[Moving] MoveTestSetupToTableFunction");

            yield return new WaitForEndOfFrame();

            OVRSemanticClassification[] allTables = FindObjectsOfType<OVRSemanticClassification>()
                .Where(c => c.Contains(OVRSceneManager.Classification.Table))
                .ToArray();

            if (allTables.Length > 0) // Checking if a table was found
            {
                Vector3 tableCenter = allTables[0].transform.position;
                Vector3 tableSize = allTables[0].transform.localScale;

                // Adjusting the position to place MyTestSetupTransform on top of the table, considering its size
                tableCenter.y += tableSize.y / 2;

                MyTestSetupTransform.position = tableCenter;
                MyTestSetupTransform.rotation = allTables[0].transform.rotation;
            }
            else
            {
                Debug.LogError("No tables found!");
            }
        }

        public void ToggleManualPositioning()
        {
            isManualPositioning = !isManualPositioning;
        }

        public void ToggleManualRotating()
        {
            isManualRotating = !isManualRotating;
        }

        // Update is called once per frame
        void Update()
        {
            if (Input.GetKeyDown(KeyCode.A))
            {
                StartCoroutine(MoveTestSetupToTableFunction());
            }

            if (Input.GetKeyDown(KeyCode.S))
            {
                isManualPositioning = !isManualPositioning;
            }
            if (Input.GetKeyDown(KeyCode.D))
            {
                isManualRotating = !isManualRotating;
            }

            if (isManualPositioning)
            {
                MyTestSetupTransform.position = RightHandTransform.position;
            }

            if (isManualRotating)
            {
                MyTestSetupTransform.rotation = RightHandTransform.rotation;
            }
        }

        public void MoveUp()
        {
            MyTestSetupTransform.position += Vector3.up * moveAmount;
        }

        public void MoveDown()
        {
            MyTestSetupTransform.position += Vector3.down * moveAmount;
        }

        public void MoveLeft()
        {
            MyTestSetupTransform.position += Vector3.left * moveAmount;
        }

        public void MoveRight()
        {
            MyTestSetupTransform.position += Vector3.right * moveAmount;
        }

        public void RotateLeft()
        {
            MyTestSetupTransform.Rotate(Vector3.up, -rotateAmount); // Rotating around the Y-axis
        }

        public void RotateRight()
        {
            MyTestSetupTransform.Rotate(Vector3.up, rotateAmount); // Rotating around the Y-axis
        }
    }
}
