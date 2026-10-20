# Audio Strategy: trending music that matches each post

## What the official API allows (Meta docs, fetched 2026-10-20)
- **Search or fetch trending music and original sounds:** `GET /ig_audio?audio_type=music|original_sound&user_id=...`. With no search text it returns **trending** items. Only audio authorised for third-party publishing is returned, so the list can differ from what you see in the Instagram app.
- **Attach it when creating a Reel:** `audio_configuration={"audio_id", "audio_volume", "video_volume"}` (volumes 1-100).
- **Needs the Facebook-Login setup** (Phase 2 of the setup guide must use "API setup with Facebook login"). Business or Creator account plus a connected Page.
- **Limits:** the docs cover **Reels only**. I found nothing for attaching music to **carousels or Stories through the API**. For those, music would be added by hand in the app (a Story takes seconds; a carousel can have one song added when posting). Our automation therefore focuses audio on **static-image Reels**.
- No preview of the final Reel with audio via the API: the Reel publishes as configured.

## How "synergy" works here
Tracks carry no mood tags, so matching is heuristic and human-checked:
1. Every Reel has a **mood** (`focus`, `calm`, `confident`, `reflective`) set when I write it. Page A uses lo-fi and Hindi/Punjabi leaning keywords; Page B uses piano, acoustic and cinematic keywords. See `content/audio_moods.json`.
2. A weekly job (`audio-shortlist.yml`) asks the Audio API for trending music, runs a keyword search per mood, and writes a ranked table to `research/audio/<date>_<page>.md`. Score: +3 if currently trending, +2 per mood keyword that returns it, +1 if ads-eligible, -5 if used in the last 14 days, hard filter on length.
3. **I read the shortlist, judge title and artist against the post, and pin the pick** by adding `"audio_id"` to the Reel JSON. In month one you can also veto it, in line with approval of every post.
4. If nothing is pinned, the publisher auto-picks the top-ranked track at publish time. If the audio lookup fails, the Reel publishes silently rather than not at all.
5. Volume: the video track is silent and the music sits at 30-40%, so the on-screen text carries the message. The trending audio's job is **distribution** (Reels that use rising audio get surfaced), and its mood supports the message.

## Vocals
- For a text-led Reel, **instrumental or lightly sung** tracks suit best, because heavy vocals compete with reading. That is a design judgement, not data.
- Posts can set `"audio_type": "original_sound"` to use a trending **original sound** (often a voiceover or trend audio). That can lift reach but may clash with our message. Use it deliberately, and I'll flag each use for your approval.

## What must be tested on the first live Reel
- That the Audio API works with the owner's tokens (permissions and account type).
- That the attached audio plays at the chosen volume, and that the Reel is eligible for recommendation.
- Whether the keyword searches give sensible, on-mood results for Hinglish/Indian lo-fi on Page A. If not, tune the keywords.

## Rules
- Use only audio the API returns (authorised for third-party publishing). No downloading music from elsewhere.
- Carousels and Stories: music is manual in the app if you want it; I'll mention a suggested mood in each post's notes.
