# Detective Conan Movie Trailer Generator
Two day hackathon project for **[AI Movie Studio](https://www.aimovie.studio/)**
[![AImovie.studio](./assets/image.png)](https://www.aimovie.studio/)

*(loosely inspired by https://fablestudio.github.io/showrunner-agents/)*

## Overview
This project automates the creation of movie trailers for the "Detective Conan" series. It converts a given news story into a compelling shotlist, generates audio and video for each shot, and compiles them into a final movie trailer.

## Components
1. **Script Generation**: Converts news stories into a script with detailed shotlists.
2. **Audio and Video Production**: Generates audio and video clips for each shot in the script.
3. **Video Editing**: Combines audio and video clips to produce the final movie trailer.

## Key Files and Directories
- `main.py`: Orchestrates the script generation and video production processes.
- `script.py`: Contains functions to generate scripts based on input news stories.
- `models.py`: Defines data models for scripts, shots, and characters.
- `editor.py`: Contains functions to edit and compile video clips into a movie trailer.
- `assets/`: Contains static files like character descriptions.
- `output/`: Contains generated scripts, audio, and video clips.
## Installation
1. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
2. Set up environment variables in `.env`:
   ```plaintext
    OPENAI_API_KEY=
    STABILITY_API_KEY=
    ELEVEN_API_KEY=
   ```

## Configuration
- Modify `assets/characters.yml` to update character details.
- Adjust script templates in `prompt.md` as needed for different story structures.

## Running the Project
Execute the main script to generate and compile the movie trailer:
```bash
python main.py
```


This project leverages AI models and video editing tools to automate the creation of engaging movie trailers, showcasing the capabilities of integrating AI with media production.

