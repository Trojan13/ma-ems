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
        public OVRSceneManager SceneManager;

        private void Awake()
        {
            SceneManager = GetComponentInParent<OVRSceneManager>();
        }

        void Start()
        {
            SceneManager.SceneModelLoadedSuccessfully += OnSceneModelLoadedSuccessfully;
            Debug.Log("[Moving] Started");
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

            Debug.Log(allTables[0]);
            MyTestSetupTransform.position = new Vector3(
                allTables[0].transform.position.x + 1.0f,
                allTables[0].transform.position.y,
                allTables[0].transform.position.z
            );
        }

        // Update is called once per frame
        void Update()
        {
            if (Input.GetKeyDown(KeyCode.A))
            {
                Debug.Log("Sending A");
                StartCoroutine(MoveTestSetupToTableFunction());
            }

            if (Input.GetKeyDown(KeyCode.S))
            {
                isManualPositioning = !isManualPositioning;
            }

            if (isManualPositioning)
            {
                // Set mytestsetup position and rotation to right hand position and rotation
                MyTestSetupTransform.position = RightHandTransform.position;
                MyTestSetupTransform.rotation = RightHandTransform.rotation;
            }
        }
    }
}
