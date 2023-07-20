using System.Collections;
using System.Collections.Generic;
using System.IO;
using TMPro;
using UnityEngine;
using System.Linq;
using System.Globalization;
using System;

public class Leaderboard : MonoBehaviour
{
    [SerializeField]
    private TextMeshPro leaderboardText;

    public class LeaderboardEntry
    {
        public string Nickname { get; set; }
        public float Time { get; set; }
        public int Errors { get; set; }
    }

    public List<LeaderboardEntry> LoadLeaderboardEntries(string filePath)
    {
        List<LeaderboardEntry> entries = new List<LeaderboardEntry>();

        using (var reader = new StreamReader(filePath))
        {
            reader.ReadLine(); // Skip the header line
            while (!reader.EndOfStream)
            {
                var line = reader.ReadLine();
                var values = line.Split(',');

                LeaderboardEntry entry = new LeaderboardEntry
                {
                    Nickname = values[1], // Assuming the nickname is in the second column
                    Errors = int.Parse(values[3]), // Assuming the errors are in the third column
                    Time = float.Parse(values[5], CultureInfo.InvariantCulture), // Assuming the time is in the sixth column
                };

                entries.Add(entry);
            }
        }

        return entries;
    }

    public List<LeaderboardEntry> SortLeaderboardEntries(List<LeaderboardEntry> entries)
    {
        // Sort by time (ascending) and then by errors (ascending)
        return entries.OrderBy(entry => entry.Time).ThenBy(entry => entry.Errors).Take(3).ToList();
    }

    public void DisplayLeaderboard(List<LeaderboardEntry> sortedEntries)
    {
        int i = 1;
        foreach (var entry in sortedEntries)
        {
            leaderboardText.text +=
                $"{i}: {entry.Nickname} - {Math.Round((decimal)entry.Time, 2)} - {entry.Errors}\n";
            i++;
        }
    }

    // Start is called before the first frame update
    void Start()
    {
        string filePath = Path.Combine(Application.dataPath, "data.csv");
        var entries = LoadLeaderboardEntries(filePath);
        var sortedEntries = SortLeaderboardEntries(entries);
        DisplayLeaderboard(sortedEntries);
    }

    // Update is called once per frame
    void Update() { }
}
