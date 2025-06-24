from youtube_transcript_api import (
    YouTubeTranscriptApi,
)  # Install youtube_transcript_api and scrapetube
from youtube_transcript_api.formatters import TextFormatter
import scrapetube

# Enter the Youtube Channel ID
channel_id = "UCXv0AGtxxRzxJ7lP1M2l4jA"

# Enter the name of the txt file to be saved
file_name = "ultra_marathi"

# Enter the path of the folder to save the txt file
folder_path = "Shardul/Youtube Subtitles"

videos = scrapetube.get_channel(channel_id)


# Function to extract video title
def extract_title(video):
    title_runs = video.get("title", {}).get("runs", [])
    if title_runs:
        return "".join([run.get("text", "") for run in title_runs])
    return "No title found"


with open(f"{folder_path}/{file_name}.txt", "a+", encoding="utf-8") as txt_file:
    for video in videos:
        video_id = video["videoId"]
        video_title = extract_title(video)
        # print(video_title)
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["mr"])
            formatter = TextFormatter()
            txt_formatted = formatter.format_transcript(transcript)
        except:
            try:
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                transcript = transcript_list.find_transcript(["en"])
                # print(transcript.fetch())
                translated_transcript = transcript.translate("mr")
                # print(translated_transcript.fetch())
                # formatter = TextFormatter()
                txt_formatted = "\n".join(
                    [item["text"] for item in translated_transcript.fetch()]
                )
                # print(txt_formatted)
            except:
                try:
                    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                    transcript = transcript_list.find_transcript(["en-US"])
                    # print(transcript.fetch())
                    translated_transcript = transcript.translate("mr")
                    # print(translated_transcript.fetch())
                    # formatter = TextFormatter()
                    txt_formatted = "\n".join(
                        [item["text"] for item in translated_transcript.fetch()]
                    )
                    # print(txt_formatted)
                except:
                    try:
                        transcript_list = YouTubeTranscriptApi.list_transcripts(
                            video_id
                        )
                        transcript = transcript_list.find_transcript(["hi"])
                        # print(transcript.fetch())
                        translated_transcript = transcript.translate("mr")
                        # print(translated_transcript.fetch())
                        # formatter = TextFormatter()
                        txt_formatted = "\n".join(
                            [item["text"] for item in translated_transcript.fetch()]
                        )
                        # print(txt_formatted)
                    except Exception:
                        print(f'Subtitles not found for video "{video_title}".')
                        continue
        txt_file.write(f"Title: {video_title}\n")
        txt_file.write(txt_formatted + "\n\n")
        print(f'Success! Transcript for video "{video_title}" saved.')


# video_id="CTBnaliRRSE"
# transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['hi']) #Enter the language of the transcript
# formatter = TextFormatter()
# txt_formatted = formatter.format_transcript(transcript)
# print(txt_formatted)
