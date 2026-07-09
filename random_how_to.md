# stop default keyring thing on ubuntu

Add password optional pam_gnome_keyring.so to /etc/pam.d/login (or gdm password), then on auto-login it won't prompt.