import os
import shutil
from PySide6.QtWidgets import QInputDialog, QMessageBox, QApplication

class ActionsController:
    def __init__(self):
        self.current_directory = os.getcwd()
    
    def process_command(self, command):
        command = command.lower().strip()
        
        if command.startswith("create folder"):
            return self._create_folder(command)
        elif command.startswith("create file"):
            return self._create_file(command)
        elif command.startswith("rename"):
            return self._rename_item(command)
        elif command.startswith("search"):
            return self._search_files(command)
        elif command.startswith("list"):
            return self._list_directory()
        elif command.startswith("cd"):
            return self._change_directory(command)
        else:
            return self._show_available_commands()
    
    def _create_folder(self, command):
        try:
            folder_name, ok = QInputDialog.getText(
                QApplication.instance().activeWindow(),
                "Create Folder",
                "Enter folder name:"
            )
            
            if ok and folder_name:
                folder_path = os.path.join(self.current_directory, folder_name)
                os.makedirs(folder_path, exist_ok=True)
                return f"✅ Created folder: {folder_name}"
            else:
                return "❌ Folder creation cancelled"
        except Exception as e:
            return f"❌ Error creating folder: {str(e)}"
    
    def _create_file(self, command):
        try:
            file_name, ok = QInputDialog.getText(
                QApplication.instance().activeWindow(),
                "Create File",
                "Enter file name (with extension):"
            )
            
            if ok and file_name:
                file_path = os.path.join(self.current_directory, file_name)
                with open(file_path, 'w') as f:
                    f.write("# New file created by AI Assistant\n")
                return f"✅ Created file: {file_name}"
            else:
                return "❌ File creation cancelled"
        except Exception as e:
            return f"❌ Error creating file: {str(e)}"
    
    def _rename_item(self, command):
        try:
            old_name, ok1 = QInputDialog.getText(
                QApplication.instance().activeWindow(),
                "Rename Item",
                "Enter current name:"
            )
            
            if ok1 and old_name:
                new_name, ok2 = QInputDialog.getText(
                    QApplication.instance().activeWindow(),
                    "Rename Item",
                    "Enter new name:"
                )
                
                if ok2 and new_name:
                    old_path = os.path.join(self.current_directory, old_name)
                    new_path = os.path.join(self.current_directory, new_name)
                    
                    if os.path.exists(old_path):
                        os.rename(old_path, new_path)
                        return f"✅ Renamed '{old_name}' to '{new_name}'"
                    else:
                        return f"❌ Item '{old_name}' not found"
                else:
                    return "❌ Rename cancelled"
            else:
                return "❌ Rename cancelled"
        except Exception as e:
            return f"❌ Error renaming: {str(e)}"
    
    def _search_files(self, command):
        try:
            search_term, ok = QInputDialog.getText(
                QApplication.instance().activeWindow(),
                "Search Files",
                "Enter search term:"
            )
            
            if ok and search_term:
                found_files = []
                for root, dirs, files in os.walk(self.current_directory):
                    for file in files:
                        if search_term.lower() in file.lower():
                            found_files.append(os.path.relpath(os.path.join(root, file), self.current_directory))
                
                if found_files:
                    return f"🔍 Found {len(found_files)} files:\n" + "\n".join(found_files[:10])
                else:
                    return f"🔍 No files found containing '{search_term}'"
            else:
                return "❌ Search cancelled"
        except Exception as e:
            return f"❌ Error searching: {str(e)}"
    
    def _list_directory(self):
        try:
            items = os.listdir(self.current_directory)
            folders = [item for item in items if os.path.isdir(os.path.join(self.current_directory, item))]
            files = [item for item in items if os.path.isfile(os.path.join(self.current_directory, item))]
            
            result = f"📁 Current directory: {self.current_directory}\n\n"
            result += f"📂 Folders ({len(folders)}):\n" + "\n".join(folders[:10])
            result += f"\n\n📄 Files ({len(files)}):\n" + "\n".join(files[:10])
            
            return result
        except Exception as e:
            return f"❌ Error listing directory: {str(e)}"
    
    def _change_directory(self, command):
        try:
            path = command.replace("cd", "").strip()
            if not path:
                path, ok = QInputDialog.getText(
                    QApplication.instance().activeWindow(),
                    "Change Directory",
                    "Enter directory path:"
                )
                if not ok or not path:
                    return "❌ Directory change cancelled"
            
            if os.path.exists(path) and os.path.isdir(path):
                self.current_directory = os.path.abspath(path)
                return f"✅ Changed to directory: {self.current_directory}"
            else:
                return f"❌ Directory not found: {path}"
        except Exception as e:
            return f"❌ Error changing directory: {str(e)}"
    
    def _show_available_commands(self):
        return """🔧 Available Actions:
        
• create folder - Create a new folder
• create file - Create a new file
• rename - Rename a file or folder
• search - Search for files
• list - List current directory contents
• cd <path> - Change directory

Type any of these commands to perform file operations!"""
