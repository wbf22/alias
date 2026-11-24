[Unit]
Description=Basic Shell Script Service
After=network.target

[Service]
ExecStart=/bin/bash /path/to/your/script.sh
WorkingDirectory=/path/to/working/dir
User=brandon
Group=brandon
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target

