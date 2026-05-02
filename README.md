# Err-Notes: An Errbot Note-Taking Plugin

`err-notes` is a plugin for [Errbot](http://errbot.io/) that allows you to manage notes directly from your favorite chat platform. It uses the `note-taker` library to store and retrieve notes, providing a seamless note-taking experience within your chat environment.

## Features

- **Create Notes**: Quick and easy note creation.
- **List Notes**: See all your stored notes at a glance.
- **Read/Show Notes**: Retrieve the content of a specific note by title or index.
- **Search**: Perform a universal search across all note titles and content.
- **Delete Notes**: Remove notes you no longer need.
- **Origin Tracking**: Automatically tracks which chat platform a note was created from.
- **Aliases**: Convenient command aliases for faster interaction.

## Installation

1.  **Dependencies**: This plugin requires the `note-taker` library. It should be installed automatically if you use the `requirements.txt` file, or you can install it manually:
    ```bash
    pip install git+ssh://git@github.com/fernand0/another-note-taking-app.git#egg=note-taker
    ```

2.  **Install the Plugin**: 
    Clone this repository into your Errbot's `plugins` directory:
    ```bash
    cd /path/to/your/errbot/plugins
    git clone https://github.com/fernand0/err-notes.git
    ```

3.  **Activate**: Restart Errbot or run `!plugin load err-notes` (depending on your Errbot configuration).

## Configuration

You can configure the storage directory for your notes. By default, it will attempt to use the configuration from the `note-taker` library.

To set a custom storage directory within Errbot:
```
!config NoteTaker {'STORAGE_DIR': '/path/to/your/notes'}
```

## Usage

All commands are prefixed with your bot's command prefix (e.g., `!`).

### Commands

-   **`!note list`**: Lists all available notes.
-   **`!note create <title> [-c content] [-t tags...]`**: Creates a new note.
    -   Example: `!note create "Meeting Notes" -c "Discussed the new README" -t work docs`
-   **`!note add <content>`**: Creates a note using the first line as the title and the rest as content.
-   **`!note read <title_or_num>`**: Displays the content of a note.
-   **`!note show <title_or_num>`**: Alias for `!note read`.
-   **`!note search <query>`**: Searches for notes matching the query.
-   **`!note delete <title_or_num>`**: Deletes the specified note.
-   **`!note del <title_or_num>`**: Alias for `!note delete`.
-   **`!note <content>`**: (Hidden catch-all) Quickly creates a note from the provided text, automatically generating a title with a timestamp.

## License

[Add License Information Here]
