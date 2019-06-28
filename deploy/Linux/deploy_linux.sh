clear
echo "
    ===================================
          Artemis 3 Deploy Script
                  LINUX
    ===================================
"

# Set the correct permissions for Artemis folder
echo "Gaining admin privileges and set folder read/write permission..."
echo ""
sudo chmod 700 $PWD/../../
# Download necessary libraries with pip3
read -p "Install the necessary Python libraries? [Y,N]..." doit 
case $doit in  
  y|Y) pip3 install -r requirements_lin.txt --user > log;; 
esac

# Generation of shortcut
echo ""
read -p "Create a desktop shortcut? [Y/N]..." doit 
case $doit in  
  y|Y)
cat << EOR > /home/$USER/.local/share/applications/artemis.desktop
#!/usr/bin/env xdg-open
[Desktop Entry]
Name=Artemis
StartupWMClass=artemis3
Exec=sh -c "cd $PWD/../../ && python3 artemis.py"
Terminal=False
Icon=artemis3
Type=Application
EOR
sudo cp ./artemis3.svg /usr/share/icons/
echo "
Link copied in: /home/$USER/.local/share/applications/artemis.desktop
Icon copied in: /usr/share/icons/artemis3.svg
"
  ;;
  n|N) ;;
  *) echo "invalid option $REPLY";;
esac
echo "
    ================================
           SETTING COMPLETE    
    ================================
"
