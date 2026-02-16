from errbot import BotPlugin, botcmd, arg_botcmd
from note_app.manager import NoteManager
from note_app.config import Config
from datetime import datetime

class NoteTaker(BotPlugin):
    """
    A plugin to manage your notes via Errbot.
    """

    def get_configuration_template(self):
        """
        Configuration template for the plugin.
        """
        return {'STORAGE_DIR': None}

    def configure(self, configuration):
        """
        Handles configuration changes.
        """
        if configuration is not None and configuration != {}:
            config = dict(self.get_configuration_template(), **configuration)
        else:
            config = self.get_configuration_template()
        super().configure(config)

    def activate(self):
        """
        Triggered when the plugin is activated.
        """
        super().activate()
        
        # Get storage directory from config or fallback to global config
        storage_dir = self.config.get('STORAGE_DIR')
        if not storage_dir:
            global_config = Config()
            storage_dir = global_config.storage_dir
            
        self.log.info(f"Initializing NoteManager with directory: {storage_dir}")
        self.note_manager = NoteManager(storage_dir)

    @botcmd
    def note_list(self, msg, args):
        """List all your notes."""
        notes = self.note_manager.list_notes()
        if not notes:
            return "No notes found."
        
        response = f"Found {len(notes)} note(s):\n"
        for i, title in enumerate(notes, 1):
            response += f"{i}. {title}\n"
        return response

    @arg_botcmd('title', type=str)
    @arg_botcmd('--content', type=str, default="")
    @arg_botcmd('--tags', type=str, nargs='*', default=[])
    def note_create(self, msg, title=None, content=None, tags=None):
        """Create a new note."""
        # Detect origin from the message source (e.g., Telegram, Slack, etc.)
        origin = f"Errbot ({self._bot.mode})"
        
        success = self.note_manager.create_note(
            title=title, 
            content=content, 
            tags=tags, 
            origin=origin
        )
        
        if success:
            return f"Note '{title}' created successfully with origin '{origin}'."
        else:
            return f"Failed to create note '{title}'. It might already exist."

    @botcmd
    def note_add(self, msg, args):
        """Create a note taking the first line as title and the rest as content."""
        if not args:
            return "Please provide content. The first line will be the title, and the rest the content."
        
        lines = args.strip().split('\n', 1)
        title = lines[0].strip()
        content = lines[1].strip() if len(lines) > 1 else ""
        
        if not title:
            return "Note must have a title (first line)."

        origin = f"Errbot ({self._bot.mode})"
        success = self.note_manager.create_note(
            title=title,
            content=content,
            tags=[],
            origin=origin
        )
        
        if success:
            return f"Note '{title}' created successfully."
        else:
            return f"Failed to create note '{title}'. It might already exist."

    @arg_botcmd('title_or_num', type=str)
    def note_read(self, msg, title_or_num=None):
        """Read a note by title or number."""
        # Try to resolve title if it's a number
        resolved_title = self._resolve_title(title_or_num)
        
        note = self.note_manager.read_note(resolved_title)
        if not note:
            return f"Note '{resolved_title}' not found."

        response = f"**{note.title}** "
        if note.origin:
            response += f"_Origin: {note.origin}_ "
        response += f"_Created: {note.created_at}_ "
        
        if note.tags:
            response += f"Tags: {', '.join(note.tags)} "
        
        response += " " + note.content
        return response

    @arg_botcmd('title_or_num', type=str)
    def note_show(self, msg, title_or_num=None):
        """Alias for note_read."""
        for line in self.note_read(msg, title_or_num):
            yield line

    @arg_botcmd('query', type=str)
    def note_search(self, msg, query=None):
        """Search across all note fields."""
        results = self.note_manager.universal_search(query)
        if not results:
            return f"No notes found matching '{query}'."
        
        response = f"Search results for '{query}':\n"
        for i, title in enumerate(results, 1):
            response += f"{i}. {title}\n" 
        return response

    @arg_botcmd('title_or_num', type=str)
    def note_delete(self, msg, title_or_num=None):
        """Delete a note by title or number."""
        resolved_title = self._resolve_title(title_or_num)
        
        # Verify it exists first
        if not self.note_manager.read_note(resolved_title):
            return f"Note '{resolved_title}' not found."
            
        success = self.note_manager.delete_note(resolved_title)
        if success:
            return f"Note '{resolved_title}' deleted successfully."
        else:
            return f"Failed to delete note '{resolved_title}'."

    @arg_botcmd('title_or_num', type=str)
    def note_del(self, msg, title_or_num=None):
        """Alias for note_delete."""
        for line in self.note_delete(msg, title_or_num):
            yield line

    def _resolve_title(self, input_str):
        """Helper to resolve a title from either a string or a list index."""
        try:
            idx = int(input_str)
            all_notes = self.note_manager.list_notes()
            if 0 < idx <= len(all_notes):
                return all_notes[idx - 1]
        except ValueError:
            pass
        return input_str

    @botcmd(hidden=True)
    def note(self, msg, args):
        """
        Creates a new note from arbitrary text following the command prefix + 'note'.
        This acts as a catch-all if no other explicit command matches.
        """
        content = args.strip()

        if not content:
            return "Please provide some content for your note."

        # Generate a title from the content, similar to cli.py
        words = content.split()
        if len(words) > 5:
            base_title = " ".join(words[:5])
        else:
            base_title = content

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        
        max_title_len = 100
        if len(base_title) > max_title_len - len(timestamp) - 1:
            base_title = base_title[:max_title_len - len(timestamp) - 1 - 3] + "..."
        
        title = f"{base_title}_{timestamp}"

        origin = f"Errbot ({self._bot.mode})"

        success = self.note_manager.create_note(
            title=title,
            content=content,
            tags=["errbot"],
            origin=origin
        )

        if success:
            return f"Note '{title}' created successfully from Errbot."
        else:
            return f"Failed to create note '{title}'. It might already exist."

