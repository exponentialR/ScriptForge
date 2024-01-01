
# Convert Bash Script to Clickable Application in Ubuntu

This guide describes how to convert a Bash script into a clickable desktop application in Ubuntu Linux.

## Step 1: Create a Desktop File

- Open a text editor and create a new file with a `.desktop` extension, e.g., `ZoteroLauncher.desktop`.

## Step 2: Edit the Desktop File

- Add the following content to the `.desktop` file:

```
[Desktop Entry]
Type=Application
Name=Zotero Launcher
Exec=/path/to/your/script.sh
Icon=/path/to/your/icon.png
Terminal=false
Comment=Launch Zotero
Categories=Office;
```

- Replace `/path/to/your/script.sh` with the full path to your Bash script.
- Replace `/path/to/your/icon.png` with the path to your icon, or omit this line if no icon is needed.
- Adjust `Name`, `Comment`, and `Categories` as appropriate.

## Step 3: Make Your Script Executable

- Run the following command to make your script executable:

```
chmod +x /path/to/your/script.sh
```

## Step 4: Make Your Desktop File Executable

- Make the `.desktop` file executable as well:

```
chmod +x /path/to/ZoteroLauncher.desktop
```

## Step 5: Place the Desktop File

- Move the `.desktop` file to the applications directory:

```
mv /path/to/ZoteroLauncher.desktop ~/.local/share/applications/
```

## Step 6: Access the Application

- 'Zotero Launcher' should now be accessible from your application menu.

## Step 7: Optional - Check for Errors

- If the application doesn't launch, verify the paths in your script and `.desktop` file.
