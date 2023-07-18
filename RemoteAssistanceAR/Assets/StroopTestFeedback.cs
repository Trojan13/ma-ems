using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class StroopTestFeedback : MonoBehaviour
{
    [SerializeField]
    public AudioClip correctSound;

    [SerializeField]
    public AudioClip wrongSound;

    [SerializeField]
    public Sprite correctSprite;

    [SerializeField]
    public Sprite wrongSprite;

    [SerializeField]
    public AudioClip rotSound;

    [SerializeField]
    public AudioClip gruenSound;

    [SerializeField]
    public AudioClip blauSound;

    [SerializeField]
    public AudioClip gelbSound;

    private SpriteRenderer SpriteRenderer;
    private AudioSource AudioSource;

    // Start is called before the first frame update
    void Start()
    {
        AudioSource = GetComponent<AudioSource>();
        // Get child game object by name
        SpriteRenderer = GetComponent<SpriteRenderer>();

        // Hide the icons
        SpriteRenderer.enabled = false;
    }

    // Update is called once per frame
    void Update() { }

    public IEnumerator Correct()
    {
        Debug.Log("Correct");
        AudioSource.PlayOneShot(correctSound);
        SpriteRenderer.sprite = correctSprite;
        SpriteRenderer.color = Color.green;
        SpriteRenderer.enabled = true;

        yield return new WaitForSeconds(1);
        SpriteRenderer.enabled = false;
    }

    public IEnumerator Wrong()
    {
        Debug.Log("Wrong");
        AudioSource.PlayOneShot(wrongSound);
        SpriteRenderer.sprite = wrongSprite;
        SpriteRenderer.color = Color.red;
        SpriteRenderer.enabled = true;

        yield return new WaitForSeconds(1);
        SpriteRenderer.enabled = false;
    }

    public void PlayRed()
    {
        AudioSource.PlayOneShot(rotSound);
    }

    public void PlayGreen()
    {
        AudioSource.PlayOneShot(gruenSound);
    }

    public void PlayBlue()
    {
        AudioSource.PlayOneShot(blauSound);
    }

    public void PlayYellow()
    {
        AudioSource.PlayOneShot(gelbSound);
    }
}
