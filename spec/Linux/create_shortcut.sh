clear
echo "
    ===================================
          Artemis 3 Shortcut Creator
                  LINUX
    ===================================
"

# Set the correct permissions for Artemis folder
echo "Gaining admin privileges and set folder read/write permission..."
echo ""
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
sudo chmod 700 $DIR

# Generation of shortcut
file=/home/$USER/.local/share/applications/artemis.desktop
if [ -e "$file" ]; then
    echo "A shortcut of Artemis 3 is already present:"
    echo ""
    echo "R) Remove the shortcut and the icon file"
    echo "U) Update the shortcut"
    echo ""
    read -p "" doit 
    case $doit in  
        u|U)
        echo "#!/usr/bin/env xdg-open" > /home/$USER/.local/share/applications/artemis.desktop
        echo "[Desktop Entry]" >> /home/$USER/.local/share/applications/artemis.desktop
        echo "Name=Artemis" >> /home/$USER/.local/share/applications/artemis.desktop
        echo "StartupWMClass=artemis3" >> /home/$USER/.local/share/applications/artemis.desktop
        echo "Exec=sh -c 'cd $DIR && ./artemis' " >> /home/$USER/.local/share/applications/artemis.desktop
        echo "Terminal=False" >> /home/$USER/.local/share/applications/artemis.desktop
        echo "Icon=artemis3" >> /home/$USER/.local/share/applications/artemis.desktop
        sudo cp ./artemis3.svg /usr/share/icons/
        echo "Link Updated!"
    ;;
        r|R) 
        sudo rm /home/$USER/.local/share/applications/artemis.desktop
        sudo rm /usr/share/icons/artemis3.svg
        echo "Link and icon removed!"
    ;;
        *) echo "Sorry! Invalid option $REPLY";;
    esac
else 
    echo "#!/usr/bin/env xdg-open" > /home/$USER/.local/share/applications/artemis.desktop
    echo "[Desktop Entry]" >> /home/$USER/.local/share/applications/artemis.desktop
    echo "Name=Artemis" >> /home/$USER/.local/share/applications/artemis.desktop
    echo "StartupWMClass=artemis3" >> /home/$USER/.local/share/applications/artemis.desktop
    echo "Exec=sh -c 'cd $DIR && ./artemis' " >> /home/$USER/.local/share/applications/artemis.desktop
    echo "Terminal=False" >> /home/$USER/.local/share/applications/artemis.desktop
    echo "Icon=artemis3" >> /home/$USER/.local/share/applications/artemis.desktop
    sudo cp ./artemis3.svg /usr/share/icons/
    echo "
    Link copied in: /home/$USER/.local/share/applications/artemis.desktop
    Icon copied in: /usr/share/icons/artemis3.svg
    "
fi 

echo "
    ================================
           SETTING COMPLETE    
    ================================
"
