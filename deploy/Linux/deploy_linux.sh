clear
# Set the correct permissions for Artemis folder
sudo chmod 700 $PWD/../../
# Download necessary libraries with pip3
read -p "Install the necessary Python libraries? [Y,N]      " doit 
case $doit in  
  y|Y) pip3 install -r requirements_lin.txt --user ;; 
esac

# Generation of shortcut
read -p "Create a desktop shortcut? [Y/N]      " doit 
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
  ;;
  n|N) ;;
  *) echo "invalid option $REPLY";;
esac
echo ""
echo "SETTING COMPLETE!"
